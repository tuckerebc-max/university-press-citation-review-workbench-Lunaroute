param(
    [ValidateRange(1024, 65535)]
    [int]$Port = 8765,
    [switch]$NoBrowser
)

$ErrorActionPreference = 'Stop'
$appRoot = $PSScriptRoot
$bundledPython = Join-Path $env:USERPROFILE '.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
$python = if (Test-Path -LiteralPath $bundledPython) { $bundledPython } else { (Get-Command python -ErrorAction Stop).Source }
$savedKey = [Environment]::GetEnvironmentVariable('LUNAROUTE_API_KEY', 'User')
if (-not $env:LUNAROUTE_API_KEY -and $savedKey) {
    $env:LUNAROUTE_API_KEY = $savedKey
}
$env:PYTHONPATH = $appRoot
$arguments = @('-X', 'utf8', '-m', 'upress_workbench.server', '--port', [string]$Port)
if ($NoBrowser) { $arguments += '--no-browser' }
& $python @arguments
