import boto3
import re
import sys
import os
import argparse
from datetime import datetime
from dateutil import parser as date_parser

# === Colores ANSI para resaltar ===
YELLOW = '\033[93m'
RED = '\033[91m'
RESET = '\033[0m'

# Regex enmascarado/tarjeta
enmascarado_regex = re.compile(r'\*{4,}\d{4}')
tarjeta_regex = re.compile(
    r'\b(?:4[0-9]{12}(?:[0-9]{3})?|'      # Visa
    r'5[1-5][0-9]{14}|'                   # MasterCard
    r'3[47][0-9]{13}|'                    # American Express
    r'3(?:0[0-5]|[68][0-9])[0-9]{11}|'    # Diners Club
    r'6(?:011|5[0-9]{2})[0-9]{12}|'       # Discover
    r'(?:2131|1800|35\d{3})\d{11})\b'
)

def luhn_checksum(card_number):
    card_number = re.sub(r"\D", "", card_number)
    def digits_of(n): return [int(d) for d in n]
    digits = digits_of(card_number)
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    checksum = sum(odd_digits)
    for d in even_digits:
        checksum += sum(digits_of(str(d * 2)))
    return checksum % 10

def es_tarjeta_valida(card_number):
    n = re.sub(r"\D", "", card_number)
    if not 13 <= len(n) <= 19:
        return False
    return luhn_checksum(n) == 0

def streams_mas_cercanos_por_fecha(streams, fecha_str, cantidad=3):
    try:
        fecha = date_parser.parse(fecha_str)
    except Exception:
        print("Fecha no válida. Usa formato YYYY-MM-DD o YYYY-MM-DDTHH:MM")
        sys.exit(2)
    def stream_datetime(s):
        parts = s['logStreamName'].split('/')
        try:
            return datetime(int(parts[0]), int(parts[1]), int(parts[2]))
        except Exception:
            last_ts = s.get('lastEventTimestamp')
            if last_ts:
                return datetime.utcfromtimestamp(last_ts/1000)
            else:
                return datetime.min
    streams = sorted(streams, key=lambda s: abs((stream_datetime(s)-fecha).total_seconds()))
    return streams[:cantidad]

