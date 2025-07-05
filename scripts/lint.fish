#!/usr/bin/env fish

# Fish Shell Linting Script for Ticket Assistant

echo "🧹 Running linting and formatting checks..."

# Change to backend directory
cd backend

# Check if we're in the backend directory
if not test -f "pyproject.toml"
    echo "❌ Not in the backend directory or pyproject.toml not found"
    exit 1
end

# Activate virtual environment
source .venv/bin/activate.fish
set -x PYTHONPATH (pwd)/src

echo "🎯 Running Ruff checks..."
echo "=================="

# Run Ruff linter
echo "🔍 Running Ruff linter..."
ruff check src/ tests/ --fix || set -l ruff_exit_code $status

# Run Ruff formatter
echo "🎨 Running Ruff formatter..."
ruff format src/ tests/ || set -l ruff_format_exit_code $status

echo ""
echo "🛡️  Running security checks..."
echo "======================="

# Run Bandit security checks
echo "🔒 Running Bandit security scan..."
bandit -r src/ -f json -o bandit-report.json || set -l bandit_exit_code $status

# Run Safety dependency check
echo "🔍 Checking for known security vulnerabilities..."
safety check -r requirements.txt || set -l safety_exit_code $status

echo ""
echo "🔍 Running type checks..."
echo "==================="

# Run MyPy type checking
echo "📝 Running MyPy type checker..."
mypy src/ --ignore-missing-imports --no-strict-optional || set -l mypy_exit_code $status

echo ""
echo "📝 Running docstring checks..."
echo "=========================="

# Run pydocstyle
echo "📚 Checking docstring style..."
pydocstyle src/ --convention=google || set -l pydocstyle_exit_code $status

echo ""
echo "🔍 Running secrets detection..."
echo "============================"

# Run detect-secrets
echo "🕵️  Scanning for secrets..."
detect-secrets scan --baseline .secrets.baseline || set -l secrets_exit_code $status

echo ""
echo "📊 Lint Summary:"
echo "================"

# Check results
set -l total_errors 0

if set -q ruff_exit_code
    echo "❌ Ruff linter: FAILED"
    set total_errors (math $total_errors + 1)
else
    echo "✅ Ruff linter: PASSED"
end

if set -q ruff_format_exit_code
    echo "❌ Ruff formatter: FAILED"
    set total_errors (math $total_errors + 1)
else
    echo "✅ Ruff formatter: PASSED"
end

if set -q bandit_exit_code
    echo "❌ Bandit security: FAILED"
    set total_errors (math $total_errors + 1)
else
    echo "✅ Bandit security: PASSED"
end

if set -q safety_exit_code
    echo "❌ Safety check: FAILED"
    set total_errors (math $total_errors + 1)
else
    echo "✅ Safety check: PASSED"
end

if set -q mypy_exit_code
    echo "❌ MyPy type check: FAILED"
    set total_errors (math $total_errors + 1)
else
    echo "✅ MyPy type check: PASSED"
end

if set -q pydocstyle_exit_code
    echo "❌ Docstring style: FAILED"
    set total_errors (math $total_errors + 1)
else
    echo "✅ Docstring style: PASSED"
end

if set -q secrets_exit_code
    echo "❌ Secrets detection: FAILED"
    set total_errors (math $total_errors + 1)
else
    echo "✅ Secrets detection: PASSED"
end

echo ""
if test $total_errors -eq 0
    echo "🎉 All linting checks passed!"
else
    echo "❌ $total_errors linting check(s) failed"
    echo ""
    echo "💡 Tips:"
    echo "   - Check bandit-report.json for security issues"
    echo "   - Run 'ruff check src/ tests/ --fix' to auto-fix issues"
    echo "   - Run 'ruff format src/ tests/' to format code"
    echo "   - Use 'pre-commit run --all-files' to run all checks"
end

echo ""
echo "🔧 Additional commands:"
echo "   ruff check src/ tests/ --fix    # Fix linting issues"
echo "   ruff format src/ tests/         # Format code"
echo "   pre-commit run --all-files      # Run all pre-commit hooks"
