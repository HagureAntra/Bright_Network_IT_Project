# Use slim Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy project files into container
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose Flask port
EXPOSE 5000

# Run the Flask app
CMD ["python", "app.py"]
