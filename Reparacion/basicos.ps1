# Winget:  https://apps.microsoft.com/detail/9nblggh4nns1?hl=es-MX&gl=AR
Write-Output "Arranca! (https://apps.microsoft.com/detail/9nblggh4nns1?hl=es-MX&gl=AR)"


$apps = @(
    @{name = "Google.Chrome" },
	@{name = "Microsoft.Office" },
	@{name = "Zoom.Zoom" },
	@{name = "RARLab.WinRAR" },
	@{name = "VideoLAN.VLC" },
	@{name = "Microsoft.VCRedist.2005.x64" },
	@{name = "Microsoft.VCRedist.2008.x64" },
	@{name = "Microsoft.VCRedist.2010.x64" },
	@{name = "Microsoft.VCRedist.2012.x64" },
	@{name = "Microsoft.VCRedist.2013.x64" },
	@{name = "Microsoft.VCRedist.2015+.x64" },
	@{name = "Microsoft.DotNet.DesktopRuntime.5" },
	@{name = "AdoptOpenJDK.OpenJDK.8" },
	@{name = "AdoptOpenJDK.OpenJDK.17" },
   	@{name = "qBittorrent.qBittorrent" }	
);

Foreach ($app in $apps) {
    $listApp = winget list --exact -q $app.name
    if (![String]::Join("", $listApp).Contains($app.name)) {
        Write-host "Ahora instalando" $app.name
        winget install -e -h --accept-source-agreements --accept-package-agreements --id $app.name 
    }
    else {
        Write-host "Omitiendo" $app.name "(ya esta instalada)"
    }
}

