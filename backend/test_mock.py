#!/usr/bin/env python3

import asyncio
import sys
from pathlib import Path

# Add src to path
root_dir = Path(__file__).parent
src_dir = root_dir / "src"
sys.path.insert(0, str(src_dir))

# Import after path modification
from ticket_assistant.core.models import ReportRequest  # noqa: E402
from ticket_assistant.services.report_service import ReportService  # noqa: E402


async def test_mock():
    service = ReportService()
    report = ReportRequest(name="Test Report", keywords=["test"], description="Test description")
    result = await service.mock_send_report(report)
    print(f"Mock test result: {result}")


if __name__ == "__main__":
    asyncio.run(test_mock())
