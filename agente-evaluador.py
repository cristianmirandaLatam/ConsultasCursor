import argparse
import concurrent.futures
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from urllib.parse import quote, urlparse, urlunparse

import urllib.request
import urllib.error
import gzip
import zlib

from agenteval import jinja_env
from agenteval.test.test_result import TestResult

CLAVES_AWS = [
    "AWS_ACCESS_KEY_ID",
    "AWS_SECRET_ACCESS_KEY",
    "AWS_SESSION_TOKEN",
    "AWS_DEFAULT_REGION",
    "AWS_REGION",
    "AWS_PROFILE",
    "AWS_SHARED_CREDENTIALS_FILE",
    "AWS_CONFIG_FILE",
]

CLAVES_JIRA = [
    "JIRA_BASE_URL",
    "JIRA_USERNAME",
    "JIRA_TOKEN",
    "TEST_CYCLE",
    "AMBIENTE",
    "ATTACH_JSON",
    "TRACES_DIR",
]

RESULT_MAP = {"A": "Passed", "B": "Failed", "UNKNOWN": "Unknown"}
USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AgentEval/1.0 (+urllib)"
PRINT_ERR_BODY_BYTES = 1500 

VERBOSO = False
def jprint(*args, **kwargs):
    if VERBOSO:
        print(*args, **kwargs)

ANSI_RED = "\x1b[31m"
ANSI_GREEN = "\x1b[32m"
ANSI_RESET = "\x1b[0m"

def _redact(h):
    h = dict(h or {})
    if "Authorization" in h:
        h["Authorization"] = "Bearer ***redacted***"
    return h

def _acorta(s, n=1024):
    try:
        s = str(s)
    except Exception:
        s = repr(s)
    return s if len(s) <= n else s[:n] + f"… [{len(s)} chars]"

def _is_akamai_html_forbidden(ct: str, body: str) -> bool:
    ct = (ct or "").lower()
    if "text/html" not in ct:
        return False
    b = (body or "").lower()
    return ("<title>access denied</title>" in b) or ("akamai" in b) or ("edgesuite" in b)

def _with_common_headers(req: urllib.request.Request, token: str, accept_json: bool = True):
    req.add_header("Authorization", f"Bearer {token}")
    if accept_json:
        req.add_header("Accept", "application/json")
    req.add_header("Accept-Encoding", "identity")
    req.add_header("User-Agent", USER_AGENT)
    return req

def _force_https(url: str) -> str:
    try:
        p = urlparse(url)
        if p.scheme == "http":
            return urlunparse(("https", p.netloc, p.path, p.params, p.query, p.fragment))
    except Exception:
        pass
    return url

def _maybe_decompress(raw: bytes, content_encoding: str | None, content_type: str | None) -> bytes:
    ce = (content_encoding or "").lower().strip()
    if ce == "gzip":
        try:
            return gzip.decompress(raw)
        except Exception:
            pass
    elif ce == "deflate":
        try:
            return zlib.decompress(raw)
        except Exception:
            try:
                return zlib.decompress(raw, -zlib.MAX_WBITS)
            except Exception:
                pass
    if len(raw) >= 2 and raw[0] == 0x1F and raw[1] == 0x8B:
        try:
            return gzip.decompress(raw)
        except Exception:
            pass
    try:
        return zlib.decompress(raw)
    except Exception:
        try:
            return zlib.decompress(raw, -zlib.MAX_WBITS)
        except Exception:
            pass
    return raw

def sanear(nombre: str) -> str:
    s = re.sub(r"[^\w\-.]+", "_", nombre.strip().lower())
    return s[:80] or "ejecucion"

def leer_tail(ruta: Path, n: int):
    try:
        with open(ruta, "r", encoding="utf-8", errors="replace") as f:
            lineas = f.readlines()
            return lineas[-n:]
    except FileNotFoundError:
        return [f"(no existe {ruta})\n"]

def cargar_env(ruta_env: Path | None) -> dict:
    env = os.environ.copy()
    if ruta_env and ruta_env.exists():
        with open(ruta_env, "r", encoding="utf-8") as f:
            for linea in f:
                l = linea.strip()
                if not l or l.startswith("#") or "=" not in l:
                    continue
                k, v = l.split("=", 1)
                k, v = k.strip(), v.strip()
                if len(v) >= 2 and v[0] == v[-1] and v[0] in ("'", '"'):
                    v = v[1:-1]
                if k in CLAVES_AWS + CLAVES_JIRA and v:
                    env[k] = v
    env["PYTHONPATH"] = os.pathsep.join([env.get("PYTHONPATH", ""), str(Path(".").resolve()), str(Path("tests").resolve())])
    return env

