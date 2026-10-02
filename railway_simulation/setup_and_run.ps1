# Railway Traffic Simulation - Setup and Run Script (PowerShell)
# Run this from f:\peeda\railway_simulation\

Write-Host "╔══════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║  AI-Based Railway Traffic Control Simulation               ║" -ForegroundColor Cyan
Write-Host "║  Setup and Run Script                                      ║" -ForegroundColor Cyan
Write-Host "╚══════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan

# --- Step 1: Find Python ---
Write-Host "`n[1/3] Locating Python..." -ForegroundColor Yellow

$pythonExe = $null
$candidates = @(
    "python",
    "python3",
    "py",
    "$env:LOCALAPPDATA\Programs\Python\Python312\python.exe",
    "$env:LOCALAPPDATA\Programs\Python\Python311\python.exe",
    "$env:LOCALAPPDATA\Programs\Python\Python310\python.exe",
    "$env:LOCALAPPDATA\Programs\Python\Python39\python.exe",
    "C:\Python312\python.exe",
    "C:\Python311\python.exe",
    "C:\Python310\python.exe",
    "C:\Users\$env:USERNAME\miniconda3\python.exe",
    "C:\Users\$env:USERNAME\anaconda3\python.exe",
    "C:\ProgramData\miniconda3\python.exe",
    "C:\ProgramData\anaconda3\python.exe"
)

foreach ($candidate in $candidates) {
    try {
        $ver = & $candidate --version 2>&1
        if ($ver -match "Python 3") {
            $pythonExe = $candidate
            Write-Host "  Found Python: $candidate ($ver)" -ForegroundColor Green
            break
        }
    } catch { }
}

if (-not $pythonExe) {
    Write-Host "  ERROR: Python 3 not found on this system!" -ForegroundColor Red
    Write-Host ""
    Write-Host "  Please install Python 3.9+ from: https://www.python.org/downloads/" -ForegroundColor Yellow
    Write-Host "  Or install via Microsoft Store: winget install Python.Python.3.12" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "  After installing, run this script again." -ForegroundColor Yellow
    exit 1
}

# --- Step 2: Install Dependencies ---
Write-Host "`n[2/3] Installing dependencies..." -ForegroundColor Yellow
& $pythonExe -m pip install matplotlib numpy --quiet
if ($LASTEXITCODE -ne 0) {
    Write-Host "  WARNING: pip install failed. Trying with --user flag..." -ForegroundColor Yellow
    & $pythonExe -m pip install matplotlib numpy --user --quiet
}
Write-Host "  Dependencies ready." -ForegroundColor Green

# --- Step 3: Run Simulations ---
Write-Host "`n[3/3] Running simulations..." -ForegroundColor Yellow

# Create output directory
New-Item -ItemType Directory -Path "output" -Force | Out-Null

Write-Host "`n--- SCENARIO 1: Normal Traffic (Heuristic Controller) ---" -ForegroundColor Magenta
& $pythonExe main.py --scenario normal --controller heuristic --output output/normal

Write-Host "`n--- SCENARIO 2: Congested Traffic (FCFS Controller) ---" -ForegroundColor Magenta
& $pythonExe main.py --scenario congested --controller fcfs --output output/congested

Write-Host "`n--- SCENARIO 3: High Priority Conflict ---" -ForegroundColor Magenta
& $pythonExe main.py --scenario high_priority --controller priority --output output/priority

Write-Host "`n--- CONTROLLER COMPARISON (Normal Scenario) ---" -ForegroundColor Magenta
& $pythonExe main.py --compare --scenario normal --output output/comparison

Write-Host "`n✅ All simulations complete!" -ForegroundColor Green
Write-Host "   Plots saved to: f:\peeda\railway_simulation\output\" -ForegroundColor Cyan
Write-Host ""
Write-Host "  Individual runs:" -ForegroundColor White
Write-Host "    python main.py                            # default" -ForegroundColor Gray
Write-Host "    python main.py --scenario congested       # high load" -ForegroundColor Gray
Write-Host "    python main.py --compare                  # all controllers" -ForegroundColor Gray
