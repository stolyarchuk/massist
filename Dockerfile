# Build stage
FROM python:3.11-slim AS builder

WORKDIR /app

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PIP_ROOT_USER_ACTION=ignore

COPY requirements.txt .
COPY pyproject.toml uv.lock* ./

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential git curl && pip install -U pip uv

# Install dependencies into a specific directory for easier copying
RUN --mount=type=bind,source=requirements.txt,target=requirements.txt \
    uv pip install --system --target=/install -r requirements.txt

# Final stage using distroless image
FROM gcr.io/distroless/python3-debian12

WORKDIR /app

ENV PYTHONUNBUFFERED=1

# Copy dependencies from builder stage
COPY --from=builder /install /usr/lib/python3.11

# Copy application code
COPY . .

EXPOSE 8000

# CMD in exec form
CMD ["-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
