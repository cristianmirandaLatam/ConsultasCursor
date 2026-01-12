# Proyecto agente-evaluador
Para facilitar su uso, ahora puedes con un comando ejecutar todos los `.yml/.yaml` en la carpeta `tests/`. Carga `.env` si existe para facilitar la configuracion de aws (Pendiente).

## Uso (Windows PowerShell/CMD)
```powershell
pip install agent-evaluation
pip install pyyaml #requerido para leer los testcasekey
# Para ejecutar los .yml desde la carpeta tests
python .\agente-evaluador.py 
# Para ejecutar varios .yml en paralelo, ej: 4
python .\agente-evaluador.py -j 4
# con .env en otro directorio 
python .\agente-evaluador.py --archivo-env C:\ruta\mis-credenciales.env
# para ejecutar un yml especifico dentro de carpeta tests
python .\agente-evaluador.py --archivos "mi_prueba.yml"
# para ejecutar los archivos yml dentro de una carpeta específica 
python .\agente-evaluador.py --dir-pruebas tests/pruebasregresion
# Para ejecutar agregando logs de jira y otros
python .\agente-evaluador.py --detallado
```

## .env
Crea `.env` desde el ejemplo y completa valores:
```
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
AWS_SESSION_TOKEN=...
AWS_REGION=us-east-1
AWS_PROFILE=...
```
## JIRA
Para actualizar los resultados en jira debes completar los datos relacionados indicados en el ejemplo `env.txt` 
En el yml cada test debe tener asociado su id de jira.
```
test_case_key: "PROCVB-T1155"
```

Ejemplo:
```
tests:
  Cambio_Vol_Motivo_Grave:
    steps:
      - "El usuario indica que necesita cambiar su vuelo, menciona que no puede viajar porque se encuentra hospitalizado."
    expected_results:
      - "El agente le indica que deberá contar con documentación asociada y será transferido con un ejecutivo para ayudarlo en su solicitud."
    max_turns: 3
    test_case_key: "PROCVB-T1155"
```