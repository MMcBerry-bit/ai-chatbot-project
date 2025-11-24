# Create MSIX Package Using MakeAppx
# Simple version without emojis

Write-Host "`nCreating MSIX Package for AI Chatbot" -ForegroundColor Green
Write-Host "============================================================"

# Find Windows SDK
$sdkVersions = Get-ChildItem "C:\Program Files (x86)\Windows Kits\10\bin\" -Directory -ErrorAction SilentlyContinue | 
               Where-Object { $_.Name -match '^\d+\.\d+\.\d+\.\d+$' } | 
               Sort-Object Name -Descending

if ($sdkVersions.Count -eq 0) {
    Write-Host "`nERROR: Windows SDK not found" -ForegroundColor Red
    Write-Host "`nEasiest solution: Use online MSIX builder (FREE)" -ForegroundColor Yellow
    Write-Host "Go to: https://www.advancedinstaller.com/msix-builder.html" -ForegroundColor Cyan
    Write-Host "Upload your EXE and it creates MSIX for you!" -ForegroundColor Cyan
    exit 1
}

$sdkPath = $sdkVersions[0].FullName
$makeAppx = Join-Path $sdkPath "x64\makeappx.exe"
$signTool = Join-Path $sdkPath "x64\signtool.exe"

if (-not (Test-Path $makeAppx)) {
    Write-Host "`nERROR: MakeAppx not found" -ForegroundColor Red
    Write-Host "Use online MSIX builder: https://www.advancedinstaller.com/msix-builder.html" -ForegroundColor Cyan
    exit 1
}

Write-Host "Found Windows SDK: $($sdkVersions[0].Name)" -ForegroundColor Green

# Create package directory
Write-Host "`nCreating package structure..." -ForegroundColor Cyan
$packageDir = "package_temp"
Remove-Item $packageDir -Recurse -Force -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Path $packageDir -Force | Out-Null

Copy-Item "dist\AI_Chatbot_Store.exe" "$packageDir\" -Force
Copy-Item "AppxManifest.xml" "$packageDir\" -Force
Copy-Item "Assets" "$packageDir\" -Recurse -Force

Write-Host "Package structure created" -ForegroundColor Green

# Create MSIX
Write-Host "`nCreating MSIX package..." -ForegroundColor Cyan
New-Item -ItemType Directory -Path "msix" -Force | Out-Null

$msixPath = "msix\AIChatbot.msix"
& $makeAppx pack /d $packageDir /p $msixPath /nv

if ($LASTEXITCODE -ne 0) {
    Write-Host "`nMSIX creation failed" -ForegroundColor Red
    exit 1
}

Write-Host "MSIX package created: $msixPath" -ForegroundColor Green

# Create test certificate
Write-Host "`nCreating test certificate..." -ForegroundColor Cyan
$certName = "CN=Dorcas Innovations LLC"
$cert = New-SelfSignedCertificate -Type Custom -Subject $certName `
    -KeyUsage DigitalSignature -FriendlyName "AI Chatbot Test Cert" `
    -CertStoreLocation "Cert:\CurrentUser\My" `
    -TextExtension @("2.5.29.37={text}1.3.6.1.5.5.7.3.3", "2.5.29.19={text}")

Write-Host "Certificate created" -ForegroundColor Green

# Export certificate
$pfxPath = "msix\AIChatbot_TestCert.pfx"
$certPassword = ConvertTo-SecureString -String "test123" -Force -AsPlainText
Export-PfxCertificate -Cert $cert -FilePath $pfxPath -Password $certPassword | Out-Null

# Sign MSIX
Write-Host "`nSigning MSIX package..." -ForegroundColor Cyan
& $signTool sign /fd SHA256 /a /f $pfxPath /p "test123" $msixPath

if ($LASTEXITCODE -ne 0) {
    Write-Host "`nSigning failed" -ForegroundColor Red
    exit 1
}

Write-Host "MSIX package signed" -ForegroundColor Green

# Cleanup
Remove-Item $packageDir -Recurse -Force -ErrorAction SilentlyContinue

# Summary
Write-Host "`n============================================================" -ForegroundColor Green
Write-Host "SUCCESS! MSIX Package Created" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
Write-Host "`nPackage Location:" -ForegroundColor Cyan
Write-Host "  $((Get-Item $msixPath).FullName)" -ForegroundColor White
Write-Host "`nCertificate:" -ForegroundColor Cyan
Write-Host "  $((Get-Item $pfxPath).FullName)" -ForegroundColor White
Write-Host "  Password: test123" -ForegroundColor Yellow

Write-Host "`nTo Test Locally:" -ForegroundColor Cyan
Write-Host "  1. Install certificate (run as Admin):" -ForegroundColor White
$fullPfxPath = (Get-Item $pfxPath).FullName
Write-Host "     Import-PfxCertificate -FilePath `"$fullPfxPath`" -CertStoreLocation Cert:\LocalMachine\TrustedPeople -Password (ConvertTo-SecureString `"test123`" -AsPlainText -Force)" -ForegroundColor Gray
Write-Host "`n  2. Install MSIX:" -ForegroundColor White
$fullMsixPath = (Get-Item $msixPath).FullName
Write-Host "     Add-AppxPackage `"$fullMsixPath`"" -ForegroundColor Gray
Write-Host "`n  3. Find app in Start Menu: AI Chatbot" -ForegroundColor White

Write-Host "`nFor Microsoft Store:" -ForegroundColor Cyan
Write-Host "  - Upload: $msixPath" -ForegroundColor White
Write-Host "  - Microsoft will re-sign with their certificate" -ForegroundColor Gray
Write-Host "  - Register at: https://partner.microsoft.com/dashboard" -ForegroundColor White

Write-Host "`n"
