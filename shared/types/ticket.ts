// Shared TypeScript types for Ticket Assistant

export enum ErrorSeverity {
  LOW = "low",
  MEDIUM = "medium",
  HIGH = "high",
  CRITICAL = "critical",
}

export enum Department {
  BACKEND = "backend",
  FRONTEND = "frontend",
  DATABASE = "database",
  DEVOPS = "devops",
  SECURITY = "security",
  API = "api",
  INTEGRATION = "integration",
  GENERAL = "general",
}

export enum TicketStatus {
  OPEN = "open",
  IN_PROGRESS = "in_progress",
  PENDING = "pending",
  RESOLVED = "resolved",
  CLOSED = "closed",
}

export interface ReportRequest {
  name: string;
  keywords: string[];
  description: string;
  error_message?: string;
  screenshot_url?: string;
}

export interface ReportResponse {
  success: boolean;
  message: string;
  ticket_id?: string;
}

export interface ClassificationRequest {
  error_description: string;
  error_message?: string;
  context?: string;
}

export interface ClassificationResponse {
  department: Department;
  severity: ErrorSeverity;
  confidence: number;
  reasoning: string;
  suggested_actions: string[];
}

export interface Ticket {
  id: string;
  name: string;
  description: string;
  error_message?: string;
  keywords: string[];
  department: Department;
  severity: ErrorSeverity;
  status: TicketStatus;
  created_at: string;
  updated_at: string;
  assignee?: string;
  screenshot_url?: string;
}

export interface TicketFilters {
  department?: Department;
  severity?: ErrorSeverity;
  status?: TicketStatus;
  search?: string;
  assignee?: string;
  date_from?: string;
  date_to?: string;
}

export interface TicketList {
  tickets: Ticket[];
  total: number;
  page: number;
  per_page: number;
  total_pages: number;
}

export interface DashboardStats {
  total_tickets: number;
  open_tickets: number;
  resolved_tickets: number;
  average_resolution_time: number;
  classification_accuracy: number;
  department_distribution: Record<Department, number>;
  severity_distribution: Record<ErrorSeverity, number>;
}
