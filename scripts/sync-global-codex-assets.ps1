[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'

$repoRoot = Split-Path -Parent $PSScriptRoot
$globalSkillRoot = Join-Path $env:USERPROFILE '.agents\skills'
$globalAgentRoot = Join-Path $env:USERPROFILE '.codex\agents'
$backupRoot = Join-Path $env:USERPROFILE ('.codex\backups\restaurant-council-' + (Get-Date -Format 'yyyyMMdd-HHmmss'))

$skillNames = @(
    'restaurant-research-librarian',
    'restaurant-commercial-council',
    'restaurant-commercial-deliverables'
)

$agentNames = @(
    'business-builder.toml',
    'chairman.toml',
    'competitor-alternatives-analyst.toml',
    'devils-advocate.toml',
    'evidence-auditor.toml',
    'market-economics-analyst.toml',
    'research-librarian.toml',
    'restaurant-operator.toml',
    'restaurant-owner.toml'
)

New-Item -ItemType Directory -Force $globalSkillRoot, $globalAgentRoot | Out-Null

function Backup-ExistingItem {
    param(
        [Parameter(Mandatory)]
        [string]$Path,
        [Parameter(Mandatory)]
        [string]$Category
    )

    if (-not (Test-Path -LiteralPath $Path)) {
        return
    }

    $categoryRoot = Join-Path $backupRoot $Category
    New-Item -ItemType Directory -Force $categoryRoot | Out-Null
    Copy-Item -LiteralPath $Path -Destination $categoryRoot -Recurse -Force
    Remove-Item -LiteralPath $Path -Recurse -Force
}

foreach ($name in $skillNames) {
    $source = Join-Path $repoRoot ".agents\skills\$name"
    $destination = Join-Path $globalSkillRoot $name
    Backup-ExistingItem -Path $destination -Category 'skills'
    Copy-Item -LiteralPath $source -Destination $destination -Recurse -Force
}

foreach ($name in $agentNames) {
    $source = Join-Path $repoRoot ".codex\agents\$name"
    $destination = Join-Path $globalAgentRoot $name
    Backup-ExistingItem -Path $destination -Category 'agents'
    Copy-Item -LiteralPath $source -Destination $destination -Force
}

Write-Output "Copied three authored skills and nine authored custom agents."
Write-Output "Existing same-name assets, if any, were backed up under: $backupRoot"