def cargar_mapa_jira_desde_yaml(ruta_yaml: Path) -> dict:
    try:
        import yaml
    except Exception:
        return {}
    try:
        with open(ruta_yaml, "r", encoding="utf-8") as f:
            doc = yaml.safe_load(f)
        out = {}
        if isinstance(doc, dict) and isinstance(doc.get("tests"), dict):
            for nombre, cfg in doc["tests"].items():
                if isinstance(cfg, dict):
                    key = cfg.get("test_case_key") or cfg.get("jira_issue")
                    if isinstance(key, str) and key.strip():
                        out[str(nombre)] = key.strip()
        return out
    except Exception:
        return {}

def jira_config(entorno: dict) -> tuple[bool, dict, list[str]]:
    cfg = {}
    cfg["base_url"] = (entorno.get("JIRA_BASE_URL") or "").strip().rstrip("/")
    cfg["username"] = (entorno.get("JIRA_USERNAME") or "").strip()
    cfg["token"] = (entorno.get("JIRA_TOKEN") or "").strip()
    cfg["test_cycle"] = (entorno.get("TEST_CYCLE") or "").strip()
    cfg["ambiente"] = (entorno.get("AMBIENTE") or "LOCAL").strip()
    cfg["attach_json"] = str(entorno.get("ATTACH_JSON") or "false").lower() == "true"
    cfg["traces_dir"] = (entorno.get("TRACES_DIR") or "agenteval_traces").strip()
    faltan = [k for k in ["base_url", "username", "token", "test_cycle"] if not cfg.get(k)]
    return (len(faltan) == 0, cfg, faltan)

def http_json(method: str, url: str, token: str, body: dict | list | None = None,
              accept_json: bool = True, extra_headers: dict | None = None,
              allow_html: bool = False) -> dict | list | str:
    data = None
    if body is not None and method.upper() != "GET":
        data = json.dumps(body).encode("utf-8")

    req = urllib.request.Request(url, data=data, method=method.upper())
    _with_common_headers(req, token, accept_json=accept_json)
    if body is not None and method.upper() != "GET":
        req.add_header("Content-Type", "application/json")
    if extra_headers:
        for k, v in extra_headers.items():
            req.add_header(k, v)

    jprint(f"Jira: {method.upper()} {url}")
    jprint("Jira: Headers:", _redact(dict(req.header_items())))
    if data is not None:
        jprint("Jira: Body:", _acorta(data.decode("utf-8", "replace"), 2000))

    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            ct = resp.headers.get("content-type", "")
            ce = resp.headers.get("content-encoding", "")
            raw = resp.read()
            raw = _maybe_decompress(raw, ce, ct)
            txt = raw.decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        ct = e.headers.get("content-type", "") if e.headers else ""
        ce = e.headers.get("content-encoding", "") if e.headers else ""
        try:
            raw_err = e.read()
        except Exception:
            raw_err = b""
        raw_err = _maybe_decompress(raw_err, ce, ct)
        err_txt = raw_err.decode("utf-8", "replace")
        jprint(f"Jira: HTTPError {e.code} {e.reason} CT={ct}")
        jprint("Jira: Headers:", _redact(dict(e.headers or {})))
        jprint("Jira: Body (inicio):", _acorta(err_txt, PRINT_ERR_BODY_BYTES))
        raise
    except urllib.error.URLError as e:
        jprint(f"Jira: URLError: {e.reason}")
        raise

    if "application/json" in (ct or "").lower():
        try:
            return json.loads(txt)
        except Exception:
            raise RuntimeError(f"Respuesta JSON inválida. CT={ct} cuerpo={_acorta(txt)}")
    else:
        if allow_html:
            return txt
        raise RuntimeError(f"Jira devolvió tipo inesperado: {ct} cuerpo={_acorta(txt)}")

def obtener_user_key(base_url: str, token: str, username: str) -> str:
    for u in [f"{base_url}/rest/api/2/myself", f"{base_url}/rest/api/3/myself"]:
        try:
            data = http_json("GET", u, token, accept_json=True)
            key = (data.get("key") or data.get("accountId") or "").strip()
            if key:
                jprint("Jira: UserKey:", key)
                return key
        except Exception as e:
            jprint("Jira: Fallo:", e)
    return ""

def _atm_post_results(url: str, token: str, body_list: list) -> dict | list | str:
    return http_json("POST", url, token, body=body_list, accept_json=True)

def _retry_on_akamai_403(base_url: str, token: str, url: str, body_list: list,
                         with_executed_by: bool) -> tuple[bool, dict | list | None]:
    https_url = _force_https(url)
    if https_url != url:
        try:
            data = _atm_post_results(https_url, token, body_list)
            return True, data
        except urllib.error.HTTPError as e:
            ct = e.headers.get("content-type", "") if e.headers else ""
            ce = e.headers.get("content-encoding", "") if e.headers else ""
            try:
                raw_err = e.read()
            except Exception:
                raw_err = b""
            raw_err = _maybe_decompress(raw_err, ce, ct)
            err_txt = raw_err.decode("utf-8", "replace")
            if e.code != 403 or not _is_akamai_html_forbidden(ct, err_txt):
                raise
        except Exception:
            raise

    if with_executed_by:
        try:
            body_no_exec = []
            for item in body_list:
                x = dict(item)
                x.pop("executedBy", None)
                body_no_exec.append(x)
            data = _atm_post_results(https_url, token, body_no_exec)
            jprint("Jira: Intentando sin executedBy.")
            return True, data
        except Exception:
            pass

    return False, None

