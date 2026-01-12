# 1. Carpeta .agenteval_runs más reciente
$runFolder = Get-ChildItem -Directory .agenteval_runs | Sort-Object LastWriteTime | Select-Object -Last 1

if (-not $runFolder) {
    Write-Host "No se encontró ninguna carpeta .agenteval_runs."
    exit 1
}
Write-Host "Utilizando carpeta más reciente: $($runFolder.FullName)"

# 2. Busca el único agenteval_summary.md en sus subdirectorios (puede estar anidado)
$summary = Get-ChildItem -Path "$($runFolder.FullName)\*\agenteval_summary.md" | Sort-Object LastWriteTime | Select-Object -Last 1

if (-not $summary) {
    Write-Host "No se encontró ningún agenteval_summary.md en la carpeta más reciente."
    exit 1
}

# 3. Extrae todos los Conversation ID del summary (varios por archivo)
$lines = Get-Content $summary.FullName
$conv_id_indexes = ($lines | Select-String 'Conversation ID:' ).LineNumber

if (-not $conv_id_indexes) {
    Write-Host "No se encontró ningún Conversation ID en el resumen."
    exit 1
}

foreach ($idx in $conv_id_indexes) {
    $conv_id = $lines[$idx].Trim()
    # Puede que el ID esté en la misma línea o en la siguiente
    if ($conv_id -eq "" -or $conv_id -eq "Conversation ID:") {
        $conv_id = $lines[$idx+1].Trim()
    } else {
        # Si está junto con el label
        $conv_id = $conv_id -replace 'Conversation ID:',''
        $conv_id = $conv_id.Trim()
    }

    if (!$conv_id) {
        Write-Host "Conversation ID vacío en el resumen, lo omito."
        continue
    }

    Write-Host "Ejecutando verificacion para Conversation ID: $conv_id"
    try {
        python verifica_enmascaramiento_logs.py --profile Asistente --region us-east-1 --conversation-id $conv_id --log-group "/aws/lambda/virtual-assistant-orchestration-stg" --fecha (Get-Date -Format yyyy-MM-dd)
    }
    catch {
        Write-Host "Error verificando logs para Conversation ID: $conv_id"
    }
}
