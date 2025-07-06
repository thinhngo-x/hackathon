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
import { ticketAssistantAPI } from '../lib/api/client';
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
        return 'bg-red-100 text-red-800 border-red-200';
      case 'in_progress':
        return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      case 'pending':
        return 'bg-blue-100 text-blue-800 border-blue-200';
      case 'resolved':
        return 'bg-green-100 text-green-800 border-green-200';
      case 'closed':
        return 'bg-gray-100 text-gray-800 border-gray-200';
      default:
        return 'bg-gray-100 text-gray-600 border-gray-200';
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
      <div className="p-6">
        <div className="animate-pulse">
          <div className="flex items-center gap-4 mb-6">
            <div className="h-6 w-6 bg-gray-200 rounded"></div>
            <div className="h-8 bg-gray-200 rounded w-48"></div>
          </div>
          <div className="bg-white rounded-lg shadow p-6 space-y-4">
            <div className="h-6 bg-gray-200 rounded w-3/4"></div>
            <div className="h-4 bg-gray-200 rounded w-1/2"></div>
            <div className="h-20 bg-gray-200 rounded"></div>
          </div>
        </div>
      </div>
    );
  }

  if (error || !ticket) {
    return (
      <div className="p-6">
        <div className="bg-red-50 border border-red-200 rounded-lg p-6">
          <div className="flex items-center gap-2 mb-4">
            <AlertCircle className="w-6 h-6 text-red-600" />
            <h2 className="text-lg font-semibold text-red-800">Ticket Not Found</h2>
          </div>
          <p className="text-red-700 mb-4">
            The ticket you're looking for doesn't exist or couldn't be loaded.
          </p>
          <button
            onClick={() => navigate('/tickets')}
            className="flex items-center gap-2 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
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
    <div className="p-6 max-w-4xl mx-auto space-y-6">
      {/* Header */}
      <div className="flex items-center gap-4">
        <button
          onClick={() => navigate('/tickets')}
          className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
        >
          <ArrowLeft className="w-5 h-5 text-gray-600" />
        </button>
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Ticket {ticket.id}</h1>
          <p className="text-gray-600">{ticket.title || ticket.description.substring(0, 100)}...</p>
        </div>
      </div>

      {/* Main Content */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Ticket Details */}
        <div className="lg:col-span-2 space-y-6">
          {/* Description */}
          <div className="bg-white rounded-lg shadow-sm border p-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Description</h2>
            <p className="text-gray-700 whitespace-pre-wrap">{ticket.description}</p>
          </div>

          {/* Keywords */}
          {ticket.keywords && ticket.keywords.length > 0 && (
            <div className="bg-white rounded-lg shadow-sm border p-6">
              <h2 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
                <Tag className="w-5 h-5" />
                Keywords
              </h2>
              <div className="flex flex-wrap gap-2">
                {ticket.keywords.map((keyword, index) => (
                  <span
                    key={index}
                    className="px-2 py-1 bg-blue-100 text-blue-800 text-sm rounded-full"
                  >
                    {keyword}
                  </span>
                ))}
              </div>
            </div>
          )}

          {/* Classification */}
          {ticket.classification && (
            <div className="bg-gradient-to-r from-blue-50 to-indigo-50 border border-blue-200 rounded-lg p-6">
              <h2 className="text-lg font-semibold text-gray-900 mb-4">AI Classification</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <div className="text-sm font-medium text-gray-500">Department</div>
                  <div className="text-lg font-semibold text-gray-900">
                    {ticket.classification.department}
                  </div>
                </div>
                <div>
                  <div className="text-sm font-medium text-gray-500">Confidence</div>
                  <div className="text-lg font-semibold text-blue-600">
                    {(ticket.classification.confidence * 100).toFixed(1)}%
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Sidebar */}
        <div className="space-y-6">
          {/* Status and Actions */}
          <div className="bg-white rounded-lg shadow-sm border p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Status & Actions</h3>

            <div className="space-y-4">
              <div className="flex items-center gap-3">
                {getStatusIcon(ticket.status)}
                <span className={`px-3 py-1 text-sm font-semibold rounded-full border ${getStatusColor(ticket.status)}`}>
                  {ticket.status.replace('_', ' ').toUpperCase()}
                </span>
              </div>

              <div className="space-y-2">
                <label className="text-sm font-medium text-gray-700">Update Status:</label>
                <select
                  value={ticket.status}
                  onChange={(e) => handleStatusUpdate(e.target.value)}
                  disabled={updateStatusMutation.isPending}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
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

          {/* Ticket Info */}
          <div className="bg-white rounded-lg shadow-sm border p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Ticket Information</h3>

            <div className="space-y-4">
              <div className="flex items-center gap-3">
                <User className="w-4 h-4 text-gray-400" />
                <div>
                  <div className="text-sm font-medium text-gray-500">Reporter</div>
                  <div className="text-sm text-gray-900">{ticket.name}</div>
                </div>
              </div>

              {ticket.reporter_email && (
                <div className="flex items-center gap-3">
                  <Mail className="w-4 h-4 text-gray-400" />
                  <div>
                    <div className="text-sm font-medium text-gray-500">Email</div>
                    <div className="text-sm text-gray-900">{ticket.reporter_email}</div>
                  </div>
                </div>
              )}

              <div className="flex items-center gap-3">
                <Tag className="w-4 h-4 text-gray-400" />
                <div>
                  <div className="text-sm font-medium text-gray-500">Department</div>
                  <div className="text-sm text-gray-900">{getDepartmentLabel(ticket.department)}</div>
                </div>
              </div>

              <div className="flex items-center gap-3">
                <AlertCircle className="w-4 h-4 text-gray-400" />
                <div>
                  <div className="text-sm font-medium text-gray-500">Severity</div>
                  <div className={`text-sm font-semibold ${severityInfo.color}`}>
                    {severityInfo.label}
                  </div>
                </div>
              </div>

              {ticket.assignee && (
                <div className="flex items-center gap-3">
                  <User className="w-4 h-4 text-gray-400" />
                  <div>
                    <div className="text-sm font-medium text-gray-500">Assignee</div>
                    <div className="text-sm text-gray-900">{ticket.assignee}</div>
                  </div>
                </div>
              )}

              <div className="flex items-center gap-3">
                <Calendar className="w-4 h-4 text-gray-400" />
                <div>
                  <div className="text-sm font-medium text-gray-500">Created</div>
                  <div className="text-sm text-gray-900">{formatDate(ticket.created_at)}</div>
                </div>
              </div>

              <div className="flex items-center gap-3">
                <Clock className="w-4 h-4 text-gray-400" />
                <div>
                  <div className="text-sm font-medium text-gray-500">Last Updated</div>
                  <div className="text-sm text-gray-900">{formatDate(ticket.updated_at)}</div>
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
