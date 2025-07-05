from enum import Enum

from pydantic import BaseModel


class ErrorSeverity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Department(str, Enum):
    BACKEND = "backend"
    FRONTEND = "frontend"
    DATABASE = "database"
    DEVOPS = "devops"
    SECURITY = "security"
    API = "api"
    INTEGRATION = "integration"
    GENERAL = "general"


class ReportRequest(BaseModel):
    name: str
    keywords: list[str]
    description: str
    error_message: str | None = None
    screenshot_url: str | None = None


class ReportResponse(BaseModel):
    success: bool
    message: str
    ticket_id: str | None = None


class ClassificationRequest(BaseModel):
    error_description: str
    error_message: str | None = None
    context: str | None = None


class ClassificationResponse(BaseModel):
    department: Department
    severity: ErrorSeverity
    confidence: float
    reasoning: str
    suggested_actions: list[str]


class TicketData(BaseModel):
    id: str
    name: str
    keywords: list[str]
    description: str
    department: Department
    severity: ErrorSeverity
    status: str = "open"
    created_at: str
