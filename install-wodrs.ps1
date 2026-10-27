<#
install-wodrs.ps1
Installs wodrs scripts + the Wodrs font to the current user.
No admin rights required. Safe to re-run.
#>

$ErrorActionPreference = "Stop"
$dir  = "$env:LOCALAPPDATA\Programs\wodrs"
$here = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "Installing wodrs..."
Write-Host "  Source: $here"
Write-Host "  Target: $dir"

# --- Copy scripts ---
New-Item -ItemType Directory -Force -Path $dir | Out-Null
Copy-Item "$here\*.py"  $dir -Force
Copy-Item "$here\*.cmd" $dir -Force
Copy-Item "$here\*.vbs" $dir -Force
Copy-Item "$here\*.txt" $dir -Force -ErrorAction SilentlyContinue

# --- Add to user PATH ---
$old = [Environment]::GetEnvironmentVariable("Path", "User")
if ($old -notlike "*$dir*") {
    [Environment]::SetEnvironmentVariable("Path", "$old;$dir", "User")
    Write-Host "  Added to user PATH."
} else {
    Write-Host "  Already on PATH."
}

# --- Create Start-menu shortcut ---
$startMenu = "$env:APPDATA\Microsoft\Windows\Start Menu\Programs"
$shortcut  = "$startMenu\wodrs.lnk"
$ws  = New-Object -ComObject WScript.Shell
$lnk = $ws.CreateShortcut($shortcut)
$lnk.TargetPath        = "$dir\run_gui.vbs"
$lnk.Arguments         = "`"$dir\wodrs_gui.py`""
$lnk.WorkingDirectory  = $dir
$lnk.IconLocation      = "imageres.dll,197"
$lnk.Description       = "wodrs - Sinhala <-> wodrs converter"
$lnk.Save()
Write-Host "  Start-menu shortcut created."

# --- Install font (per-user, no admin) ---
$fontSrc = "$here\Wodrs.ttf"
if (Test-Path $fontSrc) {
    $fontDstDir = "$env:LOCALAPPDATA\Microsoft\Windows\Fonts"
    $fontDst    = "$fontDstDir\Wodrs.ttf"
    New-Item -ItemType Directory -Force -Path $fontDstDir | Out-Null

    $skipCopy = $false
    if (Test-Path $fontDst) {
        $srcHash = (Get-FileHash $fontSrc -Algorithm MD5).Hash
        $dstHash = (Get-FileHash $fontDst -Algorithm MD5).Hash
        if ($srcHash -eq $dstHash) {
            Write-Host "  Wodrs font already installed (same version)."
            $skipCopy = $true
        }
    }

    if (-not $skipCopy) {
        try {
            Copy-Item $fontSrc $fontDst -Force
            Write-Host "  Wodrs font installed (per-user)."
        } catch {
            Write-Host "  Wodrs font is in use by Windows - will register only."
            Write-Host "  (To update the font, close all apps and log out, then re-run.)"
        }
    }

    $regPath = "HKCU:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts"
    if (-not (Test-Path $regPath)) {
        New-Item -Path $regPath -Force | Out-Null
    }
    $regName = "Wodrs (TrueType)"
    Set-ItemProperty -Path $regPath -Name $regName -Value "Wodrs.ttf"
    Write-Host "  Wodrs font registered."
} else {
    Write-Host "  Wodrs.ttf not found in the install folder - font not installed."
    Write-Host "  (You can install it manually later: right-click -> Install)"
}

Write-Host ""
Write-Host "Installation complete."
Write-Host ""
Write-Host "Next steps:"
Write-Host "  1. Close and reopen PowerShell."
Write-Host "  2. Type:  wodrs      (to verify the CLI)"
Write-Host "  3. Press Windows key, type 'wodrs', and open the GUI."
Write-Host ""
Write-Host "Note: Some applications may need to be restarted to see the new font."
