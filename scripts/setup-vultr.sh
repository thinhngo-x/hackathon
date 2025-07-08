#!/bin/bash

# Setup script for Vultr deployment
echo "🎫 Ticket Assistant - Vultr Deployment Setup"
echo "============================================="

# Function to detect OS
detect_os() {
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo "macos"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "linux"
    else
        echo "unknown"
    fi
}

# Install Docker on macOS
install_docker_macos() {
    echo "🐳 Installing Docker on macOS..."

    if command -v brew &> /dev/null; then
        echo "Using Homebrew to install Docker..."
        brew install --cask docker
    else
        echo "Please install Docker Desktop from: https://www.docker.com/products/docker-desktop/"
        echo "Or install Homebrew first: /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
    fi
}

# Install Docker on Linux
install_docker_linux() {
    echo "🐳 Installing Docker on Linux..."

    # Update package index
    sudo apt-get update

    # Install required packages
    sudo apt-get install -y \
        ca-certificates \
        curl \
        gnupg \
        lsb-release

    # Add Docker's official GPG key
    sudo mkdir -p /etc/apt/keyrings
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

    # Set up repository
    echo \
        "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
        $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

    # Install Docker
    sudo apt-get update
    sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

    # Add user to docker group
    sudo usermod -aG docker $USER

    echo "Please log out and log back in for Docker permissions to take effect."
}

# Install Vultr CLI
install_vultr_cli() {
    echo "☁️  Installing Vultr CLI..."

    if command -v go &> /dev/null; then
        go install github.com/vultr/vultr-cli@latest
        echo "✅ Vultr CLI installed via Go"
    else
        echo "📦 Installing Go first..."
        if [[ "$(detect_os)" == "macos" ]]; then
            if command -v brew &> /dev/null; then
                brew install go
                go install github.com/vultr/vultr-cli@latest
            else
                echo "Please install Go from: https://golang.org/dl/"
                echo "Then run: go install github.com/vultr/vultr-cli@latest"
            fi
        else
            # Linux installation
            curl -OL https://golang.org/dl/go1.21.5.linux-amd64.tar.gz
            sudo tar -C /usr/local -xzf go1.21.5.linux-amd64.tar.gz
            echo 'export PATH=$PATH:/usr/local/go/bin' >> ~/.bashrc
            source ~/.bashrc
            go install github.com/vultr/vultr-cli@latest
        fi
    fi
}

# Install kubectl
install_kubectl() {
    echo "⚙️  Installing kubectl..."

    if [[ "$(detect_os)" == "macos" ]]; then
        if command -v brew &> /dev/null; then
            brew install kubectl
        else
            curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/darwin/amd64/kubectl"
            chmod +x kubectl
            sudo mv kubectl /usr/local/bin/
        fi
    else
        curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
        chmod +x kubectl
        sudo mv kubectl /usr/local/bin/
    fi
}

# Main setup function
main() {
    echo "🔍 Detected OS: $(detect_os)"

    # Install Docker
    if ! command -v docker &> /dev/null; then
        case "$(detect_os)" in
            "macos")
                install_docker_macos
                ;;
            "linux")
                install_docker_linux
                ;;
            *)
                echo "❌ Unsupported OS. Please install Docker manually."
                exit 1
                ;;
        esac
    else
        echo "✅ Docker already installed"
    fi

    # Install Vultr CLI
    if ! command -v vultr-cli &> /dev/null; then
        install_vultr_cli
    else
        echo "✅ Vultr CLI already installed"
    fi

    # Install kubectl
    if ! command -v kubectl &> /dev/null; then
        install_kubectl
    else
        echo "✅ kubectl already installed"
    fi

    echo ""
    echo "✅ Setup complete!"
    echo ""
    echo "🚀 Next steps:"
    echo "1. Get your Vultr API key: https://my.vultr.com/settings/#settingsapi"
    echo "2. Get your Groq API key (optional): https://console.groq.com/keys"
    echo "3. Run: ./scripts/quick-deploy.sh"
    echo ""
    echo "Or deploy manually:"
    echo "  export VULTR_API_KEY=your_api_key"
    echo "  ./scripts/deploy-vultr.sh"
}

# Run main function
main