def derivar_estado(rc: int, mapa: dict) -> tuple[str, str]:
    interno = "A" if rc == 0 else "B"
    final = mapa.get(interno) or ("Passed" if interno == "A" else "Failed")
    return interno, final

def comentar_para_jira(
    nombre_test: str,
    ruta_yaml: Path,
    inicio: datetime,
    fin: datetime,
    interno: str,
    estado: str,
    reasoning: str = "",
):
    lineas = [
        "agente-evaluador",
        f"test_name: {nombre_test}",
        f"yaml: {ruta_yaml.name}",
        f"inicio: {inicio.isoformat(timespec='seconds')}",
        f"fin: {fin.isoformat(timespec='seconds')}",
        f"estado_interno: {interno}",
        f"estado: {estado}",
    ]
    if reasoning and estado.lower().startswith("fail"):
        lineas.append(f"reasoning: {reasoning}")
    return "\n".join(lineas)

def jira_adjuntar_archivo(url: str, token: str, ruta: Path):
    limite = "----agente-evaluador-boundary"
    contenido = ruta.read_bytes()
    cuerpo = (
        (
            f"--{limite}\r\n"
            f'Content-Disposition: form-data; name="file"; filename="{ruta.name}"\r\n'
            f"Content-Type: application/octet-stream\r\n\r\n"
        ).encode("utf-8")
        + contenido
        + f"\r\n--{limite}--\r\n".encode("utf-8")
    )
    req = urllib.request.Request(url, data=cuerpo, method="POST")
    _with_common_headers(req, token, accept_json=False)
    req.add_header("Content-Type", f"multipart/form-data; boundary={limite}")
    req.add_header("X-Atlassian-Token", "no-check")

    jprint("Jira: POST adjunto", url, "archivo:", ruta.name)
    jprint("Jira: Headers:", _redact(dict(req.header_items())))
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            _ = resp.read()
        return True
    except urllib.error.HTTPError as e:
        ct = e.headers.get("content-type", "") if e.headers else ""
        ce = e.headers.get("content-encoding", "") if e.headers else ""
        try:
            raw_err = e.read()
        except Exception:
            raw_err = b""
        raw_err = _maybe_decompress(raw_err, ce, ct)
        err_txt = raw_err.decode("utf-8", "replace")
        jprint(f"Jira: HTTPError adjunto {e.code} {e.reason} CT={ct}")
        jprint("Jira: Headers:", _redact(dict(e.headers or {})))
        jprint("Jira: Body (inicio):", _acorta(err_txt, PRINT_ERR_BODY_BYTES))
        if e.code == 403 and _is_akamai_html_forbidden(ct, err_txt):
            https_url = _force_https(url)
            if https_url != url:
                jprint("Jira: Reintentando adjunto por HTTPS…")
                req2 = urllib.request.Request(https_url, data=cuerpo, method="POST")
                _with_common_headers(req2, token, accept_json=False)
                req2.add_header("Content-Type", f"multipart/form-data; boundary={limite}")
                req2.add_header("X-Atlassian-Token", "no-check")
                try:
                    with urllib.request.urlopen(req2, timeout=60) as resp2:
                        _ = resp2.read()
                        jprint("Jira: Adjunto OK por HTTPS")
                        return True
                except Exception as e2:
                    jprint("Jira: Reintento adjunto HTTPS falló:", e2)
        raise

def _buscar_jsones_de_prueba(traces_root: Path, nombre_test: str) -> list[Path]:
    encontrados: list[Path] = []
    raiz = traces_root.resolve()
    if not raiz.exists() or not raiz.is_dir():
        return encontrados

    sane = sanear(nombre_test)
    exact_name = f"{sane}.json"

    # Intentar primero el archivo con nombre exacto
    exact_path = raiz / exact_name
    if exact_path.exists() and exact_path.is_file():
        try:
            raw = exact_path.read_text("utf-8", "replace")
            if raw and raw[0] == "\ufeff":
                raw = raw[1:]
            obj = json.loads(raw)
            tname = ""
            if isinstance(obj, dict):
                tname = (obj.get("test_name") or obj.get("name") or "").strip()
            elif isinstance(obj, list) and obj and isinstance(obj[0], dict):
                tname = (obj[0].get("test_name") or obj[0].get("name") or "").strip()
            if tname == nombre_test:
                return [exact_path]  
        except Exception:
            pass

    # Si no sirvió el exacto, lo busco
    for name in os.listdir(raiz):
        if not name.lower().endswith(".json"):
            continue
        p = raiz / name
        if not p.is_file():
            continue
        try:
            raw = p.read_text("utf-8", "replace")
            if raw and raw[0] == "\ufeff":
                raw = raw[1:]
            obj = json.loads(raw)
            tname = ""
            if isinstance(obj, dict):
                tname = (obj.get("test_name") or obj.get("name") or "").strip()
            elif isinstance(obj, list) and obj and isinstance(obj[0], dict):
                tname = (obj[0].get("test_name") or obj[0].get("name") or "").strip()
            if tname == nombre_test:
                encontrados.append(p)
                continue
        except Exception:
            pass

    vistos, unicos = set(), []
    for p in encontrados:
        rp = p.resolve()
        if rp not in vistos:
            unicos.append(p)
            vistos.add(rp)
    unicos.sort(key=lambda p: p.stat().st_mtime)
    return unicos




