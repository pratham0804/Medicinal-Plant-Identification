# Use the official Python image from Docker Hub
FROM python:3.11-slim

# Install Git and Git LFS
RUN apt-get update && apt-get install -y git curl && \
    curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.sh | bash && \
    git lfs install

# Set the working directory inside the container
WORKDIR /app

# Copy your entire project into the container
COPY . .

# Install Python dependencies
RUN pip install -r backend/requirements.txt

# Pull the Git LFS files
RUN git lfs pull

# Set the command to run your app using gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:5000", "backend.app:app"]
