import React from 'react';

const TicketDetails: React.FC = () => {
  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold text-gray-900 mb-6">Ticket Details</h1>
      <div className="bg-white p-6 rounded-lg shadow">
        <div className="border-b pb-4 mb-4">
          <h2 className="text-xl font-semibold text-gray-900">Login Issue - Unable to Access Dashboard</h2>
          <p className="text-sm text-gray-600 mt-2">Ticket #001 • Created 2 hours ago</p>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="md:col-span-2">
            <h3 className="font-medium text-gray-900 mb-2">Description</h3>
            <p className="text-gray-700 mb-6">
              User is unable to log into the dashboard after entering correct credentials.
              The page keeps redirecting to the login page without showing any error message.
            </p>
            <h3 className="font-medium text-gray-900 mb-2">AI Classification</h3>
            <div className="bg-blue-50 p-4 rounded-lg">
              <p className="text-sm text-blue-800">
                <strong>Department:</strong> IT Support<br />
                <strong>Priority:</strong> High<br />
                <strong>Confidence:</strong> 95%
              </p>
            </div>
          </div>
          <div>
            <h3 className="font-medium text-gray-900 mb-2">Ticket Information</h3>
            <div className="space-y-2 text-sm">
              <div>
                <span className="font-medium">Status:</span>
                <span className="ml-2 px-2 py-1 bg-red-100 text-red-800 rounded-full text-xs">Open</span>
              </div>
              <div>
                <span className="font-medium">Reporter:</span>
                <span className="ml-2 text-gray-600">John Doe</span>
              </div>
              <div>
                <span className="font-medium">Email:</span>
                <span className="ml-2 text-gray-600">john.doe@example.com</span>
              </div>
              <div>
                <span className="font-medium">Assigned to:</span>
                <span className="ml-2 text-gray-600">IT Support Team</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TicketDetails;
