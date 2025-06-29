#!/bin/zsh
# AutoViron Zsh Integration
# Source this file in your .zshrc

# Function to automatically activate virtual environment
autoviron_activate() {
    # Get the AutoViron script path
    local autoviron_script="$(dirname "$(dirname "$(readlink -f "${(%):-%x}")")")/autoviron.py"
    
    # Check if AutoViron script exists
    if [[ ! -f "$autoviron_script" ]]; then
        echo "AutoViron script not found at: $autoviron_script"
        return 1
    fi
    
    # Run AutoViron and capture output
    local output
    output=$(python3 "$autoviron_script" --no-auto-create 2>/dev/null)
    
    # If AutoViron found a virtual environment, activate it
    if [[ $? -eq 0 && -n "$output" ]]; then
        # Extract the source command from output
        local source_cmd=$(echo "$output" | grep "^source ")
        if [[ -n "$source_cmd" ]]; then
            eval "$source_cmd"
            return 0
        fi
    fi
    
    return 1
}

# Function to create and activate virtual environment
autoviron_create() {
    local autoviron_script="$(dirname "$(dirname "$(readlink -f "${(%):-%x}")")")/autoviron.py"
    
    if [[ ! -f "$autoviron_script" ]]; then
        echo "AutoViron script not found at: $autoviron_script"
        return 1
    fi
    
    local output
    output=$(python3 "$autoviron_script" 2>/dev/null)
    
    if [[ $? -eq 0 && -n "$output" ]]; then
        local source_cmd=$(echo "$output" | grep "^source ")
        if [[ -n "$source_cmd" ]]; then
            eval "$source_cmd"
            return 0
        fi
    fi
    
    return 1
}

# Function to deactivate current virtual environment
autoviron_deactivate() {
    if [[ -n "$VIRTUAL_ENV" ]]; then
        deactivate
        echo "Deactivated virtual environment: $VIRTUAL_ENV"
        unset VIRTUAL_ENV
    else
        echo "No virtual environment currently active"
    fi
}

# Function to show current virtual environment status
autoviron_status() {
    if [[ -n "$VIRTUAL_ENV" ]]; then
        echo "Active virtual environment: $VIRTUAL_ENV"
        echo "Python: $(which python)"
        echo "Pip: $(which pip)"
    else
        echo "No virtual environment currently active"
        
        # Check if there's a virtual environment in current directory
        local autoviron_script="$(dirname "$(dirname "$(readlink -f "${(%):-%x}")")")/autoviron.py"
        if [[ -f "$autoviron_script" ]]; then
            local output
            output=$(python3 "$autoviron_script" --no-auto-activate --verbose 2>/dev/null)
            if [[ $? -eq 0 ]]; then
                echo "Available virtual environment detected in current project"
            fi
        fi
    fi
}

# Auto-activate virtual environment when changing directories
autoviron_cd() {
    # Call the original cd command
    builtin cd "$@"
    
    # Try to activate virtual environment in new directory
    autoviron_activate
}

# Override cd command to auto-activate virtual environments
alias cd='autoviron_cd'

# Auto-activate virtual environment in current directory on shell startup
autoviron_activate

echo "AutoViron zsh integration loaded. Use 'autoviron_status' to check status." 