# Enhanced Voice System Setup Script
# Run as Administrator for best results

Write-Host "Enhanced AI Companion - Voice System Setup" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

# Check if running as administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")

if (-not $isAdmin) {
    Write-Host "WARNING: Not running as administrator. Some voice features may not work properly." -ForegroundColor Yellow
    Write-Host ""
}

# Test microphone access
Write-Host "Testing microphone access..." -ForegroundColor Green
try {
    Add-Type -AssemblyName System.Speech
    $speech = New-Object System.Speech.Recognition.SpeechRecognitionEngine
    Write-Host "✓ Microphone access available" -ForegroundColor Green
} catch {
    Write-Host "✗ Microphone access issues detected" -ForegroundColor Red
    Write-Host "Please check Windows Privacy Settings > Microphone" -ForegroundColor Yellow
}

# Test audio output
Write-Host "Testing audio output..." -ForegroundColor Green
try {
    Add-Type -AssemblyName System.Speech
    $synth = New-Object System.Speech.Synthesis.SpeechSynthesizer
    $synth.SetOutputToDefaultAudioDevice()
    Write-Host "✓ Audio output available" -ForegroundColor Green
} catch {
    Write-Host "✗ Audio output issues detected" -ForegroundColor Red
}

# Install Edge TTS if needed
Write-Host "Checking Edge TTS..." -ForegroundColor Green
python -c "import edge_tts" 2>$null
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Edge TTS available" -ForegroundColor Green
} else {
    Write-Host "Installing Edge TTS..." -ForegroundColor Yellow
    pip install edge-tts
}

Write-Host ""
Write-Host "Voice system setup complete!" -ForegroundColor Cyan
Write-Host "You can now use voice features in the Enhanced AI Companion." -ForegroundColor Green
Write-Host ""
Write-Host "Press any key to continue..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")