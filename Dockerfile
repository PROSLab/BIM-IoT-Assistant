# Use Python 3.12 base image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose the Streamlit port
EXPOSE 8501

ENV PYTHONUNBUFFERED=1

# Command to run the application
CMD ["streamlit", "run", "bot.py"]