def _extraer_estados_por_test(traces_root: Path, nombres_tests: list[str]) -> dict[str, tuple[str, str, str, str]]:
    res: dict[str, tuple[str, str, str, str]] = {}
    for nombre in nombres_tests:
        jsones = _buscar_jsones_de_prueba(traces_root, nombre)
        ultimo_status = None  # A, B, UNKNOWN
        fallback_status = None  # Para test_status en _generate_test_status
        reasoning = ""
        error_reasoning = ""
        conversation = ""

        for p in jsones:
            try:
                raw = p.read_text("utf-8", "replace")
                if raw and raw[0] == "\ufeff":
                    raw = raw[1:]
                data = json.loads(raw)
                error_reasoning = data.get("error", "") if isinstance(data, dict) else ""
            except Exception:
                continue

            def iter_items(obj):
                if isinstance(obj, dict):
                    yield obj
                    for v in obj.values():
                        if isinstance(v, (dict, list)):
                            yield from iter_items(v)
                elif isinstance(obj, list):
                    for it in obj:
                        if isinstance(it, (dict, list)):
                            yield from iter_items(it)

            for item in iter_items(data):
                step_name = item.get("step_name")
                if step_name == "_generate_evaluation":
                    ts = item.get("evaluation")
                    if isinstance(ts, str):
                        ts_norm = ts.strip().upper()
                        if ts_norm in ("A", "B", "UNKNOWN"):
                            ultimo_status = ts_norm
                            reasoning = item.get("reasoning", "")
                elif step_name == "_generate_test_status":
                    ts = item.get("test_status")
                    if isinstance(ts, str):
                        ts_norm = ts.strip().upper()
                        if ts_norm in ("A", "B", "UNKNOWN"):
                            fallback_status = ts_norm
                    # Extract conversation from prompt
                    prompt = item.get("prompt", "")
                    import re
                    conv_match = re.search(r'<conversation>(.*?)</conversation>', prompt, re.DOTALL)
                    if conv_match:
                        conversation = conv_match.group(1).strip()

            # If no reasoning from evaluation, check for error in the JSON
            if not reasoning:
                reasoning = error_reasoning

        if ultimo_status is None:
            ultimo_status = fallback_status

        if ultimo_status is None:
            # Check if there's an error in the JSON (for failed tests)
            if error_reasoning:
                ultimo_status = "B"  # Failed
            else:
                continue

        estado_interno = ultimo_status
        estado_final = RESULT_MAP.get(estado_interno, "Unknown")
        res[nombre] = (estado_interno, estado_final, reasoning or error_reasoning, conversation)

    return res

def _extraer_tiempos_por_test(traces_root: Path, nombres_tests: list[str]) -> dict[str, tuple[datetime, datetime]]:
    def _iter_items(obj):
        if isinstance(obj, dict):
            yield obj
            for v in obj.values():
                if isinstance(v, (dict, list)):
                    yield from _iter_items(v)
        elif isinstance(obj, list):
            for it in obj:
                if isinstance(it, (dict, list)):
                    yield from _iter_items(it)

    def _parse_dt(ts):
        from datetime import datetime, timezone
        if isinstance(ts, (int, float)):
            val = float(ts)
            if val > 1e12:  # ms
                val /= 1000.0
            return datetime.fromtimestamp(val, tz=timezone.utc)
        if isinstance(ts, str):
            s = ts.strip()
            try:
                # Soporta '...Z'
                if s.endswith("Z"):
                    s = s[:-1] + "+00:00"
                return datetime.fromisoformat(s)
            except Exception:
                for fmt in ("%Y-%m-%d %H:%M:%S", "%Y/%m/%d %H:%M:%S"):
                    try:
                        return datetime.strptime(s, fmt)
                    except Exception:
                        pass
        return None

    res: dict[str, tuple[datetime, datetime]] = {}
    for nombre in nombres_tests:
        jsones = _buscar_jsones_de_prueba(traces_root, nombre)
        t0, t1 = None, None

        for p in jsones:
            try:
                raw = p.read_text("utf-8", "replace")
                if raw and raw[0] == "\ufeff":
                    raw = raw[1:]
                data = json.loads(raw)
            except Exception:
                continue

            for item in _iter_items(data):
                for key in ("started_at", "ended_at", "ts", "timestamp", "time", "start_time", "end_time"):
                    dt = _parse_dt(item.get(key))
                    if dt:
                        t0 = dt if t0 is None else min(t0, dt)
                        t1 = dt if t1 is None else max(t1, dt)

        if (t0 is None or t1 is None) and jsones:
            # Fallback a tiempos de archivo si no hay timestamps en el contenido
            try:
                mtimes = [datetime.fromtimestamp(p.stat().st_mtime) for p in jsones if p.exists()]
                if mtimes:
                    t0 = min(mtimes) if t0 is None else t0
                    t1 = max(mtimes) if t1 is None else t1
            except Exception:
                pass

        if t0 and t1:
            res[nombre] = (t0, t1)
    return res

