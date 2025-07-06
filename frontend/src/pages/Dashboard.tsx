import { useQuery } from '@tanstack/react-query';
import {
  AlertCircleIcon,
  ArrowDownIcon,
  ArrowUpIcon,
  CheckCircleIcon,
  ClockIcon,
  TicketIcon,
  TrendingUpIcon
} from 'lucide-react';
import React from 'react';
import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  Legend,
  Line,
  LineChart,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
  XAxis, YAxis
} from 'recharts';
import { ticketAssistantAPI } from '../lib/api/client';

const Dashboard: React.FC = () => {
  const { data: stats, isLoading, error } = useQuery({
    queryKey: ['dashboard-stats'],
    queryFn: () => ticketAssistantAPI.getDashboardStats(),
    staleTime: 30000, // 30 seconds
    refetchInterval: 60000, // 1 minute
  });

  // Mock data for charts when API is not available
  const departmentData = [
    { name: 'Backend', value: 45, color: '#3B82F6' },
    { name: 'Frontend', value: 30, color: '#10B981' },
    { name: 'Database', value: 15, color: '#F59E0B' },
    { name: 'DevOps', value: 25, color: '#EF4444' },
    { name: 'Security', value: 20, color: '#8B5CF6' },
    { name: 'API', value: 35, color: '#06B6D4' },
  ];

  const severityData = [
    { name: 'Low', value: 60, color: '#10B981' },
    { name: 'Medium', value: 45, color: '#F59E0B' },
    { name: 'High', value: 30, color: '#EF4444' },
    { name: 'Critical', value: 15, color: '#DC2626' },
  ];

  const weeklyData = [
    { day: 'Mon', tickets: 12, resolved: 8 },
    { day: 'Tue', tickets: 19, resolved: 15 },
    { day: 'Wed', tickets: 15, resolved: 12 },
    { day: 'Thu', tickets: 22, resolved: 18 },
    { day: 'Fri', tickets: 18, resolved: 14 },
    { day: 'Sat', tickets: 8, resolved: 6 },
    { day: 'Sun', tickets: 5, resolved: 4 },
  ];

  if (isLoading) {
    return (
      <div className="p-6">
        <div className="animate-pulse">
          <div className="h-8 bg-gray-200 rounded w-48 mb-6"></div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {[1, 2, 3, 4].map((i) => (
              <div key={i} className="bg-white p-6 rounded-lg shadow">
                <div className="h-4 bg-gray-200 rounded w-24 mb-2"></div>
                <div className="h-8 bg-gray-200 rounded w-16"></div>
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-6">
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <div className="flex items-center gap-2">
            <AlertCircleIcon className="w-5 h-5 text-red-600" />
            <span className="text-red-700">Failed to load dashboard data</span>
          </div>
        </div>
      </div>
    );
  }

  const dashboardStats = stats || {
    total_tickets: 156,
    open_tickets: 42,
    resolved_tickets: 114,
    average_resolution_time: '2.4h',
    classification_accuracy: 94.5,
    department_distribution: {
      'Backend': 45,
      'Frontend': 30,
      'Database': 15,
      'DevOps': 25,
      'Security': 20,
      'API': 35
    }
  };

  // Convert classification accuracy from decimal to percentage if needed
  const accuracyPercentage = dashboardStats.classification_accuracy > 1
    ? dashboardStats.classification_accuracy
    : dashboardStats.classification_accuracy * 100;

  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
        <div className="text-sm text-gray-500">
          Last updated: {new Date().toLocaleTimeString()}
        </div>
      </div>

      {/* Key Metrics Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="bg-white p-6 rounded-lg shadow-sm border hover:shadow-md transition-shadow">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-500">Total Tickets</p>
              <p className="text-3xl font-bold text-blue-600">{dashboardStats.total_tickets}</p>
            </div>
            <div className="p-3 bg-blue-100 rounded-full">
              <TicketIcon className="w-6 h-6 text-blue-600" />
            </div>
          </div>
          <div className="mt-2 flex items-center text-sm">
            <ArrowUpIcon className="w-4 h-4 text-green-500 mr-1" />
            <span className="text-green-500">+12%</span>
            <span className="text-gray-500 ml-1">from last week</span>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-sm border hover:shadow-md transition-shadow">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-500">Open Tickets</p>
              <p className="text-3xl font-bold text-red-600">{dashboardStats.open_tickets}</p>
            </div>
            <div className="p-3 bg-red-100 rounded-full">
              <AlertCircleIcon className="w-6 h-6 text-red-600" />
            </div>
          </div>
          <div className="mt-2 flex items-center text-sm">
            <ArrowDownIcon className="w-4 h-4 text-green-500 mr-1" />
            <span className="text-green-500">-8%</span>
            <span className="text-gray-500 ml-1">from last week</span>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-sm border hover:shadow-md transition-shadow">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-500">Resolved Tickets</p>
              <p className="text-3xl font-bold text-green-600">{dashboardStats.resolved_tickets}</p>
            </div>
            <div className="p-3 bg-green-100 rounded-full">
              <CheckCircleIcon className="w-6 h-6 text-green-600" />
            </div>
          </div>
          <div className="mt-2 flex items-center text-sm">
            <ArrowUpIcon className="w-4 h-4 text-green-500 mr-1" />
            <span className="text-green-500">+15%</span>
            <span className="text-gray-500 ml-1">from last week</span>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-sm border hover:shadow-md transition-shadow">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-500">Avg Resolution Time</p>
              <p className="text-3xl font-bold text-purple-600">{dashboardStats.average_resolution_time}</p>
            </div>
            <div className="p-3 bg-purple-100 rounded-full">
              <ClockIcon className="w-6 h-6 text-purple-600" />
            </div>
          </div>
          <div className="mt-2 flex items-center text-sm">
            <ArrowDownIcon className="w-4 h-4 text-green-500 mr-1" />
            <span className="text-green-500">-0.3h</span>
            <span className="text-gray-500 ml-1">from last week</span>
          </div>
        </div>
      </div>

      {/* Charts Section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Department Distribution */}
        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Department Distribution</h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={departmentData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percent }) => `${name} ${((percent || 0) * 100).toFixed(0)}%`}
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
              >
                {departmentData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>

        {/* Severity Distribution */}
        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Severity Distribution</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={severityData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="value" fill="#3B82F6" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Weekly Trends */}
      <div className="bg-white p-6 rounded-lg shadow-sm border">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Weekly Ticket Trends</h3>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={weeklyData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="day" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Line type="monotone" dataKey="tickets" stroke="#3B82F6" strokeWidth={2} name="New Tickets" />
            <Line type="monotone" dataKey="resolved" stroke="#10B981" strokeWidth={2} name="Resolved" />
          </LineChart>
        </ResponsiveContainer>
      </div>

      {/* AI Classification Accuracy */}
      <div className="bg-gradient-to-r from-blue-50 to-indigo-50 p-6 rounded-lg border border-blue-200">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">AI Classification Accuracy</h3>
            <p className="text-3xl font-bold text-blue-600">{accuracyPercentage.toFixed(1)}%</p>
            <p className="text-sm text-gray-600">Based on {dashboardStats.total_tickets} classified tickets</p>
          </div>
          <div className="p-4 bg-blue-100 rounded-full">
            <TrendingUpIcon className="w-8 h-8 text-blue-600" />
          </div>
        </div>
        <div className="mt-4">
          <div className="flex justify-between text-sm text-gray-600 mb-1">
            <span>Accuracy Score</span>
            <span>{accuracyPercentage.toFixed(1)}%</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div
              className="bg-blue-600 h-2 rounded-full transition-all duration-500"
              style={{ width: `${accuracyPercentage}%` }}
            ></div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
