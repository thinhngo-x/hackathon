import { Zap } from 'lucide-react';
import { Link, Outlet, useLocation } from 'react-router-dom';
import './App.css';
import { ErrorBoundary } from './components/ErrorBoundary';
import ThemeSwitcher from './components/ThemeSwitcher';
import { ToastContainer } from './components/Toast';
import { ThemeProvider } from './lib/contexts/ThemeContext';
import { ToastProvider, useToastContext } from './lib/contexts/ToastContext';

function AppContent() {
  const location = useLocation();
  const { toasts, removeToast } = useToastContext();

  const navigation = [
    { name: 'Dashboard', href: '/', current: location.pathname === '/' },
    { name: 'Submit Ticket', href: '/submit', current: location.pathname === '/submit' },
    { name: 'All Tickets', href: '/tickets', current: location.pathname === '/tickets' },
    { name: 'Reports', href: '/reports', current: location.pathname === '/reports' },
  ];

  return (
    <div className="min-h-screen bg-background text-foreground transition-colors duration-300">
      {/* Modern Navigation */}
      <nav className="sticky top-0 z-50 border-b border-border/40 glass-effect">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="flex h-16 items-center justify-between">
            {/* Logo and Brand */}
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2">
                <div className="p-2 bg-primary rounded-lg">
                  <Zap className="h-5 w-5 text-primary-foreground" />
                </div>
                <h1 className="text-xl font-bold bg-gradient-to-r from-primary to-primary/80 bg-clip-text text-transparent">
                  Ticket Assistant
                </h1>
              </div>
            </div>

            {/* Navigation Links */}
            <div className="hidden md:flex items-center space-x-1">
              {navigation.map((item) => (
                <Link
                  key={item.name}
                  to={item.href}
                  className={`
                    px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200
                    ${item.current
                      ? 'bg-primary text-primary-foreground shadow-sm'
                      : 'text-muted-foreground hover:text-foreground hover:bg-accent'
                    }
                  `}
                >
                  {item.name}
                </Link>
              ))}
            </div>

            {/* Theme Switcher */}
            <div className="flex items-center space-x-4">
              <ThemeSwitcher />
            </div>
          </div>
        </div>

        {/* Mobile Navigation */}
        <div className="md:hidden border-t border-border/40">
          <div className="flex space-x-1 p-2">
            {navigation.map((item) => (
              <Link
                key={item.name}
                to={item.href}
                className={`
                  flex-1 px-3 py-2 rounded-md text-xs font-medium text-center transition-all duration-200
                  ${item.current
                    ? 'bg-primary text-primary-foreground'
                    : 'text-muted-foreground hover:text-foreground hover:bg-accent'
                  }
                `}
              >
                {item.name}
              </Link>
            ))}
          </div>
        </div>
      </nav>

      {/* Main Content with Modern Styling */}
      <main className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-6">
        <ErrorBoundary>
          <div className="animate-fade-in">
            <Outlet />
          </div>
        </ErrorBoundary>
      </main>

      {/* Toast notifications */}
      <ToastContainer
        toasts={toasts}
        onClose={removeToast}
      />
    </div>
  );
}

// Main App component with providers
function App() {
  return (
    <ThemeProvider>
      <ToastProvider>
        <AppContent />
      </ToastProvider>
    </ThemeProvider>
  );
}

export default App;
