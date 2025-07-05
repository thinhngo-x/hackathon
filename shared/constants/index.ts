// Shared constants for department information

import { Department, ErrorSeverity } from '../types/ticket';

export const DEPARTMENT_INFO = {
  [Department.BACKEND]: {
    label: 'Backend',
    description: 'Server-side logic, APIs, and database issues',
    color: '#3B82F6', // blue
    icon: 'server',
  },
  [Department.FRONTEND]: {
    label: 'Frontend',
    description: 'UI/UX, browser compatibility, and client-side issues',
    color: '#10B981', // green
    icon: 'monitor',
  },
  [Department.DATABASE]: {
    label: 'Database',
    description: 'Data storage, queries, and performance issues',
    color: '#F59E0B', // amber
    icon: 'database',
  },
  [Department.DEVOPS]: {
    label: 'DevOps',
    description: 'Infrastructure, deployment, and CI/CD issues',
    color: '#EF4444', // red
    icon: 'settings',
  },
  [Department.SECURITY]: {
    label: 'Security',
    description: 'Authentication, authorization, and security vulnerabilities',
    color: '#8B5CF6', // purple
    icon: 'shield',
  },
  [Department.API]: {
    label: 'API',
    description: 'REST APIs, GraphQL, and integration issues',
    color: '#06B6D4', // cyan
    icon: 'link',
  },
  [Department.INTEGRATION]: {
    label: 'Integration',
    description: 'Third-party services and external system issues',
    color: '#84CC16', // lime
    icon: 'plug',
  },
  [Department.GENERAL]: {
    label: 'General',
    description: 'General issues that don\'t fit other categories',
    color: '#6B7280', // gray
    icon: 'help-circle',
  },
} as const;

export const SEVERITY_INFO = {
  [ErrorSeverity.LOW]: {
    label: 'Low',
    description: 'Minor issues with workarounds available',
    color: '#10B981', // green
    priority: 1,
  },
  [ErrorSeverity.MEDIUM]: {
    label: 'Medium',
    description: 'Moderate impact on functionality',
    color: '#F59E0B', // amber
    priority: 2,
  },
  [ErrorSeverity.HIGH]: {
    label: 'High',
    description: 'Significant impact on users or systems',
    color: '#EF4444', // red
    priority: 3,
  },
  [ErrorSeverity.CRITICAL]: {
    label: 'Critical',
    description: 'System down or major functionality broken',
    color: '#DC2626', // red-600
    priority: 4,
  },
} as const;

export const API_ENDPOINTS = {
  HEALTH: '/health',
  TICKETS: '/api/tickets',
  SUBMIT_REPORT: '/api/reports/submit',
  CLASSIFY_ERROR: '/api/classification/classify',
  COMBINED_SUBMIT: '/api/combined/submit-and-classify',
} as const;

export const ROUTES = {
  HOME: '/',
  DASHBOARD: '/dashboard',
  SUBMIT: '/submit',
  TICKETS: '/tickets',
  TICKET_DETAIL: '/tickets/[id]',
  REPORTS: '/reports',
} as const;
