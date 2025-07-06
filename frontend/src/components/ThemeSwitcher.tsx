import { Button } from '@/components/ui/button';
import { cn } from '@/lib/utils';
import { Monitor, Moon, Sun } from 'lucide-react';
import React from 'react';
import { useTheme } from '../lib/contexts/ThemeContext';

const ThemeSwitcher: React.FC = () => {
  const { theme, setTheme } = useTheme();

  const themes = [
    { value: 'light', label: 'Light', icon: Sun },
    { value: 'dark', label: 'Dark', icon: Moon },
    { value: 'system', label: 'System', icon: Monitor }
  ] as const;

  return (
    <div className="flex items-center space-x-1 bg-muted rounded-lg p-1">
      {themes.map(({ value, label, icon: Icon }) => (
        <Button
          key={value}
          variant={theme === value ? "secondary" : "ghost"}
          size="sm"
          onClick={() => setTheme(value)}
          className={cn(
            "flex items-center gap-2 transition-all duration-200",
            theme === value && "bg-primary text-primary-foreground hover:bg-primary/90"
          )}
          title={`Switch to ${label.toLowerCase()} theme`}
        >
          <Icon className="w-4 h-4" />
          <span className="hidden sm:inline">{label}</span>
        </Button>
      ))}
    </div>
  );
};

export default ThemeSwitcher;
