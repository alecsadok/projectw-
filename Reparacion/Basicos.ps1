# Falta winget:  https://www.microsoft.com/en-us/p/app-installer/9nblggh4nns1
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
Write-Output "Arranca!"


$apps = @(
    @{name = "Google.Chrome" },
   	@{name = "qBittorrent.qBittorrent" }	
);

Foreach ($app in $apps) {
    $listApp = winget list --exact -q $app.name
    if (![String]::Join("", $listApp).Contains($app.name)) {
        Write-host "Ahora instalando" $app.name
        winget install -e -h --accept-source-agreements --accept-package-agreements --id $app.name 
    }
    else {
        Write-host "Omitiendo " $app.name " (ya esta instalada)"
    }
}

