# Use a lightweight Python base image
FROM python:3.13-slim

# Update essential system libraries
RUN apt-get update && apt-get install -y libglib2.0-0 && rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
WORKDIR /app

# Copy the dependencies file and install them first to leverage caching layers
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the rest of the project files into the container
COPY . .

# Expose the specific port for the Gradio interface
EXPOSE 7860

# Default command to run when the container starts
CMD ["python", "app.py"]