def reportar_a_jira(
    cfg: dict,
    mapa_yaml: dict,
    nombre_test: str,
    estado_interno: str,
    estado_final: str,
    reasoning: str,
    comentario: str,
    inicio_caso: datetime,
    fin_caso: datetime,
    dir_ejec: Path,
    adjuntar: bool,
    conversation: str,
    destino_yaml: Path,
):
    test_case_key = mapa_yaml.get(nombre_test) or ""
    if not test_case_key:
        jprint(f"Jira: Omitido: test '{nombre_test}' sin test_case_key en YAML.")
        return

    try:
        import yaml
        with open(destino_yaml, 'r', encoding='utf-8') as f:
            doc = yaml.safe_load(f)
        test_cfg = doc.get('tests', {}).get(nombre_test, {})
        steps = test_cfg.get('steps', [])
        expected_results = test_cfg.get('expected_results', [])
        vars_glob = doc.get('vars_glob', {})
        
        def render_template(text, vars_glob):
            try:
                return jinja_env.from_string(text).render(vars_glob=vars_glob)
            except Exception:
                return text
        
        rendered_steps = [render_template(step, vars_glob) for step in steps]
        rendered_expected_results = [render_template(exp, vars_glob) for exp in expected_results]
    except Exception:
        rendered_steps = []
        rendered_expected_results = []

    executed_by = obtener_user_key(cfg["base_url"], cfg["token"], cfg["username"])
    duration_ms = max(0, int((fin_caso - inicio_caso).total_seconds() * 1000))
    status_scaled = "Pass" if estado_final.lower().startswith("pass") else "Fail"

    body = [{
        "status": status_scaled,
        "testCaseKey": test_case_key,
        "environment": cfg["ambiente"],
        "executionTime": duration_ms,
        "executedBy": executed_by or None,
        "scriptResults": [{"index": 0, "status": status_scaled, "comment": estado_final}],
        "comment": comentario or None
    }]

    base = cfg["base_url"]
    test_cycle_enc = quote(cfg["test_cycle"], safe="")
    url = f"{base}/rest/atm/1.0/testrun/{test_cycle_enc}/testresults"

    try:
        data = _atm_post_results(url, cfg["token"], body)
    except urllib.error.HTTPError as e:
        ct = e.headers.get("content-type", "") if e.headers else ""
        ce = e.headers.get("content-encoding", "") if e.headers else ""
        try:
            raw_err = e.read()
        except Exception:
            raw_err = b""
        raw_err = _maybe_decompress(raw_err, ce, ct)
        err_txt = raw_err.decode("utf-8", "replace")
        if e.code == 403 and _is_akamai_html_forbidden(ct, err_txt):
            with_exec = "executedBy" in body[0] and body[0]["executedBy"]
            ok, data = _retry_on_akamai_403(base, cfg["token"], url, body, with_exec)
            if not ok:
                jprint("Jira: Error enviando resultado (tras reintentos).")
                raise
        else:
            raise

    test_result_id = ""
    if isinstance(data, list) and data:
        test_result_id = str(data[0].get("id", "") or "")
    elif isinstance(data, dict):
        test_result_id = str(data.get("id", "") or "")

    jprint(f"Jira: Registrado {nombre_test} -> {estado_final} (TC={test_case_key}) id={test_result_id or '(sin id)'}")

    if test_result_id:
        rutas_adjuntar: list[Path] = []

        traces_root = (dir_ejec / cfg.get("traces_dir", "agenteval_traces")).resolve()
        jsones = _buscar_jsones_de_prueba(traces_root, nombre_test)
        if not jsones:
            jprint(f"Jira: No se hallaron JSON en {traces_root} para '{nombre_test}'")
        rutas_adjuntar.extend(jsones)
        
        # Crear mini-summary para este test
        mini_summary_content = f"""# Test Summary: {nombre_test}

Test Case Key: {test_case_key}
Estado: {estado_final}
Estado JSON: {estado_interno}
Inicio: {inicio_caso.isoformat(timespec='seconds')}
Fin: {fin_caso.isoformat(timespec='seconds')}
Duracion: {max(0, int((fin_caso - inicio_caso).total_seconds() * 1000))} ms

## Steps
"""
        if rendered_steps:
            for i, step in enumerate(rendered_steps, 1):
                mini_summary_content += f"{i}. {step}\n"
        else:
            mini_summary_content += "N/A\n"

        mini_summary_content += "\n## Resultados Esperados\n"
        if rendered_expected_results:
            for i, exp in enumerate(rendered_expected_results, 1):
                mini_summary_content += f"{i}. {exp}\n"
        else:
            mini_summary_content += "N/A\n"

        mini_summary_content += "\n## Conversación\n"
        if conversation:
            lines = conversation.split('\n')
            for line in lines:
                line = line.strip()
                if line.startswith('USER:'):
                    mini_summary_content += f"- [Usuario]: {line[5:].strip()}\n"
                elif line.startswith('AGENT:'):
                    mini_summary_content += f"- [Asistente]:\n {line[6:].strip()}\n"
                elif line:
                    mini_summary_content += f"{line}\n"
        else:
            mini_summary_content += "N/A\n"

        mini_summary_content += f"\n## Resultado\n{estado_final}\n"

        mini_summary_content += f"\n## Razonamiento\n{reasoning or 'N/A'}\n"
        mini_summary_path = dir_ejec / f"{sanear(nombre_test)}_summary.md"
        mini_summary_path.write_text(mini_summary_content, encoding="utf-8")
        rutas_adjuntar.append(mini_summary_path)

        if not rutas_adjuntar:
            jprint("Jira: No se encontraron JSON/summary para adjuntar.")

        for p in rutas_adjuntar:
            try:
                aurl = f"{base}/rest/atm/1.0/testresult/{test_result_id}/attachments"
                try:
                    jira_adjuntar_archivo(aurl, cfg["token"], p)
                    jprint(f"Jira: Adjunto {p.name} OK")
                except urllib.error.HTTPError as e:
                    ct = e.headers.get("content-type", "") if e.headers else ""
                    ce = e.headers.get("content-encoding", "") if e.headers else ""
                    try:
                        raw_err = e.read()
                    except Exception:
                        raw_err = b""
                    raw_err = _maybe_decompress(raw_err, ce, ct)
                    err_txt = raw_err.decode("utf-8", "replace")
                    if e.code == 403 and _is_akamai_html_forbidden(ct, err_txt):
                        https_url = _force_https(aurl)
                        if https_url != aurl:
                            jira_adjuntar_archivo(https_url, cfg["token"], p)
                            jprint(f"Jira: Adjunto {p.name} OK (HTTPS)")
                        else:
                            raise
                    else:
                        raise
            except Exception as e:
                jprint(f"Jira: Error adjuntando {p.name}: {e}")

