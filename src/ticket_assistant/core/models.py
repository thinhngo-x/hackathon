from typing import List, Optional
from pydantic import BaseModel
from enum import Enum


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
    keywords: List[str]
    description: str
    error_message: Optional[str] = None
    screenshot_url: Optional[str] = None


class ReportResponse(BaseModel):
    success: bool
    message: str
    ticket_id: Optional[str] = None


class ClassificationRequest(BaseModel):
    error_description: str
    error_message: Optional[str] = None
    context: Optional[str] = None


class ClassificationResponse(BaseModel):
    department: Department
    severity: ErrorSeverity
    confidence: float
    reasoning: str
    suggested_actions: List[str]


class TicketData(BaseModel):
    id: str
    name: str
    keywords: List[str]
    description: str
    department: Department
    severity: ErrorSeverity
    status: str = "open"
    created_at: str
