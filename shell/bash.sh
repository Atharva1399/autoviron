#!/bin/bash
# AutoViron Bash Integration
# Source this file in your .bashrc or .bash_profile

# Function to automatically activate virtual environment
autoviron_activate() {
    # Get the AutoViron script path
    local autoviron_script="$(dirname "$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")")/autoviron.py"
    
    # Check if AutoViron script exists
    if [[ ! -f "$autoviron_script" ]]; then
        echo "AutoViron script not found at: $autoviron_script" >&2
        return 1
    fi
    
    # Run AutoViron and capture output
    local output
    output=$(python3 "$autoviron_script" --no-auto-create 2>/dev/null)
    
    # If AutoViron found a virtual environment, activate it
    if [[ $? -eq 0 && -n "$output" ]]; then
        # Extract the activation command from output
        local activate_cmd=$(echo "$output" | head -n1)
        if [[ -n "$activate_cmd" ]]; then
            # Handle different activation command types
            if [[ "$activate_cmd" =~ ^source ]]; then
                eval "$activate_cmd"
                return 0
            elif [[ "$activate_cmd" =~ ^poetry ]]; then
                eval "$activate_cmd"
                return 0
            elif [[ "$activate_cmd" =~ ^pipenv ]]; then
                eval "$activate_cmd"
                return 0
            elif [[ "$activate_cmd" =~ ^conda ]]; then
                eval "$activate_cmd"
                return 0
            fi
        fi
    fi
    
    return 1
}

# Function to create and activate virtual environment
autoviron_create() {
    local autoviron_script="$(dirname "$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")")/autoviron.py"
    
    if [[ ! -f "$autoviron_script" ]]; then
        echo "AutoViron script not found at: $autoviron_script" >&2
        return 1
    fi
    
    local output
    output=$(python3 "$autoviron_script" 2>/dev/null)
    
    if [[ $? -eq 0 && -n "$output" ]]; then
        local activate_cmd=$(echo "$output" | head -n1)
        if [[ -n "$activate_cmd" ]]; then
            if [[ "$activate_cmd" =~ ^source ]]; then
                eval "$activate_cmd"
                return 0
            elif [[ "$activate_cmd" =~ ^poetry ]]; then
                eval "$activate_cmd"
                return 0
            elif [[ "$activate_cmd" =~ ^pipenv ]]; then
                eval "$activate_cmd"
                return 0
            elif [[ "$activate_cmd" =~ ^conda ]]; then
                eval "$activate_cmd"
                return 0
            fi
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
    elif [[ -n "$POETRY_ACTIVE" ]]; then
        exit
        echo "Deactivated Poetry environment"
        unset POETRY_ACTIVE
    elif [[ -n "$PIPENV_ACTIVE" ]]; then
        exit
        echo "Deactivated Pipenv environment"
        unset PIPENV_ACTIVE
    elif [[ -n "$CONDA_DEFAULT_ENV" ]]; then
        conda deactivate
        echo "Deactivated Conda environment: $CONDA_DEFAULT_ENV"
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
    elif [[ -n "$POETRY_ACTIVE" ]]; then
        echo "Active Poetry environment"
        echo "Python: $(which python)"
        echo "Poetry: $(which poetry)"
    elif [[ -n "$PIPENV_ACTIVE" ]]; then
        echo "Active Pipenv environment"
        echo "Python: $(which python)"
        echo "Pipenv: $(which pipenv)"
    elif [[ -n "$CONDA_DEFAULT_ENV" ]]; then
        echo "Active Conda environment: $CONDA_DEFAULT_ENV"
        echo "Python: $(which python)"
        echo "Conda: $(which conda)"
    else
        echo "No virtual environment currently active"
        
        # Check if there's a virtual environment in current directory
        local autoviron_script="$(dirname "$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")")/autoviron.py"
        if [[ -f "$autoviron_script" ]]; then
            local output
            output=$(python3 "$autoviron_script" --no-auto-activate --verbose 2>/dev/null)
            if [[ $? -eq 0 ]]; then
                echo "Available environment detected in current project"
            fi
        fi
    fi
}

# Function to run commands in the detected environment
autoviron_run() {
    local autoviron_script="$(dirname "$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")")/autoviron.py"
    
    if [[ ! -f "$autoviron_script" ]]; then
        echo "AutoViron script not found at: $autoviron_script" >&2
        return 1
    fi
    
    python3 "$autoviron_script" "$@"
}

# Auto-activate virtual environment when changing directories
autoviron_cd() {
    # Store current directory for comparison
    local old_pwd="$PWD"
    
    # Call the original cd command
    builtin cd "$@"
    
    # Check if we actually changed directories
    if [[ "$old_pwd" != "$PWD" ]]; then
        # Try to activate virtual environment in new directory
        autoviron_activate
    fi
}

# Function to handle directory changes via PROMPT_COMMAND
autoviron_prompt() {
    # Only run if we're in a different directory than last time
    if [[ "$AUTOVIRON_LAST_DIR" != "$PWD" ]]; then
        autoviron_activate
        export AUTOVIRON_LAST_DIR="$PWD"
    fi
}

# Override cd command to auto-activate virtual environments
alias cd='autoviron_cd'

# Add to PROMPT_COMMAND for automatic activation
if [[ -n "$PROMPT_COMMAND" ]]; then
    export PROMPT_COMMAND="$PROMPT_COMMAND; autoviron_prompt"
else
    export PROMPT_COMMAND="autoviron_prompt"
fi

# Export functions for use in shell
export -f autoviron_activate
export -f autoviron_create
export -f autoviron_deactivate
export -f autoviron_status
export -f autoviron_run
export -f autoviron_cd
export -f autoviron_prompt

# Auto-activate virtual environment in current directory on shell startup
autoviron_activate

echo "AutoViron bash integration loaded. Use 'autoviron_status' to check status." 
echo "AutoViron bash integration loaded. Use 'autoviron_status' to check status." 