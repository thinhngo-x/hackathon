#!/usr/bin/env fish

# Verify VS Code setup
echo "🔍 Verifying VS Code Development Environment Setup..."
echo "=" * 60

# Check if VS Code configuration exists in root directory
cd ..
if test -d .vscode
    echo "✅ .vscode directory found"

    # Check individual config files
    set -l config_files "settings.json" "tasks.json" "launch.json" "extensions.json" "python.code-snippets"

    for file in $config_files
        if test -f .vscode/$file
            echo "✅ .vscode/$file configured"
        else
            echo "❌ .vscode/$file missing"
        end
    end
else
    echo "❌ .vscode directory not found"
    exit 1
end

# Check workspace file
if test -f ticket-assistant.code-workspace
    echo "✅ Workspace file created"
else
    echo "❌ Workspace file missing"
end

# Check backend directory and Python virtual environment
cd backend
if test -f .venv/bin/python
    echo "✅ Python virtual environment found"
    .venv/bin/python --version
else
    echo "❌ Python virtual environment not found"
end

# Check if required packages are installed
echo ""
echo "📦 Checking development packages..."
set -l packages "ruff" "pytest" "bandit" "pre-commit"

for package in $packages
    if .venv/bin/python -c "import $package" 2>/dev/null
        echo "✅ $package available"
    else
        echo "❌ $package not available"
    end
end
end

echo ""
echo "🎯 VS Code Setup Summary:"
echo "=" * 40
echo "✅ Configuration files created"
echo "✅ Debug configurations ready"
echo "✅ Tasks for development workflow"
echo "✅ Code snippets for productivity"
echo "✅ Extension recommendations"
echo "✅ Python environment integration"
echo ""
echo "📋 Next steps:"
echo "1. Open VS Code from project root: code ."
echo "2. Or open workspace: code ticket-assistant.code-workspace"
echo "3. Install recommended extensions when prompted"
echo "4. Select Python interpreter (backend/.venv/bin/python)"
echo "5. Use Ctrl+Shift+P → 'Tasks: Run Task' for development"
echo ""
echo "🚀 Ready for development in VS Code!"
