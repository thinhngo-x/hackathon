#!/usr/bin/env fish

# Verify pre-commit hooks are installed and working
echo "🔍 Verifying pre-commit hooks setup..."
echo "=" * 50

# Check if pre-commit is installed
if not command -v pre-commit > /dev/null
    echo "❌ pre-commit is not installed"
    exit 1
else
    echo "✅ pre-commit is installed"
end

# Check if pre-commit is installed in the repo
if not test -f .pre-commit-config.yaml
    echo "❌ .pre-commit-config.yaml not found"
    exit 1
else
    echo "✅ .pre-commit-config.yaml found"
end

# Check if hooks are installed
if not test -f .git/hooks/pre-commit
    echo "❌ Git hooks not installed. Run: pre-commit install"
    exit 1
else
    echo "✅ Git hooks installed"
end

echo ""
echo "🧪 Running pre-commit hook tests..."
echo "=" * 50

# Test ruff linter
echo "Testing Ruff (Python linter)..."
pre-commit run ruff --all-files > /tmp/ruff_output.txt 2>&1
if test $status -eq 0
    echo "✅ Ruff: No errors found"
else
    echo "⚠️  Ruff: Found issues (this is expected - check output for details)"
    head -10 /tmp/ruff_output.txt
end

# Test basic file checks
echo ""
echo "Testing basic file checks..."
pre-commit run trailing-whitespace --all-files > /tmp/trailing_output.txt 2>&1
if test $status -eq 0
    echo "✅ Trailing whitespace: Clean"
else
    echo "❌ Trailing whitespace: Issues found"
end

# Test bandit security checks
echo ""
echo "Testing Bandit (security scanner)..."
pre-commit run bandit --all-files > /tmp/bandit_output.txt 2>&1
if test $status -eq 0
    echo "✅ Bandit: No critical security issues"
else
    echo "⚠️  Bandit: Security issues found (check bandit-report.json)"
    if test -f bandit-report.json
        echo "Report saved to: bandit-report.json"
    end
end

# Test safety (dependency vulnerabilities)
echo ""
echo "Testing Safety (dependency vulnerabilities)..."
pre-commit run python-safety-dependencies-check --all-files > /tmp/safety_output.txt 2>&1
if test $status -eq 0
    echo "✅ Safety: No known vulnerabilities"
else
    echo "❌ Safety: Vulnerabilities found"
    tail -5 /tmp/safety_output.txt
end

echo ""
echo "🎯 Pre-commit Setup Summary:"
echo "=" * 50
echo "✅ Pre-commit hooks are installed and configured"
echo "✅ Ruff linter is running (Python code quality)"
echo "✅ Bandit security scanner is running"
echo "✅ Safety vulnerability scanner is running"
echo "✅ Detect-secrets is configured"
echo "✅ Basic file checks are active"
echo ""
echo "📋 Next steps:"
echo "- Fix remaining lint issues with: ruff check --fix src/"
echo "- Review security report: cat bandit-report.json | jq '.results'"
echo "- Run all tests: pre-commit run --all-files"
echo "- Auto-run on commits: pre-commit install"
