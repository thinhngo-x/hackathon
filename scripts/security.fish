#!/usr/bin/env fish

# Fish Shell Security Check Script for Ticket Assistant

echo "🛡️  Running comprehensive security checks..."

# Check if we're in the right directory
if not test -f "pyproject.toml"
    echo "❌ Not in the project root directory"
    exit 1
end

# Activate virtual environment
source .venv/bin/activate.fish
set -x PYTHONPATH (pwd)/src

echo "🔒 Security Analysis Report"
echo "=========================="
echo "Date: "(date)
echo ""

# Run Bandit security checks
echo "🔍 1. Running Bandit security scan..."
echo "-------------------------------------"
bandit -r src/ -f json -o bandit-report.json
bandit -r src/ -f txt

echo ""
echo "🔍 2. Checking for known vulnerabilities..."
echo "----------------------------------------"
safety check -r requirements.txt --json --output safety-report.json
safety check -r requirements.txt

echo ""
echo "🕵️  3. Scanning for secrets and sensitive data..."
echo "-----------------------------------------------"
detect-secrets scan --baseline .secrets.baseline

echo ""
echo "🔍 4. Checking environment configuration..."
echo "----------------------------------------"
if test -f ".env"
    echo "✅ .env file found"
    echo "🔍 Checking for potential security issues in .env..."

    # Check for weak configurations
    if grep -q "DEBUG=True" .env
        echo "⚠️  WARNING: DEBUG is set to True in .env"
    end

    if grep -q "API_HOST=0.0.0.0" .env
        echo "⚠️  WARNING: API_HOST is set to 0.0.0.0 (accepts all connections)"
    end

    # Check for example/placeholder values
    if grep -q "example.com" .env
        echo "⚠️  WARNING: Found example.com in .env - update with real values"
    end

    if grep -q "test-" .env
        echo "⚠️  WARNING: Found test- prefixed values in .env"
    end
else
    echo "❌ .env file not found - create from .env.example"
end

echo ""
echo "🔍 5. Checking Python dependencies..."
echo "-----------------------------------"
echo "📦 Checking for outdated packages with security issues..."
pip list --outdated

echo ""
echo "🔍 6. Analyzing imports and dependencies..."
echo "----------------------------------------"
echo "🔍 Checking for potentially dangerous imports..."
ruff check src/ tests/ --select S

echo ""
echo "🔍 7. File permissions and structure check..."
echo "--------------------------------------------"
echo "📁 Checking for world-writable files..."
find . -type f -perm -002 -not -path "./.git/*" -not -path "./.venv/*" -not -path "./__pycache__/*" | head -10

echo "📁 Checking for executable scripts..."
find . -type f -executable -not -path "./.git/*" -not -path "./.venv/*" -not -path "./node_modules/*" | head -10

echo ""
echo "📊 Security Summary:"
echo "===================="

# Check if security issues were found
set -l security_issues 0

if test -f "bandit-report.json"
    set bandit_issues (jq '.metrics._totals.CONFIDENCE.HIGH + .metrics._totals.CONFIDENCE.MEDIUM' bandit-report.json 2>/dev/null || echo "0")
    if test $bandit_issues -gt 0
        echo "❌ Bandit found $bandit_issues security issues"
        set security_issues (math $security_issues + 1)
    else
        echo "✅ Bandit: No high/medium security issues found"
    end
else
    echo "⚠️  Bandit report not generated"
end

if test -f "safety-report.json"
    set safety_issues (jq '. | length' safety-report.json 2>/dev/null || echo "0")
    if test $safety_issues -gt 0
        echo "❌ Safety found $safety_issues vulnerable dependencies"
        set security_issues (math $security_issues + 1)
    else
        echo "✅ Safety: No vulnerable dependencies found"
    end
else
    echo "⚠️  Safety report not generated"
end

echo ""
if test $security_issues -eq 0
    echo "🎉 No critical security issues found!"
else
    echo "❌ $security_issues security issue(s) detected"
    echo ""
    echo "🔧 Next steps:"
    echo "   1. Review bandit-report.json for security issues"
    echo "   2. Review safety-report.json for vulnerable dependencies"
    echo "   3. Update dependencies: pip install --upgrade -r requirements.txt"
    echo "   4. Fix any hardcoded secrets or credentials"
    echo "   5. Review and update .env configuration"
end

echo ""
echo "📋 Security best practices:"
echo "=========================="
echo "✅ Keep dependencies updated"
echo "✅ Use environment variables for secrets"
echo "✅ Enable HTTPS in production"
echo "✅ Use strong authentication"
echo "✅ Validate all input data"
echo "✅ Log security events"
echo "✅ Regular security audits"
echo ""
echo "📁 Generated reports:"
echo "   - bandit-report.json     # Security issues"
echo "   - safety-report.json     # Vulnerable dependencies"
echo "   - .secrets.baseline      # Secrets detection baseline"
