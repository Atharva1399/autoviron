# AutoViron Fish Integration
# Source this file in your config.fish

# Function to automatically activate virtual environment
function autoviron_activate
    # Get the AutoViron script path
    set autoviron_script (dirname (dirname (readlink -f (status -f))))/autoviron.py
    
    # Check if AutoViron script exists
    if not test -f "$autoviron_script"
        echo "AutoViron script not found at: $autoviron_script"
        return 1
    end
    
    # Run AutoViron and capture output
    set output (python3 "$autoviron_script" --no-auto-create 2>/dev/null)
    
    # If AutoViron found a virtual environment, activate it
    if test $status -eq 0; and test -n "$output"
        # Extract the source command from output
        set source_cmd (echo "$output" | grep "^source ")
        if test -n "$source_cmd"
            eval $source_cmd
            return 0
        end
    end
    
    return 1
end

# Function to create and activate virtual environment
function autoviron_create
    set autoviron_script (dirname (dirname (readlink -f (status -f))))/autoviron.py
    
    if not test -f "$autoviron_script"
        echo "AutoViron script not found at: $autoviron_script"
        return 1
    end
    
    set output (python3 "$autoviron_script" 2>/dev/null)
    
    if test $status -eq 0; and test -n "$output"
        set source_cmd (echo "$output" | grep "^source ")
        if test -n "$source_cmd"
            eval $source_cmd
            return 0
        end
    end
    
    return 1
end

# Function to deactivate current virtual environment
function autoviron_deactivate
    if test -n "$VIRTUAL_ENV"
        deactivate
        echo "Deactivated virtual environment: $VIRTUAL_ENV"
        set -e VIRTUAL_ENV
    else
        echo "No virtual environment currently active"
    end
end

# Function to show current virtual environment status
function autoviron_status
    if test -n "$VIRTUAL_ENV"
        echo "Active virtual environment: $VIRTUAL_ENV"
        echo "Python: "(which python)
        echo "Pip: "(which pip)
    else
        echo "No virtual environment currently active"
        
        # Check if there's a virtual environment in current directory
        set autoviron_script (dirname (dirname (readlink -f (status -f))))/autoviron.py
        if test -f "$autoviron_script"
            set output (python3 "$autoviron_script" --no-auto-activate --verbose 2>/dev/null)
            if test $status -eq 0
                echo "Available virtual environment detected in current project"
            end
        end
    end
end

# Auto-activate virtual environment when changing directories
function autoviron_cd
    # Call the original cd command
    builtin cd $argv
    
    # Try to activate virtual environment in new directory
    autoviron_activate
end

# Override cd command to auto-activate virtual environments
alias cd='autoviron_cd'

# Auto-activate virtual environment in current directory on shell startup
autoviron_activate

echo "AutoViron fish integration loaded. Use 'autoviron_status' to check status." 