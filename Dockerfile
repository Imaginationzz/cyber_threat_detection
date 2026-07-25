# Use an official lightweight Python image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all your project files into the container
COPY . .

# Expose the port that FastAPI runs on
EXPOSE 8000

# Command to start the API
# NOTE: This assumes your FastAPI app is inside the "src" folder in a file named "main.py"
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]