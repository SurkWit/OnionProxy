#!/bin/bash

# Script to install dependencies for OnionProxy.py and start it
# Supports Termux, Linux, and macOS

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to check if a command is available
check_command() {
    if command -v "$1" >/dev/null 2>&1; then
        echo -e "${GREEN}✓ $1 is installed${NC}"
        return 0
    else
        echo -e "${RED}✗ $1 is not installed${NC}"
        return 1
    }
}

# Function to check if a Python module is installed
check_python_module() {
    python3 -c "import $1" >/dev/null 2>&1
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Python module $1 is installed${NC}"
        return 0
    else
        echo -e "${RED}✗ Python module $1 is not installed${NC}"
        return 1
    }
}

# Detect OS
OS=$(uname -s)
echo -e "${YELLOW}Detected OS: $OS${NC}"

# Check for supported OS
if [ "$OS" != "Linux" ] && [ "$OS" != "Darwin" ] && ! command -v pkg >/dev/null; then
    echo -e "${RED}Unsupported system: $OS. Only Linux, macOS, and Termux are supported.${NC}"
    exit 1
fi

# Initialize flags for dependency checks
all_deps_met=true

# Check for Python3
if ! check_command python3; then
    all_deps_met=false
    echo -e "${YELLOW}Installing Python3...${NC}"
    case $OS in
        Linux)
            if command -v apt >/dev/null; then
                sudo apt update && sudo apt install -y python3
            elif command -v yum >/dev/null; then
                sudo yum install -y python3
            elif command -v pacman >/dev/null; then
                sudo pacman -S python3
            else
                echo -e "${RED}Unsupported package manager. Please install Python3 manually.${NC}"
                exit 1
            fi
            ;;
        Darwin)
            if command -v brew >/dev/null; then
                brew install python3
            else
                echo -e "${RED}Homebrew not found. Please install Homebrew or Python3 manually.${NC}"
                exit 1
            fi
            ;;
        *)
            # Termux
            if command -v pkg >/dev/null; then
                pkg install python
            else
                echo -e "${RED}Unsupported system. Please install Python3 manually.${NC}"
                exit 1
            fi
            ;;
    esac
fi

# Check for pip
if ! check_command pip3; then
    all_deps_met=false
    echo -e "${YELLOW}Installing pip...${NC}"
    case $OS in
        Linux)
            if command -v apt >/dev/null; then
                sudo apt install -y python3-pip
            elif command -v yum >/dev/null; then
                sudo yum install -y python3-pip
            elif command -v pacman >/dev/null; then
                sudo pacman -S python-pip
            else
                echo -e "${RED}Unsupported package manager. Please install pip manually.${NC}"
                exit 1
            fi
            ;;
        Darwin)
            if command -v brew >/dev/null; then
                brew install python3-pip
            else
                echo -e "${RED}Homebrew not found. Please install pip manually.${NC}"
                exit 1
            fi
            ;;
        *)
            # Termux
            if command -v pkg >/dev/null; then
                pkg install python-pip
            else
                echo -e "${RED}Unsupported system. Please install pip manually.${NC}"
                exit 1
            fi
            ;;
    esac
fi

# Check for Tor
if ! check_command tor; then
    all_deps_met=false
    echo -e "${YELLOW}Installing Tor...${NC}"
    case $OS in
        Linux)
            if command -v apt >/dev/null; then
                sudo apt update && sudo apt install -y tor
            elif command -v yum >/dev/null; then
                sudo yum install -y tor
            elif command -v pacman >/dev/null; then
                sudo pacman -S tor
            else
                echo -e "${RED}Unsupported package manager. Please install Tor manually.${NC}"
                exit 1
            fi
            ;;
        Darwin)
            if command -v brew >/dev/null; then
                brew install tor
            else
                echo -e "${RED}Homebrew not found. Please install Tor manually.${NC}"
                exit 1
            fi
            ;;
        *)
            # Termux
            if command -v pkg >/dev/null; then
                pkg install tor
            else
                echo -e "${RED}Unsupported system. Please install Tor manually.${NC}"
                exit 1
            fi
            ;;
    esac
fi

# Check for obfs4proxy
if ! check_command obfs4proxy; then
    all_deps_met=false
    echo -e "${YELLOW}Installing obfs4proxy...${NC}"
    case $OS in
        Linux)
            if command -v apt >/dev/null; then
                sudo apt update && sudo apt install -y obfs4proxy
            elif command -v yum >/dev/null; then
                sudo yum install -y obfs4proxy
            elif command -v pacman >/dev/null; then
                sudo pacman -S obfs4proxy
            else
                echo -e "${RED}Unsupported package manager. Please install obfs4proxy manually.${NC}"
                exit 1
            fi
            ;;
        Darwin)
            echo -e "${RED}obfs4proxy installation on macOS may require manual setup or building from source.${NC}"
            echo -e "${YELLOW}Please follow instructions at: https://gitlab.torproject.org/tpo/anti-censorship/pluggable-transports/obfs4${NC}"
            exit 1
            ;;
        *)
            # Termux
            if command -v pkg >/dev/null; then
                pkg install obfs4proxy
            else
                echo -e "${RED}Unsupported system. Please install obfs4proxy manually.${NC}"
                exit 1
            fi
            ;;
    esac
fi

# Check and install Python modules
for module in stem requests; do
    if ! check_python_module $module; then
        all_deps_met=false
        echo -e "${YELLOW}Installing Python module $module...${NC}"
        if ! pip3 install $module; then
            echo -e "${RED}Failed to install $module. Please install it manually: pip3 install $module${NC}"
            exit 1
        fi
    fi
done

# Special case for requests[socks]
if ! python3 -c "import requests; import socks" >/dev/null 2>&1; then
    all_deps_met=false
    echo -e "${YELLOW}Installing requests[socks]...${NC}"
    if ! pip3 install requests[socks]; then
        echo -e "${RED}Failed to install requests[socks]. Please install it manually: pip3 install requests[socks]${NC}"
        exit 1
    fi
fi

# Check if shutil is available (part of Python standard library)
if ! check_python_module shutil; then
    echo -e "${RED}shutil module is missing. This is part of the Python standard library. Please check your Python installation.${NC}"
    exit 1
fi

# Check if OnionProxy.py exists
if [ ! -f "OnionProxy.py" ]; then
    echo -e "${RED}OnionProxy.py not found in the current directory!${NC}"
    exit 1
fi

# If all dependencies are met, start OnionProxy.py
if [ "$all_deps_met" = true ]; then
    echo -e "${GREEN}All dependencies are installed. Starting OnionProxy.py...${NC}"
    python3 OnionProxy.py
else
    echo -e "${GREEN}All dependencies have been installed successfully. Starting OnionProxy.py...${NC}"
    python3 OnionProxy.py
fi