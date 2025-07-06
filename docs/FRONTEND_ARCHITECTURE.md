# Frontend Architecture Proposal - Ticket Assistant

## Overview

This document outlines the frontend architecture for the Ticket Assistant application using a **monorepo approach** with Next.js 14 and TypeScript. The frontend will integrate with the existing FastAPI backend to provide a modern, user-friendly interface for ticket submission, classification, and management.

## Technology Stack

### Core Technologies

- **React 18** with **Vite** - Fast development server and build tool
- **TypeScript** - Type safety and better development experience
- **Tailwind CSS** - Utility-first CSS framework for rapid styling
- **shadcn/ui** - Modern component library built on Radix UI primitives
- **React Router v6** - Client-side routing with modern hooks

### Additional Libraries

- **React Hook Form** + **Zod** - Form handling and validation
- **TanStack Query** - Server state management and API caching
- **Framer Motion** - Animations and transitions
- **Recharts** - Data visualization for analytics dashboard
- **Lucide React** - Icon library
- **Zustand** - Lightweight state management
- **Axios** - HTTP client for API calls

## Project Structure

```
ticket-assistant/
├── backend/                          # Existing Python FastAPI backend
│   ├── src/ticket_assistant/
│   ├── tests/
│   ├── pyproject.toml
│   └── main.py
├── frontend/                         # New React/Vite frontend
│   ├── src/
│   │   ├── components/               # Reusable UI components
│   │   │   ├── ui/                   # Base components (shadcn/ui)
│   │   │   ├── forms/                # Form components
│   │   │   ├── layout/               # Layout components
│   │   │   ├── dashboard/            # Dashboard-specific components
│   │   │   └── common/               # Common components
│   │   ├── pages/                    # Page components
│   │   │   ├── Dashboard.tsx
│   │   │   ├── TicketSubmission.tsx
│   │   │   ├── TicketList.tsx
│   │   │   ├── TicketDetails.tsx
│   │   │   └── Reports.tsx
│   │   ├── hooks/                    # Custom React hooks
│   │   ├── lib/                      # Utility functions and configurations
│   │   │   ├── api/                  # API client and types
│   │   │   ├── store/                # Zustand stores
│   │   │   ├── utils/                # Utility functions
│   │   │   └── constants/            # App constants
│   │   ├── types/                    # TypeScript type definitions
│   │   ├── styles/                   # CSS and styling
│   │   │   └── globals.css
│   │   ├── App.tsx                   # Main app component
│   │   ├── main.tsx                  # Entry point
│   │   └── router.tsx                # React Router configuration
│   ├── public/                       # Static assets
│   ├── tests/                        # Frontend tests
│   ├── vite.config.ts                # Vite configuration
│   ├── tailwind.config.js            # Tailwind configuration
│   └── tsconfig.json                 # TypeScript configuration
├── shared/                           # Shared utilities and types
│   ├── types/                        # Cross-platform TypeScript types
│   ├── constants/                    # Shared constants
│   └── utils/                        # Shared utility functions
├── docs/                             # Documentation
├── scripts/                          # Build and deployment scripts
├── docker/                           # Docker configurations
└── .github/workflows/                # CI/CD workflows
```

## Application Architecture

### Core Pages and Routes

1. **Landing Page** (`/`)

   - Quick ticket submission form
   - Recent activity overview
   - Navigation to main features

2. **Dashboard** (`/dashboard`)

   - Ticket statistics and metrics
   - Recent tickets overview
   - Department workload visualization

3. **Ticket Management** (`/tickets`)

   - List all tickets with filtering/sorting
   - Individual ticket details (`/tickets/:id`)
   - Status updates and comments

4. **Submit Ticket** (`/submit`)

   - Comprehensive ticket submission form
   - Real-time AI classification preview
   - File upload support

5. **Reports & Analytics** (`/reports`)
   - Department performance metrics
   - Ticket resolution trends
   - Classification accuracy reports

### Key Features

#### Smart Ticket Submission

- **Progressive Enhancement**: Start with basic form, expand based on classification
- **Real-time AI Feedback**: Show department/severity predictions as user types
- **Auto-completion**: Suggest keywords and common error patterns
- **File Upload**: Support for screenshots, logs, and attachments
- **Rich Text Editor**: Formatted descriptions with markdown support

