import type { TicketResponse } from '@shared/types/api';
import type { TicketStatus } from '@shared/types/ticket';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import {
  AlertCircle,
  ArrowLeft,
  Calendar,
  CheckCircle,
  Clock,
  Mail,
  Pause,
  Play,
  Tag,
  User,
  XCircle
} from 'lucide-react';
import React from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { ErrorBoundary } from '../components/ErrorBoundary';
import { ticketAssistantAPI } from '../lib/api';
import { useToastContext } from '../lib/contexts/ToastContext';
import { departmentOptions, severityOptions } from '../lib/schemas/ticketSchema';

const TicketDetails: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const { success, error: showError } = useToastContext();

  const { data: ticket, isLoading, error } = useQuery<TicketResponse>({
    queryKey: ['ticket', id],
    queryFn: () => ticketAssistantAPI.getTicketById(id!),
    enabled: !!id,
    staleTime: 30000,
  });

  const updateStatusMutation = useMutation({
    mutationFn: async (newStatus: string) => {
      return await ticketAssistantAPI.updateTicketStatus(id!, newStatus as TicketStatus);
    },
    onSuccess: (_, newStatus) => {
      queryClient.invalidateQueries({ queryKey: ['ticket', id] });
      queryClient.invalidateQueries({ queryKey: ['tickets'] });
      success('Status Updated', `Ticket status has been updated to ${newStatus}`);
    },
    onError: (err) => {
      showError('Update Failed', err instanceof Error ? err.message : 'Failed to update ticket status');
    }
  });

  const getDepartmentLabel = (dept: string) => {
    return departmentOptions.find(d => d.value === dept)?.label || dept;
  };

  const getSeverityInfo = (severity: string) => {
    return severityOptions.find(s => s.value === severity) || { label: severity, color: 'text-gray-600' };
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'open':
        return <AlertCircle className="w-5 h-5 text-red-500" />;
      case 'in_progress':
        return <Play className="w-5 h-5 text-yellow-500" />;
      case 'pending':
        return <Pause className="w-5 h-5 text-blue-500" />;
      case 'resolved':
        return <CheckCircle className="w-5 h-5 text-green-500" />;
      case 'closed':
        return <XCircle className="w-5 h-5 text-gray-500" />;
      default:
        return <Clock className="w-5 h-5 text-gray-400" />;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'open':
        return 'bg-red-100 dark:bg-red-900/20 text-red-800 dark:text-red-200 border-red-200 dark:border-red-700';
      case 'in_progress':
        return 'bg-yellow-100 dark:bg-yellow-900/20 text-yellow-800 dark:text-yellow-200 border-yellow-200 dark:border-yellow-700';
      case 'pending':
        return 'bg-blue-100 dark:bg-blue-900/20 text-blue-800 dark:text-blue-200 border-blue-200 dark:border-blue-700';
      case 'resolved':
        return 'bg-green-100 dark:bg-green-900/20 text-green-800 dark:text-green-200 border-green-200 dark:border-green-700';
      case 'closed':
        return 'bg-gray-100 dark:bg-gray-800 text-gray-800 dark:text-gray-200 border-gray-200 dark:border-gray-700';
      default:
        return 'bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-400 border-gray-200 dark:border-gray-700';
    }
  };

  const formatDate = (isoString: string) => {
    return new Date(isoString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const handleStatusUpdate = (newStatus: string) => {
    updateStatusMutation.mutate(newStatus);
  };

  if (isLoading) {
    return (
      <div className="p-6 min-h-screen bg-gray-50 dark:bg-gray-900">
        <div className="animate-pulse">
          <div className="flex items-center gap-4 mb-6">
            <div className="h-6 w-6 bg-gray-200 dark:bg-gray-700 rounded"></div>
            <div className="h-8 bg-gray-200 dark:bg-gray-700 rounded w-48"></div>
          </div>
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6 space-y-4">
            <div className="h-6 bg-gray-200 dark:bg-gray-700 rounded w-3/4"></div>
            <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded w-1/2"></div>
            <div className="h-20 bg-gray-200 dark:bg-gray-700 rounded"></div>
          </div>
        </div>
      </div>
    );
  }

  if (error || !ticket) {
    return (
      <div className="p-6 min-h-screen bg-gray-50 dark:bg-gray-900">
        <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-700 rounded-lg p-6">
          <div className="flex items-center gap-2 mb-4">
            <AlertCircle className="w-6 h-6 text-red-600 dark:text-red-400" />
            <h2 className="text-lg font-semibold text-red-800 dark:text-red-200">Ticket Not Found</h2>
          </div>
          <p className="text-red-700 dark:text-red-300 mb-4">
            The ticket you're looking for doesn't exist or couldn't be loaded.
          </p>
          <button
            onClick={() => navigate('/tickets')}
            className="flex items-center gap-2 px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg transition-colors"
          >
            <ArrowLeft className="w-4 h-4" />
            Back to Tickets
          </button>
        </div>
      </div>
    );
  }

  const severityInfo = getSeverityInfo(ticket.severity);

  return (
    <div className="min-h-screen bg-background">
      {/* Enhanced Header with Status Bar */}
      <div className="bg-card shadow-sm border-b border-border sticky top-0 z-10">
        <div className="max-w-6xl mx-auto px-6 py-4">
          <div className="flex items-center gap-4">
            <button
              onClick={() => navigate('/tickets')}
              className="p-2 hover:bg-accent rounded-lg transition-colors"
            >
              <ArrowLeft className="w-5 h-5 text-muted-foreground" />
            </button>
            <div className="flex-1">
              <div className="flex items-center gap-3">
                <h1 className="text-3xl font-bold text-foreground">Ticket {ticket.id}</h1>
                <div className="flex items-center gap-2">
                  {getStatusIcon(ticket.status)}
                  <span className={`px-3 py-1 text-sm font-semibold rounded-full border ${getStatusColor(ticket.status)}`}>
                    {ticket.status.replace('_', ' ').toUpperCase()}
                  </span>
                </div>
              </div>
              <p className="text-lg text-muted-foreground mt-1">{ticket.title || ticket.description.substring(0, 100)}...</p>
            </div>
            <div className="text-right">
              <div className="text-sm text-muted-foreground">Priority</div>
              <div className={`text-lg font-bold ${getSeverityInfo(ticket.severity).color}`}>
                {getSeverityInfo(ticket.severity).label}
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-6xl mx-auto px-6 py-6 space-y-6">

        {/* Main Content */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Ticket Details */}
          <div className="lg:col-span-2 space-y-6">
            {/* Description */}
            <div className="bg-card rounded-xl shadow-sm border border-border p-6">
              <div className="flex items-center gap-3 mb-4">
                <div className="w-10 h-10 bg-primary/10 rounded-lg flex items-center justify-center">
                  <Clock className="w-5 h-5 text-primary" />
                </div>
                <h2 className="text-xl font-semibold text-foreground">Description</h2>
              </div>
              <div className="prose prose-gray dark:prose-invert max-w-none">
                <p className="text-muted-foreground leading-relaxed whitespace-pre-wrap text-base">
                  {ticket.description}
                </p>
              </div>
            </div>

            {/* Keywords */}
            {ticket.keywords && ticket.keywords.length > 0 && (
              <div className="bg-card rounded-xl shadow-sm border border-border p-6">
                <div className="flex items-center gap-3 mb-4">
                  <div className="w-10 h-10 bg-purple-100 dark:bg-purple-900/30 rounded-lg flex items-center justify-center">
                    <Tag className="w-5 h-5 text-purple-600 dark:text-purple-400" />
                  </div>
                  <h2 className="text-xl font-semibold text-foreground">Keywords</h2>
                </div>
                <div className="flex flex-wrap gap-2">
                  {ticket.keywords.map((keyword, index) => (
                    <span
                      key={index}
                      className="px-3 py-1 bg-secondary text-secondary-foreground text-sm rounded-full font-medium hover:bg-secondary/80 transition-colors"
                    >
                      {keyword}
                    </span>
                  ))}
                </div>
              </div>
            )}

            {/* AI Classification */}
            {ticket.classification && (
              <div className="bg-gradient-to-br from-primary/5 via-primary/10 to-purple-500/5 border border-border rounded-xl p-6 shadow-sm">
                <div className="flex items-center gap-3 mb-4">
                  <div className="w-10 h-10 bg-gradient-to-r from-blue-500 to-purple-500 rounded-lg flex items-center justify-center">
                    <CheckCircle className="w-5 h-5 text-white" />
                  </div>
                  <h2 className="text-xl font-semibold text-foreground">AI Classification</h2>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div className="bg-card/60 backdrop-blur-sm rounded-lg p-4">
                    <div className="text-sm font-medium text-muted-foreground mb-1">Department</div>
                    <div className="text-2xl font-bold text-foreground">
                      {ticket.classification.department}
                    </div>
                  </div>
                  <div className="bg-card/60 backdrop-blur-sm rounded-lg p-4">
                    <div className="text-sm font-medium text-muted-foreground mb-1">Confidence</div>
                    <div className="flex items-center gap-2">
                      <div className="text-2xl font-bold text-primary">
                        {(ticket.classification.confidence * 100).toFixed(1)}%
                      </div>
                      <div className="flex-1 bg-secondary rounded-full h-2">
                        <div
                          className="bg-gradient-to-r from-blue-500 to-purple-500 h-2 rounded-full transition-all duration-300"
                          style={{ width: `${ticket.classification.confidence * 100}%` }}
                        />
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* Enhanced Sidebar */}
          <div className="space-y-6">
            {/* Status and Actions */}
            <div className="bg-card rounded-xl shadow-sm border border-border p-6">
              <h3 className="text-xl font-semibold text-foreground mb-4 flex items-center gap-2">
                <div className="w-8 h-8 bg-green-100 dark:bg-green-900/30 rounded-lg flex items-center justify-center">
                  <CheckCircle className="w-4 h-4 text-green-600 dark:text-green-400" />
                </div>
                Status & Actions
              </h3>

              <div className="space-y-4">
                <div className="flex items-center gap-3 p-3 bg-muted rounded-lg">
                  {getStatusIcon(ticket.status)}
                  <span className={`px-3 py-1 text-sm font-semibold rounded-full border ${getStatusColor(ticket.status)}`}>
                    {ticket.status.replace('_', ' ').toUpperCase()}
                  </span>
                </div>

                <div className="space-y-2">
                  <label className="text-sm font-medium text-muted-foreground">Update Status:</label>
                  <select
                    value={ticket.status}
                    onChange={(e) => handleStatusUpdate(e.target.value)}
                    disabled={updateStatusMutation.isPending}
                    className="w-full px-3 py-2 border border-input rounded-lg focus:ring-2 focus:ring-primary focus:border-primary bg-background text-foreground text-sm"
                  >
                    <option value="open">Open</option>
                    <option value="in_progress">In Progress</option>
                    <option value="pending">Pending</option>
                    <option value="resolved">Resolved</option>
                    <option value="closed">Closed</option>
                  </select>
                </div>
              </div>
            </div>

            {/* Ticket Information */}
            <div className="bg-card rounded-xl shadow-sm border border-border p-6">
              <h3 className="text-xl font-semibold text-foreground mb-4 flex items-center gap-2">
                <div className="w-8 h-8 bg-primary/10 rounded-lg flex items-center justify-center">
                  <User className="w-4 h-4 text-primary" />
                </div>
                Ticket Information
              </h3>

              <div className="space-y-4">
                <div className="flex items-start gap-3 p-3 bg-muted rounded-lg">
                  <div className="w-8 h-8 bg-muted-foreground/10 rounded-full flex items-center justify-center">
                    <User className="w-4 h-4 text-muted-foreground" />
                  </div>
                  <div className="flex-1">
                    <div className="text-sm font-medium text-muted-foreground">Reporter</div>
                    <div className="text-base font-semibold text-foreground">{ticket.name}</div>
                  </div>
                </div>

                {ticket.reporter_email && (
                  <div className="flex items-start gap-3 p-3 bg-muted rounded-lg">
                    <div className="w-8 h-8 bg-muted-foreground/10 rounded-full flex items-center justify-center">
                      <Mail className="w-4 h-4 text-muted-foreground" />
                    </div>
                    <div className="flex-1">
                      <div className="text-sm font-medium text-muted-foreground">Email</div>
                      <div className="text-base font-semibold text-foreground">{ticket.reporter_email}</div>
                    </div>
                  </div>
                )}

                <div className="flex items-start gap-3 p-3 bg-muted rounded-lg">
                  <div className="w-8 h-8 bg-muted-foreground/10 rounded-full flex items-center justify-center">
                    <Tag className="w-4 h-4 text-muted-foreground" />
                  </div>
                  <div className="flex-1">
                    <div className="text-sm font-medium text-muted-foreground">Department</div>
                    <div className="text-base font-semibold text-foreground">{getDepartmentLabel(ticket.department)}</div>
                  </div>
                </div>

                <div className="flex items-start gap-3 p-3 bg-muted rounded-lg">
                  <div className="w-8 h-8 bg-muted-foreground/10 rounded-full flex items-center justify-center">
                    <AlertCircle className="w-4 h-4 text-muted-foreground" />
                  </div>
                  <div className="flex-1">
                    <div className="text-sm font-medium text-muted-foreground">Severity</div>
                    <div className={`text-base font-bold ${severityInfo.color}`}>
                      {severityInfo.label}
                    </div>
                  </div>
                </div>

                {ticket.assignee && (
                  <div className="flex items-start gap-3 p-3 bg-muted rounded-lg">
                    <div className="w-8 h-8 bg-muted-foreground/10 rounded-full flex items-center justify-center">
                      <User className="w-4 h-4 text-muted-foreground" />
                    </div>
                    <div className="flex-1">
                      <div className="text-sm font-medium text-muted-foreground">Assignee</div>
                      <div className="text-base font-semibold text-foreground">{ticket.assignee}</div>
                    </div>
                  </div>
                )}

                <div className="flex items-start gap-3 p-3 bg-muted rounded-lg">
                  <div className="w-8 h-8 bg-muted-foreground/10 rounded-full flex items-center justify-center">
                    <Calendar className="w-4 h-4 text-muted-foreground" />
                  </div>
                  <div className="flex-1">
                    <div className="text-sm font-medium text-muted-foreground">Created</div>
                    <div className="text-base font-semibold text-foreground">{formatDate(ticket.created_at)}</div>
                  </div>
                </div>

                <div className="flex items-start gap-3 p-3 bg-muted rounded-lg">
                  <div className="w-8 h-8 bg-muted-foreground/10 rounded-full flex items-center justify-center">
                    <Clock className="w-4 h-4 text-muted-foreground" />
                  </div>
                  <div className="flex-1">
                    <div className="text-sm font-medium text-muted-foreground">Last Updated</div>
                    <div className="text-base font-semibold text-foreground">{formatDate(ticket.updated_at)}</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

const TicketDetailsWithErrorBoundary: React.FC = () => (
  <ErrorBoundary>
    <TicketDetails />
  </ErrorBoundary>
);

export default TicketDetailsWithErrorBoundary;
