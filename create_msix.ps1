# Create MSIX Package Using MakeAppx (No GUI needed)
# This script creates an MSIX package from your executable

Write-Host "`n🎯 Creating MSIX Package for AI Chatbot" -ForegroundColor Green
Write-Host "=" * 60

# Step 1: Find Windows SDK (MakeAppx tool)
$sdkVersions = Get-ChildItem "C:\Program Files (x86)\Windows Kits\10\bin\" -Directory | 
               Where-Object { $_.Name -match '^\d+\.\d+\.\d+\.\d+$' } | 
               Sort-Object Name -Descending

if ($sdkVersions.Count -eq 0) {
    Write-Host "`n❌ Windows SDK not found" -ForegroundColor Red
    Write-Host "Installing Windows SDK..." -ForegroundColor Yellow
    Write-Host "`nOption 1: Install via Visual Studio Installer (recommended)"
    Write-Host "  - Open Visual Studio Installer"
    Write-Host "  - Modify → Individual Components → Windows 10 SDK"
    Write-Host "`nOption 2: Direct download"
    Write-Host "  - https://developer.microsoft.com/en-us/windows/downloads/windows-sdk/"
    Write-Host "`nOption 3: Use online MSIX builder (easiest!)"
    Write-Host "  - https://www.advancedinstaller.com/msix-builder.html"
    Write-Host "  - Upload your EXE and it creates MSIX for you"
    exit 1
}

$sdkPath = $sdkVersions[0].FullName
$makeAppx = Join-Path $sdkPath "x64\makeappx.exe"
$signTool = Join-Path $sdkPath "x64\signtool.exe"

if (-not (Test-Path $makeAppx)) {
    Write-Host "`n❌ MakeAppx not found at: $makeAppx" -ForegroundColor Red
    Write-Host "Try the online MSIX builder instead:" -ForegroundColor Yellow
    Write-Host "https://www.advancedinstaller.com/msix-builder.html" -ForegroundColor Cyan
    exit 1
}

Write-Host "✅ Found Windows SDK: $($sdkVersions[0].Name)" -ForegroundColor Green

# Step 2: Create package directory structure
Write-Host "`n📁 Creating package structure..." -ForegroundColor Cyan
$packageDir = "package_temp"
Remove-Item $packageDir -Recurse -Force -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Path $packageDir -Force | Out-Null

# Copy files
Copy-Item "dist\AI_Chatbot_Store.exe" "$packageDir\" -Force
Copy-Item "Package.appxmanifest" "$packageDir\" -Force
Copy-Item "Assets" "$packageDir\" -Recurse -Force

Write-Host "✅ Package structure created" -ForegroundColor Green

# Step 3: Create MSIX
Write-Host "`n📦 Creating MSIX package..." -ForegroundColor Cyan
New-Item -ItemType Directory -Path "msix" -Force | Out-Null

$msixPath = "msix\AIChatbot.msix"
& $makeAppx pack /d $packageDir /p $msixPath /nv

if ($LASTEXITCODE -ne 0) {
    Write-Host "`n❌ MSIX creation failed" -ForegroundColor Red
    exit 1
}

Write-Host "✅ MSIX package created: $msixPath" -ForegroundColor Green

# Step 4: Create self-signed certificate for testing
Write-Host "`n🔐 Creating test certificate..." -ForegroundColor Cyan
$certName = "CN=Dorcas Innovations LLC"
$cert = New-SelfSignedCertificate -Type Custom -Subject $certName `
    -KeyUsage DigitalSignature -FriendlyName "AI Chatbot Test Cert" `
    -CertStoreLocation "Cert:\CurrentUser\My" `
    -TextExtension @("2.5.29.37={text}1.3.6.1.5.5.7.3.3", "2.5.29.19={text}")

Write-Host "✅ Certificate created" -ForegroundColor Green

# Export certificate
$pfxPath = "msix\AIChatbot_TestCert.pfx"
$certPassword = ConvertTo-SecureString -String "test123" -Force -AsPlainText
Export-PfxCertificate -Cert $cert -FilePath $pfxPath -Password $certPassword | Out-Null

# Step 5: Sign MSIX
Write-Host "`n✍️  Signing MSIX package..." -ForegroundColor Cyan
& $signTool sign /fd SHA256 /a /f $pfxPath /p "test123" $msixPath

if ($LASTEXITCODE -ne 0) {
    Write-Host "`n❌ Signing failed" -ForegroundColor Red
    exit 1
}

Write-Host "✅ MSIX package signed" -ForegroundColor Green

# Cleanup
Remove-Item $packageDir -Recurse -Force -ErrorAction SilentlyContinue

# Summary
Write-Host "`n" + ("=" * 60) -ForegroundColor Green
Write-Host "🎉 SUCCESS! MSIX Package Created" -ForegroundColor Green
Write-Host ("=" * 60) -ForegroundColor Green
Write-Host "`n📦 Package Location:" -ForegroundColor Cyan
Write-Host "   $((Get-Item $msixPath).FullName)" -ForegroundColor White
Write-Host "`n🔑 Certificate:" -ForegroundColor Cyan
Write-Host "   $((Get-Item $pfxPath).FullName)" -ForegroundColor White
Write-Host "   Password: test123" -ForegroundColor Yellow

Write-Host "`n🧪 To Test Locally:" -ForegroundColor Cyan
Write-Host "   1. Install certificate:" -ForegroundColor White
Write-Host "      Import-PfxCertificate -FilePath `"$pfxPath`" -CertStoreLocation Cert:\LocalMachine\TrustedPeople -Password (ConvertTo-SecureString `"test123`" -AsPlainText -Force)" -ForegroundColor Gray
Write-Host "   2. Install MSIX:" -ForegroundColor White
Write-Host "      Add-AppxPackage `"$msixPath`"" -ForegroundColor Gray
Write-Host "   3. Find app in Start Menu: AI Chatbot" -ForegroundColor White

Write-Host "`n📤 For Microsoft Store:" -ForegroundColor Cyan
Write-Host "   - Upload: $msixPath" -ForegroundColor White
Write-Host "   - Microsoft will re-sign with their certificate" -ForegroundColor Gray
Write-Host "   - Register at: https://partner.microsoft.com/dashboard" -ForegroundColor White

Write-Host "`n"
