# 🎫 Ticket Assistant Frontend

Modern React frontend for the AI-powered ticket reporting and classification system.

## Features

- **Modern Stack**: React 18 + TypeScript + Vite + Tailwind CSS
- **AI Integration**: Real-time ticket classification with Groq API
- **Responsive Design**: Mobile-first responsive UI
- **Type Safety**: Full TypeScript integration with shared types
- **Fast Development**: Hot module replacement with Vite

## Quick Start

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Visit http://localhost:3000
```

## Development

```bash
# Build for production
npm run build

# Preview production build
npm run preview

# Lint code
npm run lint

# Type check
npm run type-check
```

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint
- `npm run type-check` - Run TypeScript type checking

## Project Structure

```
src/
├── components/          # Reusable UI components
├── pages/              # Page components
├── hooks/              # Custom React hooks
├── services/           # API services
├── utils/              # Utility functions
├── types/              # TypeScript type definitions
└── main.tsx           # Application entry point
```

## Backend Integration

The frontend communicates with the FastAPI backend at `http://localhost:8000`. Make sure the backend is running before starting the frontend development server.

## Technologies Used

- **React 18** - UI framework
- **TypeScript** - Type safety
- **Vite** - Build tool and development server
- **Tailwind CSS** - Utility-first CSS framework
- **Radix UI** - Unstyled, accessible UI components
- **React Hook Form** - Form handling
- **Axios** - HTTP client
- **React Router** - Client-side routing
- **Framer Motion** - Animation library