def buscar_por_conversation_id(client, log_group, conversation_id, fecha_str=None, streams_cercanos=3, verbose=False):
    print(f"Buscando Conversation ID '{conversation_id}' en log group: {log_group}")
    streams = []
    kwargs = dict(logGroupName=log_group, orderBy='LastEventTime', descending=True)
    while True:
        resp = client.describe_log_streams(**kwargs)
        streams += resp['logStreams']
        if 'nextToken' in resp:
            kwargs['nextToken'] = resp['nextToken']
        else:
            break

    # Si hay fecha filtra los N más cercanos, sino usa todos
    if fecha_str:
        streams = streams_mas_cercanos_por_fecha(streams, fecha_str, cantidad=streams_cercanos)
        print(f"Filtrando {len(streams)} stream(s) más cercanos a la fecha indicada...")

    resultado_por_stream = []
    total_tarjetas = 0
    total_enmascaradas = 0
    tarjetas_vistas = set()

    for stream in streams:
        stream_name = stream['logStreamName']
        response = client.get_log_events(
            logGroupName=log_group,
            logStreamName=stream_name,
            startFromHead=True
        )

        mensajes_con_conversation = []
        tarjetas_en_claro = []
        tarjetas_enmascaradas = []

        cc_regex = tarjeta_regex
        enmasc_regex = enmascarado_regex

        for event in response['events']:
            mensaje = event['message']
            if conversation_id in mensaje:
                mensajes_con_conversation.append(mensaje)
                posibles_tarjetas = cc_regex.findall(mensaje)
                nuevas_tarjetas = [
                    t for t in posibles_tarjetas
                    if t not in tarjetas_vistas and es_tarjeta_valida(t)
                ]
                for t in nuevas_tarjetas:
                    tarjetas_vistas.add(t)
                if nuevas_tarjetas:
                    tarjetas_en_claro.extend(nuevas_tarjetas)
                elif enmasc_regex.search(mensaje):
                    tarjetas_enmascaradas.append(mensaje)

        if mensajes_con_conversation:
            resultado_por_stream.append({
                'stream_name': stream_name,
                'mensajes': mensajes_con_conversation,
                'tarjetas_claro': tarjetas_en_claro,
                'enmascarados': tarjetas_enmascaradas
            })
            total_tarjetas += len(tarjetas_en_claro)
            total_enmascaradas += len(tarjetas_enmascaradas)

    if not resultado_por_stream:
        print(f"NO se encontró el Conversation ID '{conversation_id}' en los streams revisados.")
        sys.exit(0)

    print("="*70)
    print(f"Conversation ID '{conversation_id}' hallado en {len(resultado_por_stream)} log stream(s) de los {len(streams)} revisados.")
    print("="*70)

    for rs in resultado_por_stream:
        print(f"\n==== Stream: {rs['stream_name']}")
        print(f"Mensajes encontrados en este stream: {len(rs['mensajes'])}")
        if rs['tarjetas_claro']:
            print(f"{RED}Tarjetas EN CLARO detectadas ({len(rs['tarjetas_claro'])} únicas): {', '.join(rs['tarjetas_claro'])}{RESET}")
            for m in rs['mensajes']:
                if any(t in m for t in rs['tarjetas_claro']):
                    out = m.replace('\n',' ').replace('\r',' ')
                    out = tarjeta_regex.sub(lambda m: f"{RED}{m.group(0)}{RESET}", out)
                    print('-'*30)
                    print(out)
        else:
            print("No se encontraron tarjetas en claro en este stream para este ConversationId.")

        if rs['enmascarados']:
            print(f"{YELLOW}Mensajes enmascarados (todos):{RESET}")
            print(f"  {RED}Tarjeta en claro     {YELLOW}Tarjeta enmascarada{RESET}")
            for i, msg in enumerate(rs['enmascarados'], 1):
                raw = msg.replace('\n',' ').replace('\r',' ')
                # Resalta posibles tarjetas en claro antes de enmascaradas (¡importante por sobreposición!)
                raw = tarjeta_regex.sub(lambda m: f"{RED}{m.group(0)}{RESET}", raw)
                raw = enmascarado_regex.sub(lambda m: f"{YELLOW}{m.group(0)}{RESET}", raw)
                print(f"[{i:03}] {raw}")


    print("="*70)
    print(f"RESUMEN:")
    print(f"Streams revisados: {len(streams)}")
    print(f"Streams con Conversation ID: {len(resultado_por_stream)}")
    print(f"Total tarjetas en claro (únicas): {total_tarjetas}")
    print(f"Total mensajes enmascarados: {total_enmascaradas}")

