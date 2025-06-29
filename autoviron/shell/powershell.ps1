# AutoViron PowerShell Integration
# Source this file in your PowerShell profile

# Function to automatically activate virtual environment
function Invoke-AutoVironActivate {
    # Get the AutoViron script path
    $autovironScript = Join-Path (Split-Path (Split-Path $PSCommandPath)) "autoviron.py"
    
    # Check if AutoViron script exists
    if (-not (Test-Path $autovironScript)) {
        Write-Host "AutoViron script not found at: $autovironScript" -ForegroundColor Red
        return $false
    }
    
    # Run AutoViron and capture output
    try {
        $output = & python $autovironScript --no-auto-create 2>$null
        
        # If AutoViron found a virtual environment, activate it
        if ($LASTEXITCODE -eq 0 -and $output) {
            # Extract the source command from output (for PowerShell, we need to handle differently)
            $sourceCmd = $output | Select-String "^source "
            if ($sourceCmd) {
                # Convert Unix source command to PowerShell equivalent
                $activatePath = ($sourceCmd.Line -replace "^source ", "").Trim()
                if (Test-Path $activatePath) {
                    & $activatePath
                    return $true
                }
            }
        }
    }
    catch {
        Write-Host "Error running AutoViron: $_" -ForegroundColor Red
    }
    
    return $false
}

# Function to create and activate virtual environment
function Invoke-AutoVironCreate {
    $autovironScript = Join-Path (Split-Path (Split-Path $PSCommandPath)) "autoviron.py"
    
    if (-not (Test-Path $autovironScript)) {
        Write-Host "AutoViron script not found at: $autovironScript" -ForegroundColor Red
        return $false
    }
    
    try {
        $output = & python $autovironScript 2>$null
        
        if ($LASTEXITCODE -eq 0 -and $output) {
            $sourceCmd = $output | Select-String "^source "
            if ($sourceCmd) {
                $activatePath = ($sourceCmd.Line -replace "^source ", "").Trim()
                if (Test-Path $activatePath) {
                    & $activatePath
                    return $true
                }
            }
        }
    }
    catch {
        Write-Host "Error running AutoViron: $_" -ForegroundColor Red
    }
    
    return $false
}

# Function to deactivate current virtual environment
function Invoke-AutoVironDeactivate {
    if ($env:VIRTUAL_ENV) {
        deactivate
        Write-Host "Deactivated virtual environment: $env:VIRTUAL_ENV" -ForegroundColor Green
        Remove-Item Env:VIRTUAL_ENV -ErrorAction SilentlyContinue
    }
    else {
        Write-Host "No virtual environment currently active" -ForegroundColor Yellow
    }
}

# Function to show current virtual environment status
function Get-AutoVironStatus {
    if ($env:VIRTUAL_ENV) {
        Write-Host "Active virtual environment: $env:VIRTUAL_ENV" -ForegroundColor Green
        Write-Host "Python: $(Get-Command python | Select-Object -ExpandProperty Source)"
        Write-Host "Pip: $(Get-Command pip | Select-Object -ExpandProperty Source)"
    }
    else {
        Write-Host "No virtual environment currently active" -ForegroundColor Yellow
        
        # Check if there's a virtual environment in current directory
        $autovironScript = Join-Path (Split-Path (Split-Path $PSCommandPath)) "autoviron.py"
        if (Test-Path $autovironScript) {
            try {
                $output = & python $autovironScript --no-auto-activate --verbose 2>$null
                if ($LASTEXITCODE -eq 0) {
                    Write-Host "Available virtual environment detected in current project" -ForegroundColor Cyan
                }
            }
            catch {
                # Silently ignore errors
            }
        }
    }
}

# Function to override Set-Location for auto-activation
function Set-AutoVironLocation {
    param(
        [Parameter(ValueFromPipeline=$true)]
        [string]$Path
    )
    
    # Call the original Set-Location command
    Set-Location $Path
    
    # Try to activate virtual environment in new directory
    Invoke-AutoVironActivate | Out-Null
}

# Create aliases for easier use
Set-Alias -Name autoviron-activate -Value Invoke-AutoVironActivate
Set-Alias -Name autoviron-create -Value Invoke-AutoVironCreate
Set-Alias -Name autoviron-deactivate -Value Invoke-AutoVironDeactivate
Set-Alias -Name autoviron-status -Value Get-AutoVironStatus
Set-Alias -Name cd -Value Set-AutoVironLocation

# Auto-activate virtual environment in current directory on shell startup
Invoke-AutoVironActivate | Out-Null

Write-Host "AutoViron PowerShell integration loaded. Use 'autoviron-status' to check status." -ForegroundColor Green 