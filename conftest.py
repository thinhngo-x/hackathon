"""Pytest configuration and fixtures."""

import pytest
import sys
from pathlib import Path

# Add src directory to Python path for all tests
root_dir = Path(__file__).parent.parent
src_dir = root_dir / "src"
sys.path.insert(0, str(src_dir))


@pytest.fixture(scope="session")
def project_root():
    """Project root directory fixture."""
    return root_dir


@pytest.fixture(scope="session") 
def src_dir():
    """Source directory fixture."""
    return root_dir / "src"


@pytest.fixture(autouse=True)
def setup_test_environment():
    """Setup test environment for each test."""
    # Any test setup can go here
    yield
    # Any test teardown can go here
