param(
  [ValidateSet("cursor", "claude", "codex")]
  [string]$Target = "cursor",

  [ValidateSet("project", "global")]
  [string]$Scope = "project",

  [string]$ProjectDir = "."
)

python "$PSScriptRoot\install.py" --target $Target --scope $Scope --project-dir $ProjectDir
