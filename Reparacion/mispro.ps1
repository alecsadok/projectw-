# Habilitar ejecución de scripts
Set-ExecutionPolicy RemoteSigned -Scope Process -Force

# Verificar si Winget está instalado
if (-not (Get-Command winget -ErrorAction SilentlyContinue)) {
    Write-Host "Winget no está instalado o no está disponible en el PATH." -ForegroundColor Red
    exit
}

# Lista de programas a instalar
$apps = @(
    "Google.Chrome",
    "Plex.PlexMediaServer",
    "Adobe.Acrobat.Reader.64-bit",
    "ElectronicArts.EADesktop",
    "CodecGuide.K-LiteCodecPack.Mega",
    "Canva.Canva",
    "Discord.Discord",
    "PeterPawlowski.foobar2000",
    "Mozilla.Firefox.ESR.es-AR",
    "OBSProject.OBSStudio",
    "qBittorrent.qBittorrent.Qt6",
    "RevoUninstaller.RevoUninstallerPro",
    "VideoLAN.VLC",
    "RARLab.WinRAR",
    "Zoom.Zoom",
    "Valve.Steam",
    "9NKSQGP7F2NH",
    "9WZDNCRFJ3TJ",
    "9P6RC76MSMMJ",
    "9NXQXXLFST89"
)

foreach ($app in $apps) {
    Write-Host "Instalando $app ..." -ForegroundColor Cyan
    winget install --id=$app -e --accept-source-agreements --accept-package-agreements
}
