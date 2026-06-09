# Step 1: Base image — OS + Python version pre-installed
FROM python:3.12-slim

# Step 2: Set working directory inside container
WORKDIR /main

# Step 3: Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Step 4: Copy all application code
COPY . .
# Step 5: Expose the port FastAPI runs on
EXPOSE 8000

# Step 6: Command to run the API
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