def derivar_estado_rc(rc: int) -> tuple[str, str]:
    return derivar_estado(rc, RESULT_MAP)

def filtrar_yaml_por_test_case_keys(ruta_in: Path, ruta_out: Path, keys: set[str]) -> bool:
    try:
        import yaml
    except Exception:
        raise RuntimeError("PyYAML es requerido para filtrar por test_case_key.")
    with open(ruta_in, "r", encoding="utf-8") as f:
        doc = yaml.safe_load(f)
    if not isinstance(doc, dict) or "tests" not in doc or not isinstance(doc["tests"], dict):
        return False
    filtrados = {}
    for nombre, cfg in doc["tests"].items():
        if isinstance(cfg, dict):
            tc = (cfg.get("test_case_key") or cfg.get("jira_issue") or "").strip()
            if tc and tc in keys:
                filtrados[nombre] = cfg
    if not filtrados:
        return False
    nuevo = dict(doc)
    nuevo["tests"] = filtrados
    with open(ruta_out, "w", encoding="utf-8") as f:
        yaml.safe_dump(nuevo, f, sort_keys=False, allow_unicode=True)
    return True

def ejecutar_uno(ruta_yaml: Path, args) -> dict:
    nombre = ruta_yaml.stem
    dir_ejec = args.salida_dir / sanear(nombre)
    dir_ejec.mkdir(parents=True, exist_ok=True)

    destino_yaml = dir_ejec / "agenteval.yml"

    if getattr(args, "tc_keys", None):
        ok_filtro = filtrar_yaml_por_test_case_keys(ruta_yaml, destino_yaml, args.tc_keys)
        if not ok_filtro:
            inicio = datetime.now(); fin = datetime.now()
            return {
                "yaml": str(ruta_yaml),
                "dir": str(dir_ejec),
                "rc": 0,
                "seg": (fin - inicio).total_seconds(),
                "estado": "SKIPPED",
                "estado_interno": "UNKNOWN",
            }
    else:
        shutil.copy2(ruta_yaml, destino_yaml)

    ruta_env = (
        Path(args.archivo_env)
        if args.archivo_env
        else (Path(".") / ".env" if (Path(".") / ".env").exists() else None)
    )
    entorno = cargar_env(ruta_env)

    cmd = [sys.executable, "-m", "agenteval", "run"]
    inicio = datetime.now()

    (dir_ejec / "logs").mkdir(exist_ok=True)
    log_out = dir_ejec / "logs" / "stdout.log"
    log_err = dir_ejec / "logs" / "stderr.log"

    try:
        if args.detallado:
            who = subprocess.run(
                ["aws", "sts", "get-caller-identity", "--output", "json"],
                env=entorno, cwd=dir_ejec, text=True, capture_output=True
            )
            print("==> Cuenta AWS Configurada:", who.stdout or who.stderr)

            claves_dbg = ["AWS_PROFILE", "AWS_REGION", "AWS_ACCESS_KEY_ID", "AWS_SESSION_TOKEN"]
            for k in claves_dbg:
                v = entorno.get(k)
                if v and k.endswith("KEY_ID"):
                    v = v[:3] + "***"       
                if v and k.endswith("TOKEN"):
                    v = v[:3] + "***"            
                print(f"==> {k}: {v if v else '(no-set)'}")

            with open(log_out, "w", encoding="utf-8") as out:
                print(f"==> Ejecutando: {' '.join(cmd)}  (cwd={dir_ejec})")
                print(
                    f"==> Perfil: {entorno.get('AWS_PROFILE','(no-set)')}  "
                    f"Región: {entorno.get('AWS_REGION') or entorno.get('AWS_DEFAULT_REGION','(no-set)')}"
                )
                proc = subprocess.Popen(
                    cmd,
                    cwd=dir_ejec,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    env=entorno,
                    text=True,
                )
                for linea in proc.stdout:
                    sys.stdout.write(linea)
                    out.write(linea)
                rc = proc.wait()
            log_err.write_text("", encoding="utf-8")

        else:
            with open(log_out, "w", encoding="utf-8") as out, open(
                log_err, "w", encoding="utf-8"
            ) as err:
                proc = subprocess.run(
                    cmd,
                    cwd=dir_ejec,
                    stdout=out,
                    stderr=err,
                    env=entorno,
                    check=False,
                    text=True,
                )
                rc = proc.returncode

    except FileNotFoundError:
        fin = datetime.now()
        return {
            "yaml": str(ruta_yaml),
            "dir": str(dir_ejec),
            "rc": 127,
            "seg": (fin - inicio).total_seconds(),
            "estado": "ERROR",
            "estado_interno": "UNKNOWN",
        }

    fin = datetime.now()
    estado_interno, estado_final = derivar_estado_rc(rc=rc)

    if rc != 0 and not args.detallado:
        n = max(1, args.lineas_errores)
        print(f"{ANSI_RED}--- Detalle (últimas {n} líneas) para {ruta_yaml.name} ---{ANSI_RESET}")
        print(f"{ANSI_RED}(stdout) {log_out}{ANSI_RESET}")
        for l in leer_tail(log_out, n):
            sys.stdout.write(f"{ANSI_RED}{l}{ANSI_RESET}")
        print(f"{ANSI_RED}(stderr) {log_err}{ANSI_RESET}")
        for l in leer_tail(log_err, n):
            sys.stdout.write(f"{ANSI_RED}{l}{ANSI_RESET}")
        print(f"{ANSI_RED}--- Fin ---{ANSI_RESET}\n")

    ok_jira, cfg_jira, faltan = jira_config(entorno)
    if ok_jira:
        mapa_yaml = cargar_mapa_jira_desde_yaml(destino_yaml)
        if not mapa_yaml:
            jprint("Jira: No se encontraron test_case_key en el YAML.")
        else:
            traces_root = (dir_ejec / cfg_jira.get("traces_dir", "agenteval_traces")).resolve()
            estados_por_test = _extraer_estados_por_test(
                traces_root=traces_root,
                nombres_tests=list(mapa_yaml.keys())
            )
            
            tiempos_por_test = _extraer_tiempos_por_test(
                traces_root=traces_root,
                nombres_tests=list(mapa_yaml.keys()),
            )

            for nombre_test in mapa_yaml.keys():
                est_interno_t, est_final_t, reasoning_t, conversation_t = estados_por_test.get(
                    nombre_test, (estado_interno, estado_final, "", "")
                )
                
                inicio_caso, fin_caso = tiempos_por_test.get(nombre_test, (inicio, fin))

                comentario = comentar_para_jira(
                    nombre_test, destino_yaml, inicio_caso, fin_caso, est_interno_t, est_final_t, reasoning_t
                )
                try:
                    reportar_a_jira(
                        cfg_jira,
                        mapa_yaml,
                        nombre_test,
                        est_interno_t,
                        est_final_t,
                        reasoning_t,
                        comentario,
                        inicio_caso,
                        fin_caso,
                        dir_ejec,
                        cfg_jira["attach_json"],
                        conversation_t,
                        destino_yaml,
                    )
                except Exception as e:
                    jprint(f"Jira: Error enviando resultado: {e}")
    else:
        if any(
            entorno.get(k)
            for k in ["JIRA_BASE_URL", "JIRA_USERNAME", "JIRA_TOKEN", "TEST_CYCLE"]
        ):
            jprint(
                f"Jira: Incompleto, faltan: {', '.join(faltan)}. La ejecución continúa sin actualizar Jira."
            )
        else:
            jprint("Jira: No configurado. La ejecución continúa sin actualizar Jira.")

    return {
        "yaml": str(ruta_yaml),
        "dir": str(dir_ejec),
        "rc": rc,
        "seg": (fin - inicio).total_seconds(),
        "estado": estado_final,
        "estado_interno": estado_interno,
    }