# El resto de funciones (buscar_tarjetas_en_logs, etc.) no necesitan cambios para el resaltado
def buscar_tarjetas_en_logs(client, log_group, log_stream):
    cc_regex = tarjeta_regex
    enmascarado_regex_local = enmascarado_regex
    tarjetas_vistas = set()
    response = client.get_log_events(
        logGroupName=log_group,
        logStreamName=log_stream,
        startFromHead=True
    )
    tarjetas_en_claro = []
    tarjetas_enmascaradas = []

    for event in response['events']:
        mensaje = event['message']
        posibles_tarjetas = cc_regex.findall(mensaje)
        nuevas_tarjetas = [
            t for t in posibles_tarjetas
            if t not in tarjetas_vistas and es_tarjeta_valida(t)
        ]
        for t in nuevas_tarjetas:
            tarjetas_vistas.add(t)
        if nuevas_tarjetas:
            tarjetas_en_claro.append((mensaje, nuevas_tarjetas))
        elif enmascarado_regex_local.search(mensaje):
            tarjetas_enmascaradas.append(mensaje)

    if tarjetas_en_claro:
        print(f"{RED}¡ATENCIÓN! Se encontraron posibles tarjetas en claro en los logs (solo imprime cada tarjeta la primera vez):{RESET}")
        for m, lista_tarjetas in tarjetas_en_claro:
            out = m.replace('\n',' ').replace('\r',' ')
            out = tarjeta_regex.sub(lambda m: f"{RED}{m.group(0)}{RESET}", out)
            print("Mensaje:", out)
            print("Tarjeta(s) encontrada(s):", ', '.join(lista_tarjetas))
            print("-" * 40)
        sys.exit(1)
    else:
        print("No se encontraron tarjetas en claro. Solo enmascaradas o ninguna.")
        if tarjetas_enmascaradas:
            print(f"{YELLOW}Ejemplos enmascarados:{RESET}")
            for i, m in enumerate(tarjetas_enmascaradas):
                out = m.replace('\n',' ').replace('\r',' ')
                out = enmascarado_regex_local.sub(lambda m: f"{YELLOW}{m.group(0)}{RESET}", out)
                print(f"[{i+1:03}] {out.strip()}")
        sys.exit(0)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Buscar tarjetas en logs de CloudWatch (Lambda)."
    )
    parser.add_argument("--profile", type=str, help="Perfil AWS (default: Asistente, o variable AWS_PROFILE)")
    parser.add_argument("--region", type=str, help="Región AWS (default: us-east-2, o variable AWS_REGION)")
    parser.add_argument("--log-group", type=str, required=True, help="Log Group")
    parser.add_argument("--log-stream", type=str, help="Log Stream (opcional, prioriza esto si se entrega)")
    parser.add_argument("--fecha", type=str, help="YYYY-MM-DD o YYYY-MM-DDTHH:MM. Limita búsqueda a streams cercanos, o para análisis individual.")
    parser.add_argument("--conversation-id", type=str, help="Busca en todos los streams donde aparezca este ConversationId. Si das --fecha, busca sólo en los N más cercanos (combina con --streams-cercanos).")
    parser.add_argument("--streams-cercanos", type=int, default=3, help="Cuántos streams revisar alrededor de la fecha si das --fecha y --conversation-id")
    parser.add_argument("--verbose", action="store_true", help="Muestra información de depuración adicional.")
    parser.add_argument("extra", nargs="*", help=argparse.SUPPRESS)
    parser.epilog = (
    "Ejemplos:\n"
    " python verifica_enmascaramiento_logs.py --profile Asistente --region us-east-1 --log-group \"/aws/lambda/Felipe_prueba_router\" --fecha 2025-10-29\n"
    " python verifica_enmascaramiento_logs.py --profile Asistente --region us-east-1 --log-group \"/aws/lambda/Felipe_prueba_router\" --conversation-id Prueba4\n"
    " python verifica_enmascaramiento_logs.py --profile Asistente --region us-east-1 --log-group \"/aws/lambda/Felipe_prueba_router\" --conversation-id Prueba4 --fecha 2025-10-29 --streams-cercanos 5\n"
    )

    args = parser.parse_args()
    profile = args.profile if args.profile else os.getenv('AWS_PROFILE', 'Asistente')
    region = args.region if args.region else os.getenv('AWS_REGION', 'us-east-2')
    session = boto3.Session(profile_name=profile)
    client = session.client('logs', region_name=region)

    if args.conversation_id:
        buscar_por_conversation_id(
            client=client,
            log_group=args.log_group,
            conversation_id=args.conversation_id,
            fecha_str=args.fecha,
            streams_cercanos=args.streams_cercanos,
            verbose=args.verbose
        )
    elif args.log_stream:
        print(f"Usando log_stream entregado: {args.log_stream}")
        buscar_tarjetas_en_logs(client, args.log_group, args.log_stream)
    else:
        # Si solo das fecha, busca el stream más cercano y lo analiza.
        streams = []
        kwargs = dict(logGroupName=args.log_group, orderBy='LastEventTime', descending=True)
        while True:
            resp = client.describe_log_streams(**kwargs)
            streams += resp['logStreams']
            if 'nextToken' in resp:
                kwargs['nextToken'] = resp['nextToken']
            else:
                break
        if args.fecha:
            streams = streams_mas_cercanos_por_fecha(streams, args.fecha, cantidad=1)
            if not streams:
                print("No se encontró log stream cercano a esa fecha.")
                sys.exit(2)
            stream_name = streams[0]['logStreamName']
            print(f"Log stream más cercano por fecha: {stream_name}")
        else:
            stream_name = streams[0]['logStreamName']
            print(f"Usando log stream más reciente: {stream_name}")
        buscar_tarjetas_en_logs(client, args.log_group, stream_name)
