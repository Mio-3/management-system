# Start with the official FastAPI image
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

# Set the working directory
WORKDIR /business-management/fastapi

# Copy the requirements file
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the FastAPI app
COPY . .

# Expose the port
EXPOSE 8000

# Run the app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]