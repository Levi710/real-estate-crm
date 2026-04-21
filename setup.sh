#!/bin/bash

echo "======================================"
echo " Real Estate CRM - Project Setup"
echo "======================================"

# Create directory structure
echo "[1/5] Creating project directories..."
mkdir -p etl analytics dashboard backend data streaming kafka spark quality dags logs
echo "✓ Directories created"

# Set permissions
echo "[2/5] Setting file permissions..."
chmod +x etl/seed.py
chmod +x etl/etl_pipeline.py
chmod +x streaming/stream_simulator.py
echo "✓ Permissions set"

# Log operation
echo "[3/5] Creating log entry..."
mkdir -p logs
echo "[$(date)] Project setup executed" >> logs/setup.log
echo "✓ Log entry created"

# Check Docker is running
echo "[4/5] Checking Docker..."
if docker info > /dev/null 2>&1; then
    echo "✓ Docker is running"
else
    echo "✗ Docker is not running - please start Docker"
fi

# Check Python dependencies
echo "[5/5] Checking Python dependencies..."
pip install -r requirements.txt -q
echo "✓ Dependencies installed"

echo "======================================"
echo " Setup Complete!"
echo "======================================"
echo "Run: docker compose up -d"
echo "Run: python etl/seed.py"
echo "Run: streamlit run dashboard/app.py"