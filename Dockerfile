# Use Python 3.13 slim as the base image
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Copy dependency configuration
COPY pyproject.toml uv.lock ./

# Copy source code
COPY app/src/ app/src/

# Install uv
RUN pip install --no-cache-dir uv

# Install dependencies using uv
RUN uv pip install --system --no-cache-dir -e .

# Expose port that FastAPI will run on
EXPOSE 8080

# Start the FastAPI application
CMD ["uvicorn", "app.src.main:app", "--host", "0.0.0.0", "--port", "8080"]