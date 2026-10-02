/* Simulador de práctica CT-GenAI. */
(function () {
  var PLAN = [
    ["1.1.1", "K1", 1, 1],
    ["1.1.2", "K2", 1, 1],
    ["1.1.2", "K2", 1, 1],
    ["1.1.3", "K2", 1, 1],
    ["1.1.4", "K2", 1, 1],
    ["1.2.1", "K2", 1, 2],
    ["1.2.2", "K2", 1, 1],
    ["2.1.1", "K2", 1, 1],
    ["2.1.1", "K2", 1, 1],
    ["2.1.2", "K2", 1, 1],
    ["2.1.3", "K2", 1, 1],
    ["2.2.1", "K3", 2, 1],
    ["2.2.2", "K3", 2, 1],
    ["2.2.3", "K3", 2, 1],
    ["2.2.4", "K3", 2, 1],
    ["2.2.5", "K3", 2, 1],
    ["2.3.1", "K2", 1, 1],
    ["2.3.2", "K2", 1, 1],
    ["3.1.1", "K1", 1, 1],
    ["3.1.2", "K3", 2, 1],
    ["3.1.3", "K2", 1, 1],
    ["3.1.4", "K1", 1, 1],
    ["3.2.1", "K2", 1, 1],
    ["3.2.2", "K2", 1, 1],
    ["3.2.2", "K2", 1, 1],
    ["3.2.3", "K2", 1, 1],
    ["3.3.1", "K2", 1, 1],
    ["3.4.1", "K1", 1, 2],
    ["4.1.1", "K2", 1, 1],
    ["4.1.2", "K2", 1, 1],
    ["4.1.3", "K2", 1, 1],
    ["4.2.1", "K2", 1, 1],
    ["4.2.2", "K2", 1, 1],
    ["5.1.1", "K1", 1, 1],
    ["5.1.2", "K2", 1, 1],
    ["5.1.3", "K2", 1, 1],
    ["5.1.4", "K1", 1, 1],
    ["5.2.1", "K2", 1, 1],
    ["5.2.2", "K1", 1, 1],
    ["5.2.3", "K1", 1, 1]
  ];

  var CAPITULOS = {
    "1": "Introducción a la IA generativa",
    "2": "Ingeniería de prompts",
    "3": "Gestión de riesgos",
    "4": "Infraestructura de prueba impulsada por LLM",
    "5": "Despliegue e integración"
  };

  var TOTAL_PUNTOS = 46;
  var CORTE = 30;
  var CLAVE_HIST = "ctgenai-historial";
  var CLAVE_SESION = "ctgenai-sesion";

  var estado = null;
  var reloj = null;

  function barajar(lista) {
    var a = lista.slice();
    for (var i = a.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1));
      var t = a[i]; a[i] = a[j]; a[j] = t;
    }
    return a;
  }

  function porLo(lo) {
    return window.BANCO.filter(function (p) { return p.lo === lo; });
  }

  function armarExamen() {
    var usados = {};
    var preguntas = PLAN.map(function (slot) {
      var lo = slot[0];
      var candidatas = porLo(lo).filter(function (p) { return !usados[p._id]; });
      if (!candidatas.length) candidatas = porLo(lo);
      var elegida = barajar(candidatas)[0];
      usados[elegida._id] = true;
      var orden = barajar(elegida.opciones.map(function (_, i) { return i; }));
      var correctas = elegida.correctas.map(function (i) { return orden.indexOf(i); }).sort(function (a, b) { return a - b; });
      return {
        lo: elegida.lo,
        k: elegida.k,
        puntos: elegida.puntos,
        elegir: elegida.elegir,
        enunciado: elegida.enunciado,
        opciones: orden.map(function (i) { return elegida.opciones[i]; }),
        correctas: correctas,
        porque: elegida.porque
      };
    });
    return barajar(preguntas);
  }

  function letra(i) { return String.fromCharCode(97 + i); }

  function mismoConjunto(a, b) {
    if (!a || a.length !== b.length) return false;
    var x = a.slice().sort(function (m, n) { return m - n; });
    var y = b.slice().sort(function (m, n) { return m - n; });
    for (var i = 0; i < x.length; i++) if (x[i] !== y[i]) return false;
    return true;
  }

  function puntuar(preguntas, respuestas) {
    var puntos = 0;
    var detalle = preguntas.map(function (p, i) {
      var marca = respuestas[i] || [];
      var bien = mismoConjunto(marca, p.correctas);
      if (bien) puntos += p.puntos;
      return { bien: bien, marca: marca };
    });
    return { puntos: puntos, detalle: detalle, aprobado: puntos >= CORTE };
  }

  function guardarHistorial(item) {
    var h = leerHistorial();
    h.unshift(item);
    localStorage.setItem(CLAVE_HIST, JSON.stringify(h.slice(0, 20)));
  }

  function leerHistorial() {
    try { return JSON.parse(localStorage.getItem(CLAVE_HIST)) || []; }
    catch (e) { return []; }
  }

  function persistir() {
    if (!estado) return;
    sessionStorage.setItem(CLAVE_SESION, JSON.stringify(estado));
  }

  function formatear(seg) {
    seg = Math.max(0, seg);
    var m = Math.floor(seg / 60);
    var s = seg % 60;
    return (m < 10 ? "0" : "") + m + ":" + (s < 10 ? "0" : "") + s;
  }

  function restantes() {
    return Math.round((estado.fin - Date.now()) / 1000);
  }

  function el(html) {
    var n = document.createElement("div");
    n.innerHTML = html.trim();
    return n.firstChild;
  }

  function escapar(t) {
    return String(t)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;");
  }

  function mostrar(nodo) {
    var raiz = document.getElementById("app");
    raiz.innerHTML = "";
    raiz.appendChild(nodo);
  }

  function pararReloj() {
    if (reloj) { clearInterval(reloj); reloj = null; }
  }

  /* ---------- pantallas ---------- */
  function pantallaInicio() {
    pararReloj();
    estado = null;
    sessionStorage.removeItem(CLAVE_SESION);
    var hist = leerHistorial();
    var filas = hist.length
      ? hist.map(function (h) {
          return "<li><span>" + escapar(h.fecha) + "</span><strong>" + h.puntos + "/" + TOTAL_PUNTOS + "</strong><em class='" + (h.aprobado ? "ok" : "mal") + "'>" + (h.aprobado ? "Aprobado" : "No aprobado") + "</em></li>";
        }).join("")
      : "<li class='vacio'>Todavía no hay intentos en este navegador.</li>";

    var nodo = el(
      "<section class='panel inicio'>" +
        "<p class='kicker'>Práctica · ISTQB CT-GenAI</p>" +
        "<h1>Simulador de examen</h1>" +
        "<p class='lead'>Cada intento arma un examen nuevo: una formulación distinta por objetivo de aprendizaje, con las opciones y el orden barajados. Las preguntas son originales, escritas a partir del programa de estudios y del estilo del examen de muestra. No son los ítems oficiales.</p>" +
        "<ul class='reglas'>" +
          "<li><strong>40 preguntas</strong> y <strong>46 puntos</strong>, como el examen.</li>" +
          "<li>Se aprueba con <strong>30 puntos</strong> (65&nbsp;%).</li>" +
          "<li><strong>60 minutos</strong>. Quien no rinde en su lengua materna dispone de 75.</li>" +
          "<li>Seis preguntas de nivel K3 valen 2 puntos. El resto vale 1.</li>" +
          "<li>En las de «elija dos», el punto cuenta solo si las dos opciones son las correctas.</li>" +
        "</ul>" +
        "<label class='check'><input type='checkbox' id='extra'> Añadir el 25&nbsp;% de tiempo (75 minutos)</label>" +
        "<div class='acciones'><button class='primario' id='empezar' type='button'>Empezar simulacro</button></div>" +
        "<h2>Intentos anteriores</h2>" +
        "<ul class='historial'>" + filas + "</ul>" +
      "</section>"
    );
    mostrar(nodo);
    nodo.querySelector("#empezar").addEventListener("click", function () {
      var extra = nodo.querySelector("#extra").checked;
      empezar(extra ? 75 : 60);
    });
  }

  function empezar(minutos) {
    var preguntas = armarExamen();
    estado = {
      preguntas: preguntas,
      respuestas: preguntas.map(function () { return []; }),
      marcas: preguntas.map(function () { return false; }),
      indice: 0,
      fin: Date.now() + minutos * 60 * 1000,
      minutos: minutos,
      cerrado: false
    };
    persistir();
    pintarExamen();
  }

  function pintarExamen() {
    var p = estado.preguntas[estado.indice];
    var marca = estado.respuestas[estado.indice];
    var tipo = p.elegir === 2 ? "checkbox" : "radio";
    var aviso = p.elegir === 2 ? "Elija DOS opciones." : "Elija UNA opción.";
    var opciones = p.opciones.map(function (texto, i) {
      var activo = marca.indexOf(i) !== -1;
      return "<label class='opcion" + (activo ? " activa" : "") + "'>" +
        "<input type='" + tipo + "' name='op' value='" + i + "'" + (activo ? " checked" : "") + ">" +
        "<span class='letra'>" + letra(i) + "</span><span>" + escapar(texto) + "</span></label>";
    }).join("");

    var celdas = estado.preguntas.map(function (_, i) {
      var cls = (i === estado.indice ? "actual" : "") + (estado.respuestas[i].length ? " hecha" : "") + (estado.marcas[i] ? " bandera" : "");
      return "<button type='button' class='celda " + cls + "' data-i='" + i + "'>" + (i + 1) + "</button>";
    }).join("");

    var cap = CAPITULOS[p.lo.charAt(0)];
    var nodo = el(
      "<section class='examen'>" +
        "<header class='barra'>" +
          "<div><strong>Simulacro CT-GenAI</strong><span class='meta'>Pregunta " + (estado.indice + 1) + " de 40 · " + p.puntos + (p.puntos === 1 ? " punto" : " puntos") + " · " + p.k + "</span></div>" +
          "<div class='tiempo' id='tiempo'>" + formatear(restantes()) + "</div>" +
        "</header>" +
        "<div class='cuerpo'>" +
          "<nav class='mapa' aria-label='Preguntas'>" + celdas + "</nav>" +
          "<article class='pregunta'>" +
            "<p class='lo'>" + escapar(cap) + " · GenAI-" + escapar(p.lo) + "</p>" +
            "<h1>" + escapar(p.enunciado) + "</h1>" +
            "<p class='aviso'>" + aviso + "</p>" +
            "<div class='opciones'>" + opciones + "</div>" +
            "<footer class='pie-pregunta'>" +
              "<label class='check'><input type='checkbox' id='bandera'" + (estado.marcas[estado.indice] ? " checked" : "") + "> Marcar para revisar</label>" +
              "<div class='acciones'>" +
                "<button type='button' id='prev' " + (estado.indice === 0 ? "disabled" : "") + ">Anterior</button>" +
                (estado.indice < 39
                  ? "<button type='button' class='primario' id='next'>Siguiente</button>"
                  : "<button type='button' class='primario' id='cerrar'>Entregar examen</button>") +
              "</div>" +
            "</footer>" +
          "</article>" +
        "</div>" +
      "</section>"
    );
    mostrar(nodo);

    nodo.querySelectorAll(".celda").forEach(function (b) {
      b.addEventListener("click", function () {
        estado.indice = Number(b.getAttribute("data-i"));
        persistir();
        pintarExamen();
      });
    });
    nodo.querySelectorAll("input[name='op']").forEach(function (input) {
      input.addEventListener("change", function () {
        leerMarcas(nodo, p.elegir);
      });
    });
    nodo.querySelector("#bandera").addEventListener("change", function (e) {
      estado.marcas[estado.indice] = e.target.checked;
      persistir();
      pintarExamen();
    });
    var prev = nodo.querySelector("#prev");
    if (prev) prev.addEventListener("click", function () { mover(-1); });
    var next = nodo.querySelector("#next");
    if (next) next.addEventListener("click", function () { mover(1); });
    var cerrar = nodo.querySelector("#cerrar");
    if (cerrar) cerrar.addEventListener("click", function () { confirmarCierre(); });

    arrancarReloj();
  }

  function leerMarcas(nodo, elegir) {
    var previas = (estado.respuestas[estado.indice] || []).slice();
    var inputs = Array.prototype.slice.call(nodo.querySelectorAll("input[name='op']"));
    var marks = [];
    inputs.forEach(function (input, idx) {
      if (input.checked) marks.push(idx);
    });
    if (elegir === 2 && marks.length > 2) {
      var quitar = previas.length ? previas[0] : marks[0];
      inputs[quitar].checked = false;
      marks = marks.filter(function (i) { return i !== quitar; });
    }
    estado.respuestas[estado.indice] = marks;
    persistir();
    nodo.querySelectorAll(".opcion").forEach(function (lab) {
      lab.classList.toggle("activa", lab.querySelector("input").checked);
    });
    var celda = nodo.querySelector('.celda[data-i="' + estado.indice + '"]');
    if (celda) celda.classList.toggle("hecha", marks.length > 0);
  }

  function mover(delta) {
    estado.indice = Math.min(39, Math.max(0, estado.indice + delta));
    persistir();
    pintarExamen();
  }

  function arrancarReloj() {
    pararReloj();
    reloj = setInterval(function () {
      var caja = document.getElementById("tiempo");
      var seg = restantes();
      if (caja) {
        caja.textContent = formatear(seg);
        caja.classList.toggle("urgente", seg < 60);
      }
      if (seg <= 0) {
        pararReloj();
        cerrarExamen(true);
      }
    }, 250);
  }

  function confirmarCierre() {
    var vacias = estado.respuestas.filter(function (r) { return !r.length; }).length;
    var texto = vacias
      ? "Quedan " + vacias + " preguntas sin responder. ¿Entregar el examen igualmente?"
      : "¿Entregar el examen y ver el resultado?";
    if (window.confirm(texto)) cerrarExamen(false);
  }

  function cerrarExamen(porTiempo) {
    if (!estado || estado.cerrado) return;
    estado.cerrado = true;
    pararReloj();
    var resultado = puntuar(estado.preguntas, estado.respuestas);
    guardarHistorial({
      fecha: new Date().toLocaleString("es"),
      puntos: resultado.puntos,
      aprobado: resultado.aprobado,
      porTiempo: porTiempo
    });
    sessionStorage.removeItem(CLAVE_SESION);
    pintarResultado(resultado, porTiempo);
  }

  function pintarResultado(resultado, porTiempo) {
    var porCap = {};
    estado.preguntas.forEach(function (p, i) {
      var c = p.lo.charAt(0);
      if (!porCap[c]) porCap[c] = { bien: 0, puntos: 0, max: 0 };
      porCap[c].max += p.puntos;
      if (resultado.detalle[i].bien) {
        porCap[c].bien += 1;
        porCap[c].puntos += p.puntos;
      }
    });
    var filasCap = Object.keys(porCap).sort().map(function (c) {
      var x = porCap[c];
      return "<li><span>Capítulo " + c + ". " + escapar(CAPITULOS[c]) + "</span><strong>" + x.puntos + " de " + x.max + " puntos</strong></li>";
    }).join("");

    var repaso = estado.preguntas.map(function (p, i) {
      var d = resultado.detalle[i];
      var suyas = d.marca.length ? d.marca.map(letra).join(", ") : "sin respuesta";
      var buenas = p.correctas.map(letra).join(", ");
      var ops = p.opciones.map(function (t, k) {
        var cls = p.correctas.indexOf(k) !== -1 ? "buena" : (d.marca.indexOf(k) !== -1 ? "mala" : "");
        return "<li class='" + cls + "'><span class='letra'>" + letra(k) + "</span> " + escapar(t) + "</li>";
      }).join("");
      return "<details" + (d.bien ? "" : " open") + ">" +
        "<summary><span class='pill " + (d.bien ? "ok" : "mal") + "'>" + (d.bien ? "Bien" : "Mal") + "</span> " +
        (i + 1) + ". GenAI-" + escapar(p.lo) + " · " + p.k + " · " + p.puntos + " pt · su respuesta: " + suyas + " · correcta: " + buenas + "</summary>" +
        "<p>" + escapar(p.enunciado) + "</p><ol class='repaso-ops'>" + ops + "</ol><p class='porque'><strong>Por qué. </strong>" + escapar(p.porque) + "</p></details>";
    }).join("");

    var nodo = el(
      "<section class='panel resultado'>" +
        "<p class='kicker'>" + (porTiempo ? "El tiempo se agotó" : "Examen entregado") + "</p>" +
        "<h1 class='" + (resultado.aprobado ? "ok" : "mal") + "'>" + (resultado.aprobado ? "Aprobado" : "No aprobado") + "</h1>" +
        "<p class='nota'>" + resultado.puntos + " / " + TOTAL_PUNTOS + " puntos · el corte es " + CORTE + "</p>" +
        "<h2>Por capítulo</h2><ul class='historial'>" + filasCap + "</ul>" +
        "<div class='acciones'><button class='primario' id='otro' type='button'>Nuevo simulacro</button><button id='inicio' type='button'>Volver al inicio</button></div>" +
        "<h2>Repaso</h2>" + repaso +
      "</section>"
    );
    mostrar(nodo);
    nodo.querySelector("#otro").addEventListener("click", function () { empezar(estado.minutos); });
    nodo.querySelector("#inicio").addEventListener("click", pantallaInicio);
    window.scrollTo(0, 0);
  }

  function restaurar() {
    var crudo = sessionStorage.getItem(CLAVE_SESION);
    if (!crudo) return false;
    try { estado = JSON.parse(crudo); }
    catch (e) { return false; }
    if (!estado || estado.cerrado || !estado.preguntas) return false;
    if (restantes() <= 0) { cerrarExamen(true); return true; }
    pintarExamen();
    return true;
  }

  document.addEventListener("DOMContentLoaded", function () {
    window.BANCO.forEach(function (p, i) { p._id = p.lo + "#" + i; });
    if (!restaurar()) pantallaInicio();
  });

  window.CTGenAI = { PLAN: PLAN, armarExamen: armarExamen, puntuar: puntuar, TOTAL_PUNTOS: TOTAL_PUNTOS, CORTE: CORTE };
})();
