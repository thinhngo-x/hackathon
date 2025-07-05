import React from 'react';

const Dashboard: React.FC = () => {
  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold text-gray-900 mb-6">Dashboard</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-semibold text-gray-700">Total Tickets</h3>
          <p className="text-3xl font-bold text-blue-600">156</p>
        </div>
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-semibold text-gray-700">Open Tickets</h3>
          <p className="text-3xl font-bold text-red-600">42</p>
        </div>
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-semibold text-gray-700">Resolved</h3>
          <p className="text-3xl font-bold text-green-600">114</p>
        </div>
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-semibold text-gray-700">Avg Resolution</h3>
          <p className="text-3xl font-bold text-purple-600">2.4h</p>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
