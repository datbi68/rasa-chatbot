FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Train model if not exists
RUN if [ ! -f "models/*.tar.gz" ]; then rasa train; fi

# Expose port
EXPOSE 5005

# Run Rasa
CMD ["rasa", "run", "--enable-api", "--cors", "*", "--port", "5005"]
