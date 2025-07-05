import { createBrowserRouter } from 'react-router-dom';
import App from './App';
import Dashboard from './pages/Dashboard';
import TicketSubmission from './pages/TicketSubmission';
import TicketList from './pages/TicketList';
import TicketDetails from './pages/TicketDetails';
import Reports from './pages/Reports';

export const router = createBrowserRouter([
  {
    path: '/',
    element: <App />,
    children: [
      {
        index: true,
        element: <Dashboard />,
      },
      {
        path: 'submit',
        element: <TicketSubmission />,
      },
      {
        path: 'tickets',
        element: <TicketList />,
      },
      {
        path: 'tickets/:id',
        element: <TicketDetails />,
      },
      {
        path: 'reports',
        element: <Reports />,
      },
    ],
  },
]);
