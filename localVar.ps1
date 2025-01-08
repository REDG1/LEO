Write-Host "Adding variables:"

# Set environment variables in PowerShell
[System.Environment]::SetEnvironmentVariable("DEBUG", "True", [System.EnvironmentVariableTarget]::Process)
[System.Environment]::SetEnvironmentVariable("SERVICE_URL", "127.0.0.1", [System.EnvironmentVariableTarget]::Process)
[System.Environment]::SetEnvironmentVariable("DB_NAME", "nfdiDB", [System.EnvironmentVariableTarget]::Process)
[System.Environment]::SetEnvironmentVariable("DB_USER", "nfdiUser", [System.EnvironmentVariableTarget]::Process)
[System.Environment]::SetEnvironmentVariable("DB_PASS", "nfdiPass", [System.EnvironmentVariableTarget]::Process)
[System.Environment]::SetEnvironmentVariable("DB_HOST", "127.0.0.1", [System.EnvironmentVariableTarget]::Process)
[System.Environment]::SetEnvironmentVariable("DB_PORT", "3307", [System.EnvironmentVariableTarget]::Process)
[System.Environment]::SetEnvironmentVariable("SECRET_KEY", "leo_nfdi_2025", [System.EnvironmentVariableTarget]::Process)

# Display the values of the environment variables

Write-Host "SERVICE_URL: $env:SERVICE_URL"
Write-Host "DEBUG: $env:DEBUG"
Write-Host "DB_NAME: $env:DB_NAME"
Write-Host "DB_USER: $env:DB_USER"
Write-Host "DB_PASS: $env:DB_PASS"
Write-Host "DB_HOST: $env:DB_HOST"
Write-Host "DB_PORT: $env:DB_PORT"
Write-Host "SECRET_KEY: $env:SECRET_KEY"


Write-Host "Variables added"