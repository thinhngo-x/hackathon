import {
  Activity,
  AlertCircle,
  BarChart3,
  CheckCircle,
  Clock,
  Download,
  Filter,
  RefreshCw,
  Target,
  TrendingUp,
  Users,
  XCircle
} from 'lucide-react';
import React, { useState } from 'react';

interface ReportData {
  totalTickets: number;
  openTickets: number;
  resolvedTickets: number;
  avgResolutionTime: number;
  departmentStats: Array<{
    department: string;
    count: number;
    percentage: number;
    color: string;
  }>;
  severityStats: Array<{
    severity: string;
    count: number;
    percentage: number;
    color: string;
  }>;
  weeklyTrends: Array<{
    day: string;
    newTickets: number;
    resolved: number;
  }>;
  aiAccuracy: number;
}

const Reports: React.FC = () => {
  const [selectedPeriod, setSelectedPeriod] = useState('7d');
  const [selectedDepartment, setSelectedDepartment] = useState('all');

  // Mock data - in a real app, this would come from an API
  const reportData: ReportData = {
    totalTickets: 156,
    openTickets: 42,
    resolvedTickets: 114,
    avgResolutionTime: 2.4,
    departmentStats: [
      { department: 'IT Support', count: 94, percentage: 60, color: 'bg-blue-500' },
      { department: 'Network', count: 39, percentage: 25, color: 'bg-green-500' },
      { department: 'Security', count: 23, percentage: 15, color: 'bg-red-500' },
    ],
    severityStats: [
      { severity: 'Low', count: 62, percentage: 40, color: 'bg-green-400' },
      { severity: 'Medium', count: 56, percentage: 36, color: 'bg-yellow-400' },
      { severity: 'High', count: 31, percentage: 20, color: 'bg-orange-400' },
      { severity: 'Critical', count: 7, percentage: 4, color: 'bg-red-500' },
    ],
    weeklyTrends: [
      { day: 'Mon', newTickets: 12, resolved: 8 },
      { day: 'Tue', newTickets: 18, resolved: 15 },
      { day: 'Wed', newTickets: 15, resolved: 12 },
      { day: 'Thu', newTickets: 22, resolved: 18 },
      { day: 'Fri', newTickets: 25, resolved: 20 },
      { day: 'Sat', newTickets: 8, resolved: 6 },
      { day: 'Sun', newTickets: 5, resolved: 4 },
    ],
    aiAccuracy: 94.5,
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'resolved':
        return <CheckCircle className="w-5 h-5 text-green-500" />;
      case 'open':
        return <AlertCircle className="w-5 h-5 text-red-500" />;
      default:
        return <XCircle className="w-5 h-5 text-gray-500" />;
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      {/* Header */}
      <div className="bg-white dark:bg-gray-800 shadow-sm border-b border-gray-200 dark:border-gray-700">
        <div className="max-w-7xl mx-auto px-6 py-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Reports & Analytics</h1>
              <p className="text-gray-600 dark:text-gray-300 mt-1">Comprehensive insights into your ticket system</p>
            </div>
            <div className="flex items-center gap-3">
              <button className="flex items-center gap-2 px-4 py-2 text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors">
                <Filter className="w-4 h-4" />
                Filter
              </button>
              <button className="flex items-center gap-2 px-4 py-2 text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors">
                <Download className="w-4 h-4" />
                Export
              </button>
              <button className="flex items-center gap-2 px-4 py-2 text-white bg-blue-600 rounded-lg hover:bg-blue-700 transition-colors">
                <RefreshCw className="w-4 h-4" />
                Refresh
              </button>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-6 py-6 space-y-6">
        {/* Time Period Selector */}
        <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6">
          <div className="flex items-center justify-between">
            <h2 className="text-lg font-semibold text-gray-900 dark:text-white">Time Period</h2>
            <div className="flex items-center gap-1 bg-gray-100 dark:bg-gray-700 rounded-lg p-1">
              {['7d', '30d', '90d', '1y'].map((period) => (
                <button
                  key={period}
                  onClick={() => setSelectedPeriod(period)}
                  className={`px-3 py-1 text-sm rounded-md transition-colors ${
                    selectedPeriod === period
                      ? 'bg-blue-600 text-white'
                      : 'text-gray-600 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600'
                  }`}
                >
                  {period === '7d' ? 'Last 7 Days' : period === '30d' ? 'Last 30 Days' : period === '90d' ? 'Last 90 Days' : 'Last Year'}
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Key Metrics */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6">
            <div className="flex items-center justify-between mb-4">
              <div className="w-12 h-12 bg-blue-100 dark:bg-blue-900/30 rounded-lg flex items-center justify-center">
                <BarChart3 className="w-6 h-6 text-blue-600 dark:text-blue-400" />
              </div>
              <div className="text-right">
                <div className="text-2xl font-bold text-gray-900 dark:text-white">{reportData.totalTickets}</div>
                <div className="text-sm text-gray-500 dark:text-gray-400">Total Tickets</div>
              </div>
            </div>
            <div className="flex items-center gap-2 text-sm">
              <TrendingUp className="w-4 h-4 text-green-500" />
              <span className="text-green-600 dark:text-green-400 font-medium">+12%</span>
              <span className="text-gray-500 dark:text-gray-400">from last period</span>
            </div>
          </div>

          <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6">
            <div className="flex items-center justify-between mb-4">
              <div className="w-12 h-12 bg-red-100 dark:bg-red-900/30 rounded-lg flex items-center justify-center">
                <AlertCircle className="w-6 h-6 text-red-600 dark:text-red-400" />
              </div>
              <div className="text-right">
                <div className="text-2xl font-bold text-gray-900 dark:text-white">{reportData.openTickets}</div>
                <div className="text-sm text-gray-500 dark:text-gray-400">Open Tickets</div>
              </div>
            </div>
            <div className="flex items-center gap-2 text-sm">
              <TrendingUp className="w-4 h-4 text-red-500 rotate-180" />
              <span className="text-red-600 dark:text-red-400 font-medium">-8%</span>
              <span className="text-gray-500 dark:text-gray-400">from last period</span>
            </div>
          </div>

          <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6">
            <div className="flex items-center justify-between mb-4">
              <div className="w-12 h-12 bg-green-100 dark:bg-green-900/30 rounded-lg flex items-center justify-center">
                <CheckCircle className="w-6 h-6 text-green-600 dark:text-green-400" />
              </div>
              <div className="text-right">
                <div className="text-2xl font-bold text-gray-900 dark:text-white">{reportData.resolvedTickets}</div>
                <div className="text-sm text-gray-500 dark:text-gray-400">Resolved Tickets</div>
              </div>
            </div>
            <div className="flex items-center gap-2 text-sm">
              <TrendingUp className="w-4 h-4 text-green-500" />
              <span className="text-green-600 dark:text-green-400 font-medium">+15%</span>
              <span className="text-gray-500 dark:text-gray-400">from last period</span>
            </div>
          </div>

          <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6">
            <div className="flex items-center justify-between mb-4">
              <div className="w-12 h-12 bg-purple-100 dark:bg-purple-900/30 rounded-lg flex items-center justify-center">
                <Clock className="w-6 h-6 text-purple-600 dark:text-purple-400" />
              </div>
              <div className="text-right">
                <div className="text-2xl font-bold text-gray-900 dark:text-white">{reportData.avgResolutionTime}h</div>
                <div className="text-sm text-gray-500 dark:text-gray-400">Avg Resolution Time</div>
              </div>
            </div>
            <div className="flex items-center gap-2 text-sm">
              <TrendingUp className="w-4 h-4 text-purple-500 rotate-180" />
              <span className="text-purple-600 dark:text-purple-400 font-medium">-0.3h</span>
              <span className="text-gray-500 dark:text-gray-400">from last period</span>
            </div>
          </div>
        </div>

        {/* Charts Section */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Department Distribution */}
          <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6">
            <div className="flex items-center gap-3 mb-6">
              <div className="w-10 h-10 bg-blue-100 dark:bg-blue-900/30 rounded-lg flex items-center justify-center">
                <Users className="w-5 h-5 text-blue-600 dark:text-blue-400" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900 dark:text-white">Department Distribution</h3>
            </div>
            <div className="space-y-4">
              {reportData.departmentStats.map((dept, index) => (
                <div key={index} className="space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-medium text-gray-700 dark:text-gray-300">{dept.department}</span>
                    <div className="flex items-center gap-2">
                      <span className="text-sm text-gray-900 dark:text-white">{dept.count} tickets</span>
                      <span className="text-sm text-gray-500 dark:text-gray-400">({dept.percentage}%)</span>
                    </div>
                  </div>
                  <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-3">
                    <div
                      className={`h-3 rounded-full transition-all duration-500 ${dept.color}`}
                      style={{ width: `${dept.percentage}%` }}
                    />
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Severity Distribution */}
          <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6">
            <div className="flex items-center gap-3 mb-6">
              <div className="w-10 h-10 bg-yellow-100 dark:bg-yellow-900/30 rounded-lg flex items-center justify-center">
                <Target className="w-5 h-5 text-yellow-600 dark:text-yellow-400" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900 dark:text-white">Severity Distribution</h3>
            </div>
            <div className="space-y-4">
              {reportData.severityStats.map((severity, index) => (
                <div key={index} className="space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-medium text-gray-700 dark:text-gray-300">{severity.severity}</span>
                    <div className="flex items-center gap-2">
                      <span className="text-sm text-gray-900 dark:text-white">{severity.count} tickets</span>
                      <span className="text-sm text-gray-500 dark:text-gray-400">({severity.percentage}%)</span>
                    </div>
                  </div>
                  <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-3">
                    <div
                      className={`h-3 rounded-full transition-all duration-500 ${severity.color}`}
                      style={{ width: `${severity.percentage}%` }}
                    />
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Weekly Trends */}
        <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6">
          <div className="flex items-center gap-3 mb-6">
            <div className="w-10 h-10 bg-green-100 dark:bg-green-900/30 rounded-lg flex items-center justify-center">
              <Activity className="w-5 h-5 text-green-600 dark:text-green-400" />
            </div>
            <h3 className="text-xl font-semibold text-gray-900 dark:text-white">Weekly Ticket Trends</h3>
          </div>
          <div className="space-y-4">
            <div className="flex items-center gap-4 text-sm">
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 bg-blue-500 rounded-full"></div>
                <span className="text-gray-600 dark:text-gray-400">New Tickets</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 bg-green-500 rounded-full"></div>
                <span className="text-gray-600 dark:text-gray-400">Resolved</span>
              </div>
            </div>
            <div className="relative">
              <div className="flex items-end justify-between h-48 gap-2">
                {reportData.weeklyTrends.map((day, index) => (
                  <div key={index} className="flex-1 flex flex-col items-center gap-2">
                    <div className="w-full flex flex-col items-center gap-1 h-40">
                      <div className="w-full bg-gray-100 dark:bg-gray-700 rounded-t-lg relative overflow-hidden">
                        <div
                          className="bg-blue-500 transition-all duration-500 rounded-t-lg"
                          style={{ height: `${(day.newTickets / 25) * 100}%` }}
                        />
                        <div
                          className="bg-green-500 transition-all duration-500"
                          style={{ height: `${(day.resolved / 25) * 100}%` }}
                        />
                      </div>
                      <div className="text-xs text-gray-500 dark:text-gray-400 text-center">
                        <div>{day.newTickets} new</div>
                        <div>{day.resolved} resolved</div>
                      </div>
                    </div>
                    <div className="text-xs font-medium text-gray-700 dark:text-gray-300">{day.day}</div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* AI Classification Accuracy */}
        <div className="bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 dark:from-blue-900/20 dark:via-indigo-900/20 dark:to-purple-900/20 border border-blue-200 dark:border-blue-700 rounded-xl p-6">
          <div className="flex items-center gap-3 mb-6">
            <div className="w-10 h-10 bg-gradient-to-r from-blue-500 to-purple-500 rounded-lg flex items-center justify-center">
              <Target className="w-5 h-5 text-white" />
            </div>
            <h3 className="text-xl font-semibold text-gray-900 dark:text-white">AI Classification Performance</h3>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="bg-white/60 dark:bg-gray-800/60 backdrop-blur-sm rounded-lg p-4">
              <div className="text-center">
                <div className="text-4xl font-bold text-blue-600 dark:text-blue-400 mb-2">{reportData.aiAccuracy}%</div>
                <div className="text-sm text-gray-600 dark:text-gray-400">Overall Accuracy</div>
              </div>
              <div className="mt-3 w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                <div
                  className="bg-gradient-to-r from-blue-500 to-purple-500 h-2 rounded-full transition-all duration-500"
                  style={{ width: `${reportData.aiAccuracy}%` }}
                />
              </div>
            </div>
            <div className="bg-white/60 dark:bg-gray-800/60 backdrop-blur-sm rounded-lg p-4">
              <div className="text-center">
                <div className="text-4xl font-bold text-green-600 dark:text-green-400 mb-2">{reportData.totalTickets}</div>
                <div className="text-sm text-gray-600 dark:text-gray-400">Tickets Classified</div>
              </div>
              <div className="mt-3 text-xs text-gray-500 dark:text-gray-400">
                Over the last {selectedPeriod === '7d' ? '7 days' : selectedPeriod === '30d' ? '30 days' : selectedPeriod === '90d' ? '90 days' : 'year'}
              </div>
            </div>
            <div className="bg-white/60 dark:bg-gray-800/60 backdrop-blur-sm rounded-lg p-4">
              <div className="text-center">
                <div className="text-4xl font-bold text-purple-600 dark:text-purple-400 mb-2">2.1s</div>
                <div className="text-sm text-gray-600 dark:text-gray-400">Avg Classification Time</div>
              </div>
              <div className="mt-3 flex items-center justify-center gap-1 text-xs text-gray-500 dark:text-gray-400">
                <TrendingUp className="w-3 h-3 text-green-500" />
                <span>15% faster than last period</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Reports;
