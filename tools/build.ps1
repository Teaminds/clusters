# Переходим в корень проекта (если запуск из tools)
Set-Location "$PSScriptRoot\.."

# Получаем версию из main.py
$mainPy = Get-Content .\main.py
$versionLine = $mainPy | Where-Object { $_ -match 'APP_VERSION\s*=\s*["''](.+)["'']' }
if ($versionLine -match 'APP_VERSION\s*=\s*["''](.+)["'']') {
    $version = $matches[1]
} else {
    Write-Host "Не удалось найти версию в main.py"
    exit 1
}

# Собираем exe с версией в имени
pyinstaller --onefile --windowed `
    --add-data "levels;levels" `
    --add-data "assets;assets" `
    --add-data "components;components" `
    --add-data "system_components;system_components" `
    --add-data "ui;ui" `
    --name "clusters_v$version" main.py