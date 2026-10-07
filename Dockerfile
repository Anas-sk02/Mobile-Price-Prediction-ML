# Multi-Stage Production Dockerfile for SmartPrice Full-Stack System
# Stage 1: Build the React + TypeScript Frontend
FROM node:20-alpine AS frontend-builder
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

# Stage 2: Production Python Backend Engine
FROM python:3.11-slim
WORKDIR /app

# Install system dependencies for scientific packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python requirements
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code, models, data, and pipelines
COPY backend/ ./backend/
COPY ml/ ./ml/
COPY data/ ./data/
COPY smartphone_cleaned_v5.csv ./
COPY run_backend.py ./

# Copy built frontend assets from Stage 1 into frontend/dist
COPY --from=frontend-builder /app/frontend/dist ./frontend/dist

# Expose port (default 8000, dynamically overridden by $PORT on Render/Cloud)
ENV PORT=8000
EXPOSE 8000

# Start FastAPI production server with Uvicorn
CMD ["python", "run_backend.py"]
