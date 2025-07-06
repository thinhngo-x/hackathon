#!/usr/bin/env python3
"""
Quick test script - Runs the most common test scenarios
"""

import subprocess
import sys
from pathlib import Path

def main():
    """Run quick tests."""
    tests_dir = Path(__file__).parent
    runner = tests_dir / "run_tests.py"
    
    print("🚀 Running Quick Test Suite")
    print("=" * 40)
    
    # Run setup and health checks
    result = subprocess.run([
        sys.executable, str(runner), "--setup", "--health"
    ], cwd=tests_dir)
    
    if result.returncode == 0:
        print("\n✅ Quick tests passed!")
        print("💡 For more options, run: python run_tests.py --help")
    else:
        print("\n❌ Quick tests failed!")
        print("💡 For detailed testing, run: python run_tests.py --all")
    
    return result.returncode

if __name__ == "__main__":
    sys.exit(main())