#### Intelligent Dashboard

- **Status Visualization**: Interactive cards showing ticket states
- **Department Routing**: Flow diagram showing ticket journey
- **Quick Actions**: Bulk operations and status updates
- **Advanced Search**: Filter by department, severity, date, assignee
- **Real-time Updates**: Live updates via WebSocket connections

#### Analytics & Insights

- **Classification Metrics**: AI accuracy and confidence scores
- **Performance Tracking**: Response times and resolution rates
- **Trend Analysis**: Identify patterns in ticket submissions
- **Custom Reports**: Exportable reports in PDF/CSV format

## Technical Implementation

### API Integration

#### Type-Safe API Client

```typescript
// lib/api/client.ts
import axios from "axios";

const apiClient = axios.create({
  baseURL: process.env.REACT_APP_API_URL || "http://localhost:8000",
  headers: {
    "Content-Type": "application/json",
  },
});

class TicketAssistantAPI {
  async submitTicket(ticket: TicketSubmission): Promise<TicketResponse> {
    const response = await apiClient.post("/tickets", ticket);
    return response.data;
  }

  async classifyError(description: string): Promise<ClassificationResult> {
    const response = await apiClient.post("/classify", { description });
    return response.data;
  }

  async getTickets(filters: TicketFilters): Promise<TicketList> {
    const response = await apiClient.get("/tickets", { params: filters });
    return response.data;
  }

  async getTicketById(id: string): Promise<TicketDetails> {
    const response = await apiClient.get(`/tickets/${id}`);
    return response.data;
  }
}
```

#### React Router Configuration

```typescript
// router.tsx
import { createBrowserRouter } from "react-router-dom";
import App from "./App";
import Dashboard from "./pages/Dashboard";
import TicketSubmission from "./pages/TicketSubmission";
import TicketList from "./pages/TicketList";
import TicketDetails from "./pages/TicketDetails";
import Reports from "./pages/Reports";

export const router = createBrowserRouter([
  {
    path: "/",
    element: <App />,
    children: [
      {
        index: true,
        element: <Dashboard />,
      },
      {
        path: "submit",
        element: <TicketSubmission />,
      },
      {
        path: "tickets",
        element: <TicketList />,
      },
      {
        path: "tickets/:id",
        element: <TicketDetails />,
      },
      {
        path: "reports",
        element: <Reports />,
      },
    ],
  },
]);
```

#### Real-time Updates

- **WebSocket connections** for live ticket updates (optional for hackathon)
- **Polling strategy** for simpler real-time updates
- **Optimistic UI updates** for better user experience
- **Automatic retry logic** for failed requests

### State Management

#### Zustand Stores

```typescript
// lib/store/ticketStore.ts
import { create } from "zustand";

interface TicketStore {
  tickets: Ticket[];
  loading: boolean;
  error: string | null;
  fetchTickets: () => Promise<void>;
  submitTicket: (ticket: TicketSubmission) => Promise<void>;
  updateTicketStatus: (id: string, status: TicketStatus) => Promise<void>;
}

export const useTicketStore = create<TicketStore>((set, get) => ({
  tickets: [],
  loading: false,
  error: null,
  fetchTickets: async () => {
    set({ loading: true });
    try {
      const tickets = await api.getTickets();
      set({ tickets, loading: false });
    } catch (error) {
      set({ error: error.message, loading: false });
    }
  },
  // ... other actions
}));
```

- **Auth Store**: User authentication and permissions
- **Ticket Store**: Ticket data and operations
- **UI Store**: Application state and preferences

#### TanStack Query

- Server state caching and synchronization
- Background data fetching
- Optimistic updates and rollback

### Component Architecture

#### Base Components (shadcn/ui)

- Button, Input, Card, Form, Dialog
- Consistent design system
- Accessibility built-in

#### Composite Components

- TicketForm, TicketCard, FilterPanel
- Dashboard widgets and charts
- Navigation and layout components

### Performance Optimizations

#### Code Splitting

- **Route-based code splitting** with React.lazy and Suspense
- **Component-level lazy loading** for heavy components
- **Dynamic imports** for large libraries

