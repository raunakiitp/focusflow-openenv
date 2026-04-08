FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose the standard Gradio port for Hugging Face Spaces
EXPOSE 7860

# Run the UI app to keep the container alive instead of the single-run inference script
CMD ["python", "app.py"]
