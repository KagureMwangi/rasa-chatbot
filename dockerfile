# Use official Rasa base image
FROM rasa/rasa:3.6.10

# Set working directory
WORKDIR /app

# Copy project files into the container
COPY . /app

# Install additional dependencies (Supabase, etc.)
RUN pip install --no-cache-dir -r requirements.txt

# Run Rasa server with API and CORS support
CMD ["run", "--enable-api", "--cors", "*", "--debug"]
