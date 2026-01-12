# Ejecuta el test (ajusta los parámetros si quieres otros filtros)
python .\agente-evaluador.py --dir-pruebas tests/"Sprint 4"/ -t "PACONW-T435"

# Busca el archivo agenteval_summary más reciente
$summary = Get-ChildItem -Path .agenteval_runs\*\*\agenteval_summary.md | Sort-Object LastWriteTime | Select-Object -Last 1

if (-not $summary) {
    Write-Host "No se encontró ningún agenteval_summary.md. ¿Ejecutaste una prueba válida?"
    exit 1
}

# Extrae el Conversation ID (línea siguiente tras "Conversation ID:")
$lines = Get-Content $summary.FullName
$idx = ($lines | Select-String 'Conversation ID:' ).LineNumber
if (-not $idx) {
    Write-Host "No se encontró Conversation ID en el resumen."
    exit 1
}
$conv_id = $lines[$idx].Trim()
if ($conv_id -eq "") { $conv_id = $lines[$idx+1].Trim() }
Write-Host "Conversation ID extraído: $conv_id"

# Ejecuta la verificación de logs usando el Conversation ID
python verifica_enmascaramiento_logs.py --profile Asistente --region us-east-1 --conversation-id $conv_id --log-group "/aws/lambda/virtual-assistant-orchestration-stg" --fecha (Get-Date -Format yyyy-MM-dd)
