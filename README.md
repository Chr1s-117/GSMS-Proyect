# GSMS - GPS Multi-Device Tracking System

Sistema de seguimiento GPS en tiempo real con geofencing, multi-dispositivo y análisis de rutas.

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- PostgreSQL 15+ with PostGIS extension
- Node.js 20+ (for frontend)

### Installation

```bash
# Clone repository
git clone https://github.com/Chr1s-117/GSMS-Proyect-develop-chris.git
cd GSMS-Proyect-develop-chris

# Install backend dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env
# Edit .env with your database credentials

# Run Alembic migrations
alembic upgrade head

# Start backend
uvicorn src.main:app --reload --port 8101