import type { Department, ErrorSeverity, TicketStatus } from './ticket';

export interface TicketResponse {
  id: string;
  name: string;
  description: string;
  keywords: string[];
  department: Department;
  severity: ErrorSeverity;
  status: TicketStatus;
  created_at: string;
  updated_at: string;
  assignee?: string;
  title?: string;
  reporter?: string;
  reporter_email?: string;
  classification?: {
    department: string;
    confidence: number;
    priority: string;
  };
}

export interface DashboardStats {
  total_tickets: number;
  open_tickets: number;
  resolved_tickets: number;
  average_resolution_time: string;
  classification_accuracy: number;
  department_distribution: Record<string, number>;
}

export interface HealthCheckResponse {
  status: string;
  message?: string;
  services?: {
    report_service: boolean;
    groq_classifier: boolean;
  };
}

export interface ApiError {
  detail: string;
  error_code?: string;
  timestamp?: string;
}
