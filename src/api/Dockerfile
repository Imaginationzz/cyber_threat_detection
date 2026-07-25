# Use a lightweight Python image
FROM python:3.9-slim

# Create a non-root user for security
RUN useradd -m -r appuser

# Set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY src/api/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the API code into the container
COPY src/api/app.py .

# Change ownership of the app directory to the non-root user
RUN chown -R appuser:appuser /app

# Switch to the non-root user
USER appuser

# Expose the port the app runs on
EXPOSE 8000

# Command to run the API using Uvicorn

CMD ["python", "-m", "uvicorn", "src.api.app:app", "--host", "0.0.0.0", "--port", "8000"]