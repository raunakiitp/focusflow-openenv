FROM python:3.11-slim

WORKDIR /app

# Install uv
RUN pip install uv openenv-core

# Copy the whole repo
COPY . /app

# Install dependencies
RUN pip install -r server/requirements.txt || pip install fastapi uvicorn pydantic openenv-core openai

ENV PYTHONPATH="/app:$PYTHONPATH"

EXPOSE 7860

CMD ["uvicorn", "server.app:app", "--host", "0.0.0.0", "--port", "7860"]