#### Caching Strategy

- **API response caching** with TanStack Query
- **Browser caching** for static assets
- **Memory optimization** with proper cleanup

#### Bundle Optimization

- **Vite's automatic optimizations** for fast builds
- **Tree shaking** for unused code
- **Image optimization** with modern formats
- **Font optimization** and preloading

## User Experience Design

### Responsive Design

- **Mobile-first approach**: Optimized for mobile ticket submission
- **Progressive Web App capabilities**: Service worker for offline functionality
- **Touch-friendly interface**: Large buttons and intuitive gestures

### Accessibility

- **WCAG 2.1 AA compliance**
- **Keyboard navigation support**
- **Screen reader compatibility**
- **High contrast mode support**

### Loading States

- **Skeleton screens** for content loading
- **Progress indicators** for form submissions
- **Error boundaries** with recovery options

## Development Workflow

### Setup Scripts

```json
{
  "scripts": {
    "dev": "concurrently \"npm run dev:backend\" \"npm run dev:frontend\"",
    "dev:backend": "cd backend && uv run python main.py",
    "dev:frontend": "cd frontend && npm run dev",
    "build": "npm run build:backend && npm run build:frontend",
    "build:backend": "cd backend && echo 'Backend build not needed for development'",
    "build:frontend": "cd frontend && npm run build",
    "test": "npm run test:backend && npm run test:frontend",
    "test:backend": "cd backend && uv run pytest tests/ -v",
    "test:frontend": "cd frontend && npm run test",
    "lint": "npm run lint:backend && npm run lint:frontend",
    "lint:backend": "cd backend && uv run ruff check src/ tests/",
    "lint:frontend": "cd frontend && npm run lint",
    "type-check": "cd frontend && npm run type-check",
    "preview": "cd frontend && npm run preview"
  }
}
```

### Vite Configuration

```typescript
// frontend/vite.config.ts
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import path from "path";

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
      "@shared": path.resolve(__dirname, "../shared"),
    },
  },
  server: {
    port: 3000,
    proxy: {
      "/api": {
        target: "http://localhost:8000",
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ""),
      },
    },
  },
});
```

### Testing Strategy

- **Unit Tests**: Component logic with **Vitest** (faster than Jest)
- **Integration Tests**: API interactions with **MSW** (Mock Service Worker)
- **Component Tests**: React components with **React Testing Library**
- **E2E Tests**: User flows with **Playwright** (if time permits)

### Code Quality

- **ESLint** + **Prettier** for consistent code formatting
- **TypeScript strict mode** for type safety
- **Husky** + **lint-staged** for pre-commit hooks
- **Conventional commits** for clear commit messages

## Deployment Strategy

### Docker Configuration

```yaml
# docker-compose.yml
services:
  backend:
    build:
      context: ./backend
      dockerfile: ../docker/Dockerfile.backend
    ports:
      - "8000:8000"
    environment:
      - GROQ_API_KEY=${GROQ_API_KEY}

  frontend:
    build:
      context: ./frontend
      dockerfile: ../docker/Dockerfile.frontend
    ports:
      - "3000:3000"
    depends_on:
      - backend
    environment:
      - REACT_APP_API_URL=http://backend:8000
```

### Frontend Dockerfile

```dockerfile
# docker/Dockerfile.frontend
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY . .
RUN npm run build

EXPOSE 3000

CMD ["npm", "run", "preview"]
```

### CI/CD Pipeline

- **GitHub Actions** for automated testing and deployment
- **Automated testing** on pull requests
- **Staged deployments** for preview environments
- **Production deployments** with rollback capability

### Hosting Options

- **Frontend**: Vercel, Netlify, or **Surge.sh** (simpler for React SPA)
- **Backend**: Railway, Render, or AWS ECS
- **Database**: PostgreSQL on AWS RDS or Supabase (if needed)
- **CDN**: CloudFront or Cloudflare for static assets

## Implementation Phases - 4-Day Hackathon Timeline

### Day 1: Foundation & Setup (8 hours)

**Goal: Get the basic structure and UI foundation ready**

