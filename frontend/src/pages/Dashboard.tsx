import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
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
  const { data: stats, isLoading, error, refetch } = useQuery({
    queryKey: ['dashboard-stats'],
    queryFn: () => ticketAssistantAPI.getDashboardStats(),
    staleTime: 10000, // 10 seconds - shorter for more responsive updates
    refetchInterval: 30000, // 30 seconds - more frequent updates
    refetchOnWindowFocus: true, // Refetch when user returns to window
  });

  // Function to manually refresh stats (can be called when new tickets are created)
  const refreshStats = () => {
    refetch();
  };

  // Listen for custom events when tickets are created
  React.useEffect(() => {
    const handleTicketCreated = () => {
      console.log('New ticket created, refreshing dashboard stats...');
      refreshStats();
    };

    // Listen for custom ticket creation events
    window.addEventListener('ticketCreated', handleTicketCreated);

    return () => {
      window.removeEventListener('ticketCreated', handleTicketCreated);
    };
  }, [refetch]);

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
      <div className="space-y-6">
        <div className="animate-pulse">
          <div className="h-8 bg-muted rounded w-48 mb-6"></div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {[1, 2, 3, 4].map((i) => (
              <div key={i} className="bg-card p-6 rounded-lg card-shadow">
                <div className="h-4 bg-muted rounded w-24 mb-2"></div>
                <div className="h-8 bg-muted rounded w-16"></div>
              </div>
            ))}
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
            <AlertCircleIcon className="w-5 h-5 text-destructive" />
            <span className="text-destructive">Failed to load dashboard data</span>
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
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold text-foreground">Dashboard</h1>
        <div className="text-sm text-muted-foreground">
          Last updated: {new Date().toLocaleTimeString()}
        </div>
      </div>

      {/* Key Metrics Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card className="hover:shadow-lg transition-all duration-300">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Tickets</CardTitle>
            <div className="p-2 bg-primary/10 rounded-full">
              <TicketIcon className="w-4 h-4 text-primary" />
            </div>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-primary">{dashboardStats.total_tickets}</div>
            <div className="flex items-center text-sm text-muted-foreground">
              <ArrowUpIcon className="w-4 h-4 text-green-500 mr-1" />
              <span className="text-green-500">+12%</span>
              <span className="ml-1">from last week</span>
            </div>
          </CardContent>
        </Card>

        <Card className="hover:shadow-lg transition-all duration-300">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Open Tickets</CardTitle>
            <div className="p-2 bg-destructive/10 rounded-full">
              <AlertCircleIcon className="w-4 h-4 text-destructive" />
            </div>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-destructive">{dashboardStats.open_tickets}</div>
            <div className="flex items-center text-sm text-muted-foreground">
              <ArrowDownIcon className="w-4 h-4 text-green-500 mr-1" />
              <span className="text-green-500">-8%</span>
              <span className="ml-1">from last week</span>
            </div>
          </CardContent>
        </Card>

        <Card className="hover:shadow-lg transition-all duration-300">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Resolved Tickets</CardTitle>
            <div className="p-2 bg-green-100 dark:bg-green-900/20 rounded-full">
              <CheckCircleIcon className="w-4 h-4 text-green-600" />
            </div>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-green-600">{dashboardStats.resolved_tickets}</div>
            <div className="flex items-center text-sm text-muted-foreground">
              <ArrowUpIcon className="w-4 h-4 text-green-500 mr-1" />
              <span className="text-green-500">+15%</span>
              <span className="ml-1">from last week</span>
            </div>
          </CardContent>
        </Card>

        <Card className="hover:shadow-lg transition-all duration-300">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Avg Resolution Time</CardTitle>
            <div className="p-2 bg-purple-100 dark:bg-purple-900/20 rounded-full">
              <ClockIcon className="w-4 h-4 text-purple-600" />
            </div>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-purple-600">{dashboardStats.average_resolution_time}</div>
            <div className="flex items-center text-sm text-muted-foreground">
              <ArrowDownIcon className="w-4 h-4 text-green-500 mr-1" />
              <span className="text-green-500">-0.3h</span>
              <span className="ml-1">from last week</span>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Charts Section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Department Distribution */}
        <Card>
          <CardHeader>
            <CardTitle>Department Distribution</CardTitle>
          </CardHeader>
          <CardContent>
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
                <Tooltip
                  contentStyle={{
                    backgroundColor: 'hsl(var(--popover))',
                    border: '1px solid hsl(var(--border))',
                    borderRadius: '8px',
                    color: 'hsl(var(--popover-foreground))',
                    boxShadow: '0 10px 40px rgba(0, 0, 0, 0.4)',
                    fontSize: '14px',
                    fontWeight: '500',
                    padding: '8px 12px',
                    zIndex: 1000
                  }}
                  labelStyle={{
                    color: 'hsl(var(--popover-foreground))',
                    fontWeight: '600'
                  }}
                />
              </PieChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        {/* Severity Distribution */}
        <Card>
          <CardHeader>
            <CardTitle>Severity Distribution</CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={severityData}>
                <CartesianGrid strokeDasharray="3 3" className="opacity-30" />
                <XAxis dataKey="name" className="text-muted-foreground" />
                <YAxis className="text-muted-foreground" />
                <Tooltip
                  contentStyle={{
                    backgroundColor: 'hsl(var(--popover))',
                    border: '1px solid hsl(var(--border))',
                    borderRadius: '8px',
                    color: 'hsl(var(--popover-foreground))',
                    boxShadow: '0 10px 40px rgba(0, 0, 0, 0.4)',
                    fontSize: '14px',
                    fontWeight: '500',
                    padding: '8px 12px',
                    zIndex: 1000
                  }}
                  labelStyle={{
                    color: 'hsl(var(--popover-foreground))',
                    fontWeight: '600'
                  }}
                />
                <Bar dataKey="value" fill="hsl(var(--primary))" />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>

      {/* Weekly Trends */}
      <Card>
        <CardHeader>
          <CardTitle>Weekly Ticket Trends</CardTitle>
        </CardHeader>
        <CardContent>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={weeklyData}>
              <CartesianGrid strokeDasharray="3 3" className="opacity-30" />
              <XAxis dataKey="day" className="text-muted-foreground" />
              <YAxis className="text-muted-foreground" />
              <Tooltip
                contentStyle={{
                  backgroundColor: 'hsl(var(--popover))',
                  border: '1px solid hsl(var(--border))',
                  borderRadius: '8px',
                  color: 'hsl(var(--popover-foreground))',
                  boxShadow: '0 10px 40px rgba(0, 0, 0, 0.4)',
                  fontSize: '14px',
                  fontWeight: '500',
                  padding: '8px 12px',
                  zIndex: 1000
                }}
                labelStyle={{
                  color: 'hsl(var(--popover-foreground))',
                  fontWeight: '600'
                }}
              />
              <Legend />
              <Line type="monotone" dataKey="tickets" stroke="hsl(var(--primary))" strokeWidth={2} name="New Tickets" />
              <Line type="monotone" dataKey="resolved" stroke="#10B981" strokeWidth={2} name="Resolved" />
            </LineChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>

      {/* AI Classification Accuracy */}
      <Card className="bg-gradient-to-r from-primary/10 to-primary/5 border-primary/20">
        <CardContent className="p-6">
          <div className="flex items-center justify-between">
            <div>
              <CardTitle className="text-lg mb-2">AI Classification Accuracy</CardTitle>
              <p className="text-3xl font-bold text-primary">{accuracyPercentage.toFixed(1)}%</p>
              <p className="text-sm text-muted-foreground">Based on {dashboardStats.total_tickets} classified tickets</p>
            </div>
            <div className="p-4 bg-primary/10 rounded-full">
              <TrendingUpIcon className="w-8 h-8 text-primary" />
            </div>
          </div>
          <div className="mt-4">
            <div className="flex justify-between text-sm text-muted-foreground mb-1">
              <span>Accuracy Score</span>
              <span>{accuracyPercentage.toFixed(1)}%</span>
            </div>
            <div className="w-full bg-muted rounded-full h-2">
              <div
                className="bg-primary h-2 rounded-full transition-all duration-500"
                style={{ width: `${accuracyPercentage}%` }}
              ></div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default Dashboard;
