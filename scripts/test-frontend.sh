#!/usr/bin/env bash

# Frontend Environment Setup and Testing Script

echo "🚀 Ticket Assistant Frontend - Environment Setup"
echo "================================================"

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js >= 18"
    exit 1
fi

# Check Node.js version
NODE_VERSION=$(node --version | cut -d'.' -f1 | cut -d'v' -f2)
if [ "$NODE_VERSION" -lt 18 ]; then
    echo "❌ Node.js version is too old. Please install Node.js >= 18"
    exit 1
fi

echo "✅ Node.js version: $(node --version)"

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "❌ npm is not installed"
    exit 1
fi

echo "✅ npm version: $(npm --version)"

# Navigate to frontend directory
cd "$(dirname "$0")/frontend" || exit 1

echo "📁 Working directory: $(pwd)"

# Install dependencies
echo "📦 Installing dependencies..."
npm install --silent

# Check for TypeScript errors
echo "🔍 Checking TypeScript compilation..."
if npx tsc --noEmit --quiet; then
    echo "✅ TypeScript compilation successful"
else
    echo "❌ TypeScript compilation failed"
    exit 1
fi

# Test build
echo "🔨 Testing production build..."
if npm run build --silent; then
    echo "✅ Production build successful"
else
    echo "❌ Production build failed"
    exit 1
fi

# Start development server
echo "🌐 Starting development server..."
echo "📍 Frontend will be available at: http://localhost:3000"
echo "📍 If port 3000 is busy, check the console for the alternate port"
echo ""
echo "🔧 To run from project root: npm run dev:frontend"
echo "🔧 To run both frontend and backend: npm run dev"
echo ""
echo "Press Ctrl+C to stop the server"
npm run dev