- [x] Set up monorepo structure
- [x] Initialize React app with Vite and TypeScript (1h)
- [x] Set up Tailwind CSS and shadcn/ui components (1h)
- [x] Configure React Router and basic routing (1h)
- [x] Implement shared type definitions from backend (1h)
- [x] Create basic layout with header/sidebar navigation (2h)
- [x] Set up API client with Axios and TanStack Query (2h)

### Day 2: Core UI & Ticket Submission (8 hours)

**Goal: Build the main ticket submission flow with AI classification**

- [x] Build responsive ticket submission form with React Hook Form (3h)
- [x] Integrate real-time AI classification preview with TanStack Query (2h)
- [x] Create dashboard with metrics using Recharts (2h)
- [x] Implement ticket list view with filtering and sorting (1h)

### Day 3: Backend Integration & Polish (8 hours)

**Goal: Connect to real API and make it look professional**

- [x] Connect to existing FastAPI backend with proper error handling (2h)
- [x] Implement ticket submission with real AI classification (2h)
- [x] Add loading states, error boundaries, and user feedback (2h)
- [x] Create detailed ticket view with status updates (1h)
- [x] Add search and filtering functionality (1h)

### Day 3 Completion Summary

**✅ All Day 3 Goals Achieved Successfully!**

Day 3 has been completed with all planned features implemented:

1. **Backend Integration**: Frontend now fully connected to the FastAPI backend with proper error handling and fallback mechanisms
2. **Toast Notification System**: Global toast notifications implemented with React Context for user feedback
3. **Real Status Updates**: Ticket status updates now call real API endpoints with optimistic updates
4. **Enhanced Search & Filtering**: Advanced search functionality across multiple fields including keywords and assignees
5. **Error Boundaries**: Comprehensive error handling with user-friendly messages and recovery options
6. **Loading States**: Improved loading states and skeleton screens throughout the application

**Key Technical Achievements:**

- Toast Context Provider for global notifications
- Real API integration with mock fallbacks
- Enhanced search with multi-field support
- Proper React Router navigation
- Type-safe API calls with error handling
- Optimistic UI updates for better UX

**User Experience Improvements:**

- Seamless notifications for all user actions
- Enhanced filtering with clear functionality
- Real-time feedback for status updates
- Better error messages and recovery options
- Advanced search capabilities

Ready for Day 4: Demo Preparation & Final Polish!

### Day 4: Demo Preparation & Final Polish (8 hours)

**Goal: Make it demo-ready with impressive visual features**

- [ ] Add smooth animations and micro-interactions with Framer Motion (2h)
- [ ] Create impressive analytics dashboard with interactive charts (3h)
- [ ] Implement fully responsive design for mobile demo (1h)
- [ ] Add demo data seeding and reset functionality (1h)
- [ ] Final testing, bug fixes, and performance optimization (1h)

## Hackathon-Specific Technical Goals

### MVP Features (Must Have)

1. **Ticket Submission Form**

   - Clean, intuitive UI with validation
   - Real-time AI classification feedback
   - Visual department routing preview

2. **Dashboard Overview**

   - Key metrics with animated counters
   - Recent tickets with status indicators
   - Department distribution chart

3. **Ticket Management**

   - List view with filtering
   - Individual ticket details
   - Status update functionality

4. **AI Integration**
   - Live classification as user types
   - Confidence score visualization
   - Department routing suggestions

### Nice-to-Have Features (If Time Permits)

1. **Advanced Analytics**

   - Interactive charts and graphs
   - Trend analysis visualization
   - Export functionality (simple JSON download)

2. **Enhanced UX**

   - Dark/light theme toggle
   - Keyboard shortcuts
   - Toast notifications

3. **Demo Enhancements**
   - Fake real-time updates simulation
   - Sample data generator
   - Demo mode with guided tour

### Technical Simplifications for Hackathon

#### Authentication

- **Skip complex auth**: Use simple localStorage for demo user
- **Mock user data**: Pre-defined user roles and permissions
- **No registration flow**: Focus on core functionality

#### Data Persistence

- **Use localStorage**: For demo data persistence and offline drafts
- **Mock API responses**: When backend isn't available during development
- **Sample data**: Pre-loaded realistic ticket examples
- **Session storage**: For temporary form data and navigation state

