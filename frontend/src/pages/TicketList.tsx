import type { Department, ErrorSeverity, Ticket, TicketStatus } from '@shared/types/ticket';
import { useQuery } from '@tanstack/react-query';
import {
    AlertCircle,
    Calendar,
    CheckCircle,
    Clock,
    Eye,
    Filter,
    Search,
    SortAsc, SortDesc,
    XCircle
} from 'lucide-react';
import React, { useMemo, useState } from 'react';
import { Link } from 'react-router-dom';
import { ticketAssistantAPI } from '../lib/api/client';
import { useToastContext } from '../lib/contexts/ToastContext';
import { departmentOptions, severityOptions } from '../lib/schemas/ticketSchema';

const TicketList: React.FC = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState<TicketStatus | ''>('');
  const [departmentFilter, setDepartmentFilter] = useState<Department | ''>('');
  const [severityFilter, setSeverityFilter] = useState<ErrorSeverity | ''>('');
  const [sortBy, setSortBy] = useState<'created_at' | 'updated_at' | 'severity'>('created_at');
  const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('desc');
  const { info } = useToastContext();

  const { data: tickets, isLoading, error } = useQuery<Ticket[]>({
    queryKey: ['tickets'],
    queryFn: () => ticketAssistantAPI.getTickets(),
    staleTime: 30000,
  });

  // Mock data for development
  const mockTickets: Ticket[] = [
    {
      id: 'TK-001',
      name: 'John Doe',
      description: 'Unable to login to dashboard after entering correct credentials',
      keywords: ['login', 'authentication', 'dashboard'],
      department: 'backend' as Department,
      severity: 'high' as ErrorSeverity,
      status: 'open' as TicketStatus,
      created_at: new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString(),
      updated_at: new Date(Date.now() - 1 * 60 * 60 * 1000).toISOString(),
      assignee: 'Alice Johnson'
    },
    {
      id: 'TK-002',
      name: 'Jane Smith',
      description: 'Intermittent network connectivity issues affecting productivity',
      keywords: ['network', 'connectivity', 'intermittent'],
      department: 'devops' as Department,
      severity: 'medium' as ErrorSeverity,
      status: 'in_progress' as TicketStatus,
      created_at: new Date(Date.now() - 4 * 60 * 60 * 1000).toISOString(),
      updated_at: new Date(Date.now() - 30 * 60 * 1000).toISOString(),
      assignee: 'Bob Wilson'
    },
    {
      id: 'TK-003',
      name: 'Mike Johnson',
      description: 'Database query performance is extremely slow',
      keywords: ['database', 'performance', 'query'],
      department: 'database' as Department,
      severity: 'critical' as ErrorSeverity,
      status: 'resolved' as TicketStatus,
      created_at: new Date(Date.now() - 6 * 60 * 60 * 1000).toISOString(),
      updated_at: new Date(Date.now() - 10 * 60 * 1000).toISOString(),
      assignee: 'Carol Davis'
    },
    {
      id: 'TK-004',
      name: 'Sarah Brown',
      description: 'Frontend component not rendering correctly on mobile devices',
      keywords: ['frontend', 'mobile', 'rendering'],
      department: 'frontend' as Department,
      severity: 'low' as ErrorSeverity,
      status: 'pending' as TicketStatus,
      created_at: new Date(Date.now() - 8 * 60 * 60 * 1000).toISOString(),
      updated_at: new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString(),
    },
    {
      id: 'TK-005',
      name: 'David Lee',
      description: 'Security vulnerability found in user authentication system',
      keywords: ['security', 'vulnerability', 'authentication'],
      department: 'security' as Department,
      severity: 'critical' as ErrorSeverity,
      status: 'open' as TicketStatus,
      created_at: new Date(Date.now() - 12 * 60 * 60 * 1000).toISOString(),
      updated_at: new Date(Date.now() - 5 * 60 * 60 * 1000).toISOString(),
      assignee: 'Eve Martinez'
    }
  ];

  const displayTickets = tickets || mockTickets;

  const filteredAndSortedTickets = useMemo(() => {
    const filtered = displayTickets.filter(ticket => {
      const matchesSearch = searchTerm === '' ||
                           ticket.description.toLowerCase().includes(searchTerm.toLowerCase()) ||
                           ticket.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                           ticket.id.toLowerCase().includes(searchTerm.toLowerCase()) ||
                           ticket.keywords.some(keyword => keyword.toLowerCase().includes(searchTerm.toLowerCase())) ||
                           (ticket.assignee && ticket.assignee.toLowerCase().includes(searchTerm.toLowerCase()));

      const matchesStatus = !statusFilter || ticket.status === statusFilter;
      const matchesDepartment = !departmentFilter || ticket.department === departmentFilter;
      const matchesSeverity = !severityFilter || ticket.severity === severityFilter;

      return matchesSearch && matchesStatus && matchesDepartment && matchesSeverity;
    });

    // Sort tickets
    filtered.sort((a, b) => {
      let aValue: string | number;
      let bValue: string | number;

      switch (sortBy) {
        case 'created_at':
          aValue = new Date(a.created_at).getTime();
          bValue = new Date(b.created_at).getTime();
          break;
        case 'updated_at':
          aValue = new Date(a.updated_at).getTime();
          bValue = new Date(b.updated_at).getTime();
          break;
        case 'severity': {
          const severityOrder = { critical: 4, high: 3, medium: 2, low: 1 };
          aValue = severityOrder[a.severity as keyof typeof severityOrder];
          bValue = severityOrder[b.severity as keyof typeof severityOrder];
          break;
        }
        default:
          aValue = a.created_at;
          bValue = b.created_at;
      }

      if (sortOrder === 'desc') {
        return bValue > aValue ? 1 : -1;
      }
      return aValue > bValue ? 1 : -1;
    });

    return filtered;
  }, [displayTickets, searchTerm, statusFilter, departmentFilter, severityFilter, sortBy, sortOrder]);

  const getStatusIcon = (status: TicketStatus) => {
    switch (status) {
      case 'open':
        return <AlertCircle className="w-4 h-4 text-red-500" />;
      case 'in_progress':
        return <Clock className="w-4 h-4 text-yellow-500" />;
      case 'resolved':
        return <CheckCircle className="w-4 h-4 text-green-500" />;
      case 'closed':
        return <XCircle className="w-4 h-4 text-gray-500" />;
      default:
        return <Clock className="w-4 h-4 text-blue-500" />;
    }
  };

  const getStatusColor = (status: TicketStatus) => {
    switch (status) {
      case 'open':
        return 'bg-red-100 text-red-800';
      case 'in_progress':
        return 'bg-yellow-100 text-yellow-800';
      case 'resolved':
        return 'bg-green-100 text-green-800';
      case 'closed':
        return 'bg-gray-100 text-gray-800';
      default:
        return 'bg-blue-100 text-blue-800';
    }
  };

  const getSeverityColor = (severity: ErrorSeverity) => {
    switch (severity) {
      case 'low':
        return 'bg-green-100 text-green-800';
      case 'medium':
        return 'bg-yellow-100 text-yellow-800';
      case 'high':
        return 'bg-orange-100 text-orange-800';
      case 'critical':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const formatRelativeTime = (isoString: string) => {
    const now = new Date();
    const date = new Date(isoString);
    const diffMs = now.getTime() - date.getTime();
    const diffHours = Math.floor(diffMs / (1000 * 60 * 60));
    const diffDays = Math.floor(diffHours / 24);

    if (diffDays > 0) {
      return `${diffDays} day${diffDays > 1 ? 's' : ''} ago`;
    } else if (diffHours > 0) {
      return `${diffHours} hour${diffHours > 1 ? 's' : ''} ago`;
    } else {
      const diffMinutes = Math.floor(diffMs / (1000 * 60));
      return `${diffMinutes} minute${diffMinutes > 1 ? 's' : ''} ago`;
    }
  };

  const toggleSort = (column: typeof sortBy) => {
    if (sortBy === column) {
      setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc');
    } else {
      setSortBy(column);
      setSortOrder('desc');
    }
  };

  if (isLoading) {
    return (
      <div className="space-y-6">
        <div className="animate-pulse">
          <div className="h-8 bg-muted rounded w-48 mb-6"></div>
          <div className="bg-card rounded-lg card-shadow p-4">
            <div className="space-y-4">
              {[1, 2, 3, 4, 5].map((i) => (
                <div key={i} className="flex space-x-4">
                  <div className="h-4 bg-muted rounded w-16"></div>
                  <div className="h-4 bg-muted rounded w-48"></div>
                  <div className="h-4 bg-muted rounded w-24"></div>
                  <div className="h-4 bg-muted rounded w-32"></div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="space-y-6">
        <div className="bg-destructive/10 border border-destructive/20 rounded-lg p-4">
          <div className="flex items-center gap-2">
            <AlertCircle className="w-5 h-5 text-destructive" />
            <span className="text-destructive">Failed to load tickets</span>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold text-foreground">All Tickets</h1>
        <div className="text-sm text-muted-foreground">
          Showing {filteredAndSortedTickets.length} of {displayTickets.length} tickets
        </div>
      </div>

      {/* Filters */}
      <div className="bg-card p-4 rounded-lg card-shadow border border-border space-y-4">
        <div className="flex items-center gap-2 mb-4">
          <Filter className="w-5 h-5 text-muted-foreground" />
          <h2 className="text-lg font-semibold text-card-foreground">Filters</h2>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
          {/* Search */}
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-muted-foreground" />
            <input
              type="text"
              placeholder="Search tickets..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-10 pr-4 py-2 border border-input rounded-lg bg-background text-foreground focus:ring-2 focus:ring-ring focus:border-ring"
            />
          </div>

          {/* Status Filter */}
          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value as TicketStatus | '')}
            className="w-full px-3 py-2 border border-input rounded-lg bg-background text-foreground focus:ring-2 focus:ring-ring focus:border-ring"
          >
            <option value="">All Statuses</option>
            <option value="open">Open</option>
            <option value="in_progress">In Progress</option>
            <option value="pending">Pending</option>
            <option value="resolved">Resolved</option>
            <option value="closed">Closed</option>
          </select>

          {/* Department Filter */}
          <select
            value={departmentFilter}
            onChange={(e) => setDepartmentFilter(e.target.value as Department | '')}
            className="w-full px-3 py-2 border border-input rounded-lg bg-background text-foreground focus:ring-2 focus:ring-ring focus:border-ring"
          >
            <option value="">All Departments</option>
            {departmentOptions.map(dept => (
              <option key={dept.value} value={dept.value}>{dept.label}</option>
            ))}
          </select>

          {/* Severity Filter */}
          <select
            value={severityFilter}
            onChange={(e) => setSeverityFilter(e.target.value as ErrorSeverity | '')}
            className="w-full px-3 py-2 border border-input rounded-lg bg-background text-foreground focus:ring-2 focus:ring-ring focus:border-ring"
          >
            <option value="">All Severities</option>
            {severityOptions.map(severity => (
              <option key={severity.value} value={severity.value}>{severity.label}</option>
            ))}
          </select>

          {/* Clear Filters */}
          <button
            onClick={() => {
              setSearchTerm('');
              setStatusFilter('');
              setDepartmentFilter('');
              setSeverityFilter('');
              info('Filters Cleared', 'All filters have been reset');
            }}
            className="px-4 py-2 bg-muted text-muted-foreground rounded-lg hover:bg-accent hover:text-accent-foreground transition-colors"
          >
            Clear Filters
          </button>
        </div>
      </div>

      {/* Tickets Table */}
      <div className="bg-card rounded-lg card-shadow border border-border overflow-x-auto">
        <table className="min-w-full divide-y divide-border">
          <thead className="bg-muted/50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider w-20">
                ID
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider min-w-80">
                Title & Reporter
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider w-32">
                Status
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider w-28">
                Department
              </th>
              <th
                className="px-6 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider cursor-pointer hover:bg-accent w-24"
                onClick={() => toggleSort('severity')}
              >
                <div className="flex items-center gap-1">
                  Severity
                  {sortBy === 'severity' && (
                    sortOrder === 'asc' ? <SortAsc className="w-3 h-3" /> : <SortDesc className="w-3 h-3" />
                  )}
                </div>
              </th>
              <th
                className="px-6 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider cursor-pointer hover:bg-accent w-32"
                onClick={() => toggleSort('created_at')}
              >
                <div className="flex items-center gap-1">
                  Created
                  {sortBy === 'created_at' && (
                    sortOrder === 'asc' ? <SortAsc className="w-3 h-3" /> : <SortDesc className="w-3 h-3" />
                  )}
                </div>
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider w-32">
                Assignee
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider w-24">
                Actions
              </th>
            </tr>
          </thead>
          <tbody className="bg-card divide-y divide-border">
            {filteredAndSortedTickets.map((ticket) => (
              <tr key={ticket.id} className="hover:bg-accent/50 transition-colors">
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="text-sm font-medium text-card-foreground">{ticket.id}</div>
                </td>
                <td className="px-6 py-4">
                  <div className="text-sm font-medium text-card-foreground">
                    {ticket.description}
                  </div>
                  <div className="text-sm text-muted-foreground">
                    Reporter: {ticket.name}
                  </div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="flex items-center gap-2">
                    {getStatusIcon(ticket.status)}
                    <span className={`px-2 py-1 text-xs font-semibold rounded-full ${getStatusColor(ticket.status)}`}>
                      {ticket.status ? ticket.status.replace('_', ' ').toUpperCase() : 'UNKNOWN'}
                    </span>
                  </div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="text-sm text-card-foreground">
                    {departmentOptions.find(d => d.value === ticket.department)?.label || ticket.department}
                  </div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <span className={`px-2 py-1 text-xs font-semibold rounded-full ${getSeverityColor(ticket.severity)}`}>
                    {ticket.severity ? ticket.severity.toUpperCase() : 'UNKNOWN'}
                  </span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="flex items-center gap-1 text-sm text-muted-foreground">
                    <Calendar className="w-4 h-4" />
                    {formatRelativeTime(ticket.created_at)}
                  </div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-card-foreground">
                  {ticket.assignee || 'Unassigned'}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                  <Link
                    to={`/tickets/${ticket.id}`}
                    className="text-primary hover:text-primary/80 flex items-center gap-1 transition-colors"
                  >
                    <Eye className="w-4 h-4" />
                    View
                  </Link>
                </td>
              </tr>
            ))}
          </tbody>
        </table>

        {filteredAndSortedTickets.length === 0 && (
          <div className="p-8 text-center">
            <AlertCircle className="w-12 h-12 text-muted-foreground mx-auto mb-4" />
            <p className="text-muted-foreground">
              {searchTerm || statusFilter || departmentFilter || severityFilter
                ? 'No tickets match your current filters'
                : 'No tickets found'
              }
            </p>
          </div>
        )}
      </div>
    </div>
  );
};

export default TicketList;
