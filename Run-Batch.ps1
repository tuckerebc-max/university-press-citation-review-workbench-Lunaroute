param(
    [Parameter(Mandatory = $true)][string]$InputFolder,
    [Parameter(Mandatory = $true)][string]$OutputFolder,
    [Parameter(Mandatory = $true)][string]$CaseOwner,
    [string]$Project = 'University Press chapter review',
    [ValidateSet('public', 'unpublished_approved')][string]$Classification = 'unpublished_approved',
    [ValidateSet('baseline', 'incremental', 'full', 'release', 'proof')][string]$Mode = 'baseline',
    [ValidateSet('glm-5.3-background', 'glm-5.3', 'glm-5.3-flash-background', 'glm-5.3-flash')][string]$Model = 'glm-5.3-background',
    [ValidateRange(1, 6)][int]$Concurrency = 3,
    [switch]$NoCrossref,
    [Parameter(Mandatory = $true)][switch]$ApproveLunaRoute
)

$ErrorActionPreference = 'Stop'
$appRoot = $PSScriptRoot
$bundledPython = Join-Path $env:USERPROFILE '.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
$python = if (Test-Path -LiteralPath $bundledPython) { $bundledPython } else { (Get-Command python -ErrorAction Stop).Source }
$savedKey = [Environment]::GetEnvironmentVariable('LUNAROUTE_API_KEY', 'User')
if (-not $env:LUNAROUTE_API_KEY -and $savedKey) { $env:LUNAROUTE_API_KEY = $savedKey }
$env:PYTHONPATH = $appRoot
$arguments = @(
    '-X', 'utf8', '-m', 'upress_workbench.cli',
    '--input', $InputFolder,
    '--output', $OutputFolder,
    '--owner', $CaseOwner,
    '--project', $Project,
    '--classification', $Classification,
    '--mode', $Mode,
    '--model', $Model,
    '--concurrency', [string]$Concurrency,
    '--approve-lunaroute'
)
if ($NoCrossref) { $arguments += '--no-crossref' } else { $arguments += '--crossref' }
& $python @arguments