def descubrir_pruebas(dir_pruebas: Path, patrones):
    archivos = []
    for p in patrones:
        archivos.extend(sorted(dir_pruebas.rglob(p)))
    return [a for a in archivos if a.is_file()]

def principal():
    global VERBOSO
    parser = argparse.ArgumentParser(
        description="Ejecuta múltiples YAML de Agent Evaluation con .env opcional y reporte a Jira Zephyr Scale."
    )
    parser.add_argument("--dir-pruebas", default="tests", help="Carpeta con .yml/.yaml")
    parser.add_argument("--archivos", default="*.yml,*.yaml", help="Patrón de archivos")
    parser.add_argument("--dir-salida", default=".agenteval_runs", help="Carpeta de resultados")
    parser.add_argument("-j", "--concurrencia", type=int, default=1, help="Ejecuciones en paralelo (JOBS)")
    parser.add_argument("--detener-al-fallar", action="store_true", help="Detiene al primer fallo")
    parser.add_argument("--detallado", action="store_true", help="Salida detallada")
    parser.add_argument("--lineas-errores", type=int, default=80, help="Líneas de log a mostrar al fallar")
    parser.add_argument("--archivo-env", default=None, help="Ruta a .env")
    parser.add_argument(
        "-t", "--test-case-key",
        default="",
        help="Uno o varios test_case_key separados por comas (p.ej. PROCVB-T1214,PROCVB-T1216)"
    )
    args = parser.parse_args()

    args.tc_keys = {s.strip() for s in args.test_case_key.split(",") if s.strip()}

    VERBOSO = args.detallado  

    dir_pruebas = Path(args.dir_pruebas)
    if not dir_pruebas.exists():
        print(f"ERROR: No existe la carpeta {dir_pruebas}", file=sys.stderr)
        sys.exit(2)

    args.salida_dir = Path(args.dir_salida)
    marca = datetime.now().strftime("%Y%m%d_%H%M%S")
    args.salida_dir = args.salida_dir / marca
    args.salida_dir.mkdir(parents=True, exist_ok=True)
    print(f"Carpeta de esta ejecución: {args.salida_dir}")

    patrones = [p.strip() for p in args.archivos.split(",") if p.strip()]
    archivos = descubrir_pruebas(dir_pruebas, patrones)
    if not archivos:
        print("No se encontraron archivos .yml/.yaml en la carpeta de pruebas.", file=sys.stderr)
        sys.exit(3)

    print(f"Encontrados {len(archivos)} archivo(s). En paralelo: {args.concurrencia}")

    resultados = []

    if args.concurrencia <= 1 or args.detallado:
        for a in archivos:
            r = ejecutar_uno(a, args)
            resultados.append(r)
            linea = f"[{r['estado']}] {r['yaml']} -> {r['dir']}"
            print(linea)
            if args.detener_al_fallar and r["rc"] != 0:
                break
    else:
        with concurrent.futures.ThreadPoolExecutor(max_workers=args.concurrencia) as pool:
            futuros = {pool.submit(ejecutar_uno, a, args): a for a in archivos}
            for fut in concurrent.futures.as_completed(futuros):
                r = fut.result()
                resultados.append(r)
                linea = f"[{r['estado']}] {r['yaml']} -> {r['dir']}"
                print(linea)

    ok = sum(1 for r in resultados if r["rc"] == 0)
    fail = sum(1 for r in resultados if r["rc"] != 0)
    print("\n===== RESUMEN POR ARCHIVO =====")
    for r in sorted(resultados, key=lambda x: x["yaml"]):
        estado = r["estado"]
        if estado.lower().startswith("pass"):
            estado_fmt = f"{ANSI_GREEN}{estado:>10}{ANSI_RESET}"
        elif estado.lower().startswith("fail"):
            estado_fmt = f"{ANSI_RED}{estado:>10}{ANSI_RESET}"
        else:
            estado_fmt = f"{estado:>10}"
        fila = f"{estado_fmt}  {r['seg']:>7.2f}s  {r['yaml']}  -> {r['dir']}"
        print(fila)

    fin_line = f"\nTotal: {len(resultados)} | OK: {ok} | FAILED: {fail}"
    print(fin_line)
    sys.exit(0 if fail == 0 else 1)

if __name__ == "__main__":
    principal()