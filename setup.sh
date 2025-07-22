#!/bin/bash

# AI Q&A Interview Project Setup Script
# This script sets up both backend and frontend for development

echo "🚀 Setting up AI Q&A Interview Project..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed. Please install Python 3.8+ and try again."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    print_error "Node.js is not installed. Please install Node.js 18+ and try again."
    exit 1
fi

print_status "Python version: $(python3 --version)"
print_status "Node.js version: $(node --version)"

# Setup Backend
print_status "Setting up backend..."
cd backend

# Create virtual environment
if [ ! -d "venv" ]; then
    print_status "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
print_status "Activating virtual environment..."
source venv/bin/activate

# Install Python dependencies
print_status "Installing Python dependencies..."
pip install -r requirements.txt

# Check if .env file exists
if [ ! -f ".env" ]; then
    print_warning ".env file not found. Creating from template..."
    cp .env.template .env
    print_warning "Please edit .env file with your API keys before running the application."
fi

cd ..

# Setup Frontend
print_status "Setting up frontend..."
cd frontend

# Install Node.js dependencies
print_status "Installing Node.js dependencies..."
npm install

cd ..

print_status "✅ Setup complete!"
echo ""
echo "🔧 Next steps:"
echo "1. Edit backend/.env with your API keys"
echo "2. Start the backend: cd backend && source venv/bin/activate && python main.py"
echo "3. Start the frontend: cd frontend && npm run dev"
echo "4. Open http://localhost:3000 in your browser"
echo ""
echo "📚 Documentation:"
echo "- API Docs: http://localhost:8000/docs"
echo "- Health Check: http://localhost:8000/api/v1/health"
echo "- Project README: ./README.md"
