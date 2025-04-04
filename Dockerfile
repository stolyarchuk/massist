FROM python:3.12-slim

WORKDIR /app

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PIP_ROOT_USER_ACTION=ignore

COPY requirements.txt .

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential && rm -rf /var/lib/apt/lists/* && \
    pip install --no-cache-dir --upgrade -r requirements.txt && \
    apt-get purge -y build-essential && apt-get -y autoremove

# Copy requirements first to leverage Docker cache
# RUN pip install --no-cache-dir -U pip && uv sync

# Copy project files
COPY . .

# Expose the port the app will run on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
