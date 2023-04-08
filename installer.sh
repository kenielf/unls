#!/usr/bin/env sh
# Usage: ./installer.sh -i [-f] || ./installer -r

# <!-- Constants -->
# Support for disabling colors according to 'https://no-color.org/'
if [ "${NO_COLOR}" = "1" ]; then
    RESET=""
    RED=""
    YELLOW=""
    BLUE=""
    CYAN=""
else
    RESET="\x1b[00m"
    RED="\x1b[31m"
    YELLOW="\x1b[33m"
    BLUE="\x1b[34m"
    CYAN="\x1b[36m"
fi

# Installation Specifics
_PATH="${HOME}/.local/share/unls"
_BIN_PATH="${HOME}/.local/bin/unls"

# <!-- Functions -->
error() {
    1>&2 printf "${RED}[ERROR]${RESET} %s\n" "${1}" && \
        exit 1
}

warn() {
    1>&2 printf "${YELLOW}[WARNING]${RESET} %s\n" "${1}"
}

debug() {
    [ "${UNLS_DEBUG}" = "1" ] && printf "${CYAN}[DEBUG]${RESET} %s\n" "${1}"
}

info() {
    printf "${BLUE}[INFO]${RESET} %s\n" "${1}"
}

# <!-- Code -->
# Install
if [ "${1}" = "-i" ]; then
    info "Installing"
    # Enable force variable
    FORCE=0
    for arg in "$@"; do
        if [ "${arg}" = "-f" ]; then
            FORCE=1
        fi
    done

    # Check dependencies
    dependencies="python3 gpg nmcli geckodriver"
    
    missing=""
    # Check for each command individually
    for cmd in ${dependencies}; do
        if ! command -v "${cmd}" >/dev/null 2>&1; then
            # Add to the missing list
            if [ -z "${missing}" ]; then
                missing="${cmd}"
            else
                missing="${missing}, ${cmd}"
            fi
        fi
    done
    
    # Prompt the user to continue or not if commands are not found.
    if [ -n "${missing}" ]; then
        warn "Some commands were not found!"
        printf "%s %s\n%s\n" \
            "Missing:" "${missing}" \
            "Do you want to continue the installation anyway? [y/N]"
        while true; do
            printf " > "
            read -r choice
            case ${choice} in
                "y" | "Y")
                    printf "%s\n" "Continuing..."
                    break
                    ;;
                "n" | "N" | "")
                    error "Exiting due to missing commands!"
                    ;;
                *)
                    printf "%s\n" "Invalid options, use either 'y' for yes or 'n' for no!"
            esac
        done
    fi
    
    if [ -d "${_PATH}" ]; then
        if [ "${FORCE}" = "1" ]; then
            rm -rf "${_PATH}"
        else
            error "Program is already installed, to force an installation use '-f' flag!"
        fi
    fi
    
    # Create target directory
    debug "Creating install target directory..."
    mkdir -p "${_PATH}" || \
        error "Failed to create directory"
    
    # Copy files to the target directory
    for file in src/*.py; do
        debug "Installing: '${file}'"
        install -D -m644 "${file}" "${_PATH}/${file}"
    done
    debug "Installing binary..."
    install -D -m755 "src/unls" "${_PATH}/bin/unls"
    ln -sfT "${_PATH}/bin/unls" "${_BIN_PATH}"
    install -D -m644 "LICENSE" "${_PATH}/LICENSE"
    
    # Create virtual environment and install dependencies
    debug "Creating environment..."
    python3 -m venv "${_PATH}/.env" >/dev/null || \
        error "Failed to create environment!"
    
    # shellcheck source=/dev/null
    . "${_PATH}/.env/bin/activate" && \
        (python3 -m pip install -r "requirements.txt" >/dev/null || \
            error "Failed to install dependencies") && \
        deactivate

# Uninstall
elif [ "${1}" = "-r" ]; then
    info "Uninstalling..."
    if [ -d "${_PATH}" ]; then
        rm -rf "${_PATH}"
        rm -rf "${_BIN_PATH}"
    fi
    exit 0
else
    error "Invalid argument, please execute with '-i' to install or '-r' to remove!"
fi

