$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
$env:BLENDER_USER_RESOURCES = Join-Path $root '.blender-user'
$env:BLENDER_MCP_DISABLE_TELEMETRY = '1'
$env:BLENDERMCP_NO_UPDATE_CHECK = '1'
& 'C:\Program Files\Blender Foundation\Blender 5.2\blender.exe' --factory-startup --disable-autoexec --python-exit-code 1 --python (Join-Path $PSScriptRoot 'blender_bootstrap.py')
if ($LASTEXITCODE -ne 0) {
    throw "Blender exited with code $LASTEXITCODE"
}
