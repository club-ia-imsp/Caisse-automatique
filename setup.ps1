# ============================================================
#   setup.ps1 - Installation de l'environnement Caisse Auto.
#   Usage : .\setup.ps1
#   Options :
#       -GPU      Active CUDA (torch cu124 pour NVIDIA)
#       -SkipNode Ignore l installation Node.js du frontend
# ============================================================
param(
    [switch]$GPU,
    [switch]$SkipNode
)

$ErrorActionPreference = "Stop"

$ROOT  = $PSScriptRoot
$VENV  = Join-Path $ROOT ".venv"
$REQS  = Join-Path $ROOT "requirements.txt"

function Write-Step { param([string]$msg) Write-Host "`n==> $msg" -ForegroundColor Cyan }
function Write-OK   { param([string]$msg) Write-Host "  [OK] $msg" -ForegroundColor Green }
function Write-Warn { param([string]$msg) Write-Host "  [!]  $msg" -ForegroundColor Yellow }
function Write-Fail { param([string]$msg) Write-Host "  [X]  $msg" -ForegroundColor Red; exit 1 }

# ── 1. Vérifier Python ───────────────────────────────────────
Write-Step "Verification de Python"
try {
    $pyVer = python --version 2>&1
    Write-OK $pyVer
} catch {
    Write-Fail "Python introuvable. Installez Python 3.10+ depuis https://python.org"
}

# ── 2. Créer l'environnement virtuel ─────────────────────────
Write-Step "Creation de l'environnement virtuel (.venv)"
if (Test-Path $VENV) {
    Write-Warn ".venv existe deja, il sera reutilise."
} else {
    python -m venv $VENV
    Write-OK "Environnement cree dans $VENV"
}

# ── 3. Activer le venv ───────────────────────────────────────
Write-Step "Activation du venv"
$activate = Join-Path $VENV "Scripts\Activate.ps1"
if (-not (Test-Path $activate)) {
    Write-Fail "Script d'activation introuvable : $activate"
}
& $activate
Write-OK "Venv actif"

# ── 4. Mettre à jour pip ─────────────────────────────────────
Write-Step "Mise a jour de pip"
python -m pip install --upgrade pip
Write-OK "pip mis a jour"

# ── 5. Torch GPU (optionnel) ──────────────────────────────────
if ($GPU) {
    Write-Step "Installation PyTorch avec support CUDA 12.4 (GPU NVIDIA)"
    Write-Warn "Cela peut prendre plusieurs minutes et telecharger ~2-3 Go"
    pip install torch torchvision --index-url https://download.pytorch.org/whl/cu124
    Write-OK "PyTorch CUDA installe"
}

# ── 6. Installer toutes les dependances Python ───────────────
Write-Step "Installation des dependances Python (requirements.txt)"
if (-not (Test-Path $REQS)) {
    Write-Fail "requirements.txt introuvable : $REQS"
}

pip install --upgrade -r $REQS
Write-OK "Toutes les dependances Python installees"

# ── 7. Frontend Node.js (optionnel) ──────────────────────────
if (-not $SkipNode) {
    Write-Step "Frontend React (Node.js / npm)"
    $frontendDir = Join-Path $ROOT "Caisse\frontend"
    if (Test-Path $frontendDir) {
        try {
            $nodeVer = node --version 2>&1
            Write-OK "Node.js $nodeVer detecte"
            Push-Location $frontendDir
            npm install
            Pop-Location
            Write-OK "Dependances npm installees"
        } catch {
            Write-Warn "Node.js introuvable. Installez-le depuis https://nodejs.org"
            Write-Warn "Puis lancez : cd Caisse\frontend && npm install"
        }
    } else {
        Write-Warn "Dossier frontend introuvable ($frontendDir), etape ignoree."
    }
} else {
    Write-Warn "Installation Node.js ignoree (-SkipNode)"
}

# ── 8. Résumé ─────────────────────────────────────────────────
Write-Host ""
Write-Host "============================================" -ForegroundColor Green
Write-Host "  Installation terminee avec succes !" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Green
Write-Host ""
Write-Host "Pour activer le venv manuellement :"
Write-Host "  .\.venv\Scripts\Activate.ps1" -ForegroundColor Yellow
Write-Host ""
Write-Host "Pour lancer le backend FastAPI :"
Write-Host "  cd Caisse\backend" -ForegroundColor Yellow
Write-Host "  uvicorn app.main:app --reload" -ForegroundColor Yellow
Write-Host ""
Write-Host "Pour lancer l'app desktop :"
Write-Host "  python Caisse\caisseAutomat_version1.py" -ForegroundColor Yellow
Write-Host ""
Write-Host "Pour lancer le frontend :"
Write-Host "  cd Caisse\frontend ; npm run start" -ForegroundColor Yellow
Write-Host ""