#### Testing & Quality

- **Basic error handling**: Focus on happy path
- **Manual testing only**: Skip automated test suite
- **Console logging**: For debugging during demo

#### Deployment

- **Frontend SPA**: Deploy to Vercel, Netlify, or Surge.sh
- **Environment variables**: Simple config for API endpoints
- **Static fallbacks**: Work without backend if needed
- **Build optimization**: Ensure fast loading and small bundle size

### Demo Strategy

#### Storyline for Presentation

1. **Problem Statement** (30 seconds)

   - Show current manual ticket routing pain
   - Highlight time waste and miscategorization

2. **Solution Demo** (3 minutes)

   - Live ticket submission with AI classification
   - Dashboard showing department routing efficiency
   - Real-time updates and analytics

3. **Technical Highlights** (1 minute)
   - AI integration with Groq
   - Modern React architecture
   - Responsive design showcase

#### Demo Data Setup

- **Pre-populated tickets**: Various departments and severities
- **Realistic scenarios**: Common IT issues and routing
- **Performance metrics**: Impressive but believable numbers

### Success Metrics for Hackathon

#### Technical Achievement

- ✅ Working AI classification integration with real-time feedback
- ✅ Responsive, professional UI with modern design patterns
- ✅ Smooth single-page application experience
- ✅ Clean, maintainable code structure with TypeScript

#### Visual Impact

- ✅ Modern, polished design
- ✅ Smooth animations and transitions
- ✅ Impressive data visualizations
- ✅ Mobile-responsive demonstration

#### Functionality

- ✅ End-to-end ticket submission flow
- ✅ Dashboard with meaningful metrics
- ✅ Search and filtering capabilities
- ✅ Status tracking and updates

## Security Considerations

### Authentication & Authorization

- JWT tokens for session management
- Role-based access control (RBAC)
- Secure cookie handling
- CSRF protection

### Data Security

- Input validation and sanitization
- XSS protection with Content Security Policy
- Secure API communication (HTTPS only)
- Environment variable security

### Privacy

- Data minimization principles
- GDPR compliance considerations
- Audit logging for sensitive operations
- Secure file upload handling

## Monitoring & Analytics

### Application Monitoring

- **Error tracking** with Sentry
- **Performance monitoring** with Web Vitals
- **User analytics** with privacy-focused tools
- **API monitoring** with health checks

### Business Metrics

- Ticket submission rates
- Classification accuracy
- User engagement metrics
- System performance indicators

## Future Enhancements

### AI-Powered Features

- **Smart Suggestions**: Recommend similar resolved tickets
- **Auto-categorization**: Pre-fill fields based on description
- **Sentiment Analysis**: Detect urgent or frustrated users
- **Multi-language Support**: Auto-detect and translate content

### Collaboration Features

- **Real-time Comments**: Team collaboration on tickets
- **Assignment System**: Automatic routing to team members
- **Notification System**: Email/push notifications
- **Activity Timeline**: Complete audit trail

### Integration Possibilities

- **Slack/Teams Integration**: Notifications and updates
- **JIRA/Linear Integration**: Sync with project management tools
- **Email Integration**: Ticket creation from emails
- **Webhook Support**: Custom integrations

## Conclusion

This React-based frontend architecture provides a solid foundation for building a modern, scalable ticket assistant application. The combination of **React + Vite** offers excellent developer experience with fast hot-reloading, while **TypeScript** ensures type safety across the entire application.

The monorepo approach ensures seamless integration between frontend and backend, with shared types and constants preventing API mismatches. The chosen technologies (**Tailwind CSS**, **shadcn/ui**, **TanStack Query**, **Zustand**) provide a perfect balance between developer productivity and application performance.

**Key advantages of this React stack:**

- **Faster development**: Vite's lightning-fast dev server and HMR
- **Better control**: Full control over routing and state management
- **Smaller bundle**: Only include what you need, no unnecessary Next.js features
- **Easier deployment**: Simple SPA deployment to any static hosting
- **Hackathon-friendly**: Quicker setup and fewer configuration complexities

The phased implementation approach allows for iterative development and early user feedback, ensuring the final product meets user needs and business requirements while staying within the hackathon timeline.
