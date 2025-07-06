import { Link, Outlet, useLocation } from 'react-router-dom';
import './App.css';

function App() {
  const location = useLocation();

  const navigation = [
    { name: 'Dashboard', href: '/', current: location.pathname === '/' },
    { name: 'Submit Ticket', href: '/submit', current: location.pathname === '/submit' },
    { name: 'All Tickets', href: '/tickets', current: location.pathname === '/tickets' },
    { name: 'Reports', href: '/reports', current: location.pathname === '/reports' },
  ];

  return (
    <div className="min-h-screen bg-gray-100">
      <nav className="bg-white shadow-sm">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="flex h-16 justify-between">
            <div className="flex">
              <div className="flex flex-shrink-0 items-center">
                <h1 className="text-xl font-bold text-gray-900">Ticket Assistant</h1>
              </div>
              <div className="ml-6 flex space-x-4 sm:space-x-8">
                {navigation.map((item) => (
                  <Link
                    key={item.name}
                    to={item.href}
                    className={`inline-flex items-center border-b-2 px-1 pt-1 text-xs sm:text-sm font-medium ${
                      item.current
                        ? 'border-blue-500 text-gray-900'
                        : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700'
                    }`}
                  >
                    {item.name}
                  </Link>
                ))}
              </div>
            </div>
          </div>
        </div>
      </nav>

      <main className="mx-auto max-w-7xl">
        <Outlet />
      </main>
    </div>
  );
}

export default App;
