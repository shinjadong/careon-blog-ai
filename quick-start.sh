#!/bin/bash

# CareOn Blog Automation - Quick Start Script
# 백엔드와 프론트엔드를 자동으로 설정하고 실행합니다

set -e

echo "=========================================="
echo "CareOn Blog Automation - Quick Start"
echo "=========================================="
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if running in correct directory
if [ ! -f "docker-compose.yml" ]; then
    echo "❌ Error: Please run this script from project root"
    exit 1
fi

# Function to print section header
print_section() {
    echo ""
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
}

# 1. Check Prerequisites
print_section "1️⃣  Checking Prerequisites"

# Check Python
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo -e "${GREEN}✅ Python: $PYTHON_VERSION${NC}"
else
    echo -e "${YELLOW}⚠️  Python 3.11+ required${NC}"
    exit 1
fi

# Check Node.js
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    echo -e "${GREEN}✅ Node.js: $NODE_VERSION${NC}"
else
    echo -e "${YELLOW}⚠️  Node.js 20+ required${NC}"
    exit 1
fi

# Check ADB
if command -v adb &> /dev/null; then
    ADB_VERSION=$(adb --version | head -n 1)
    echo -e "${GREEN}✅ ADB: $ADB_VERSION${NC}"
else
    echo -e "${YELLOW}⚠️  ADB not found. Install Android Platform Tools${NC}"
    exit 1
fi

# 2. Setup Backend
print_section "2️⃣  Setting Up Backend"

cd backend

# Create virtual environment if not exists
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
    echo -e "${GREEN}✅ Virtual environment created${NC}"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing Python dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt
echo -e "${GREEN}✅ Python dependencies installed${NC}"

# Create .env if not exists
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo -e "${GREEN}✅ Created .env file${NC}"
fi

# Run setup test
echo "Running setup tests..."
python test_setup.py

cd ..

# 3. Setup Frontend
print_section "3️⃣  Setting Up Frontend"

cd frontend

# Install dependencies
echo "Installing Node.js dependencies..."
npm install --silent
echo -e "${GREEN}✅ Node.js dependencies installed${NC}"

# Create .env.local if not exists
if [ ! -f ".env.local" ]; then
    cp .env.local.example .env.local
    echo -e "${GREEN}✅ Created .env.local file${NC}"
fi

cd ..

# 4. Start Servers
print_section "4️⃣  Starting Servers"

echo "Starting Backend server..."
cd backend
source venv/bin/activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!
echo -e "${GREEN}✅ Backend running on http://localhost:8000 (PID: $BACKEND_PID)${NC}"

cd ..

echo "Waiting for backend to start..."
sleep 3

echo "Starting Frontend server..."
cd frontend
npm run dev &
FRONTEND_PID=$!
echo -e "${GREEN}✅ Frontend running on http://localhost:3000 (PID: $FRONTEND_PID)${NC}"

cd ..

# 5. Summary
print_section "🎉 Setup Complete!"

echo -e "${GREEN}Backend API:${NC}     http://localhost:8000"
echo -e "${GREEN}API Docs:${NC}        http://localhost:8000/docs"
echo -e "${GREEN}Frontend:${NC}        http://localhost:3000"
echo -e "${GREEN}Admin Dashboard:${NC} http://localhost:3000/devices"
echo ""
echo -e "${YELLOW}📱 Next Steps:${NC}"
echo "1. Connect Android device via USB"
echo "2. Enable USB debugging"
echo "3. Open http://localhost:3000/devices"
echo "4. Scan and connect your device"
echo "5. Start calibration workflow"
echo ""
echo "Press Ctrl+C to stop servers"
echo ""

# Wait for Ctrl+C
trap "echo ''; echo 'Stopping servers...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; echo 'Servers stopped.'; exit 0" INT

wait
