FROM python:3.12-slim

WORKDIR /app

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PIP_ROOT_USER_ACTION=ignore

COPY requirements.txt .
COPY pyproject.toml uv.lock* ./

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential git curl && pip install -U pip uv

RUN uv pip install --system -r requirements.txt && \
    apt-get purge -y build-essential && apt-get -y autoremove && \
    apt-get clean all && rm -rf /var/lib/apt/lists/*

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
