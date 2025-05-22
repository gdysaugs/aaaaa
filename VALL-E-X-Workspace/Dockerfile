# Stage 1: Build stage with Git LFS
FROM ubuntu:22.04 AS builder

# Install Git, Git LFS, and ca-certificates
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    git \
    git-lfs \
    ca-certificates \
    wget \
    python3 \
    python3-pip && \
    rm -rf /var/lib/apt/lists/*

# Set up Python
RUN ln -s /usr/bin/python3 /usr/bin/python

# Initialize Git LFS
RUN git lfs install --system

# Clone the repository
WORKDIR /app
RUN git clone https://github.com/Plachtaa/VALL-E-X.git .

# Fetch LFS objects
RUN git lfs fetch --all

# Checkout LFS files
RUN git lfs checkout

# Patch the generation.py file to fix PyTorch 2.6 compatibilities
RUN sed -i 's/checkpoint = torch.load(os.path.join(checkpoints_dir, model_checkpoint_name), map_location='\''cpu'\'')/checkpoint = torch.load(os.path.join(checkpoints_dir, model_checkpoint_name), map_location='\''cpu'\'', weights_only=False)/g' /app/utils/generation.py

# Install Python dependencies
# Ensure requirements.txt exists before running this command
RUN if [ -f requirements.txt ]; then pip3 install --no-cache-dir -r requirements.txt; else echo "requirements.txt not found, skipping pip install -r requirements.txt"; fi
RUN pip3 install --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
RUN pip3 install --no-cache-dir gradio

# Download models
RUN mkdir -p ./checkpoints && python -c "from utils.generation import preload_models; preload_models()"

# Download NLTK data
RUN python -c "import nltk; nltk.download('punkt', download_dir='./nltk_data')"

# Stage 2: Runtime stage
FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04

# Install libexpat1 and other Python build dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libexpat1 \
    python3 \
    python3-pip \
    python3-venv \
    wget \
    ca-certificates \
    git \
    ffmpeg \
    git-lfs && \
    rm -rf /var/lib/apt/lists/*

# Set up Python, ensure it's python3 and pip3
RUN ln -sf /usr/bin/python3 /usr/bin/python && \
    ln -sf /usr/bin/pip3 /usr/bin/pip

WORKDIR /app

# Copy only the application code and necessary scripts/data from builder stage
COPY --from=builder /app /app

# Re-install Python dependencies in the runtime stage
# This ensures that the Python environment is clean and compatible with the base image
RUN if [ -f requirements.txt ]; then pip install --no-cache-dir -r requirements.txt; else echo "requirements.txt not found, skipping pip install -r requirements.txt"; fi
RUN pip install --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
RUN pip install --no-cache-dir gradio

# Copy NLTK data
COPY --from=builder /app/nltk_data /app/nltk_data

# Set environment variables
ENV NVIDIA_VISIBLE_DEVICES=all
ENV NVIDIA_DRIVER_CAPABILITIES=compute,utility
ENV NLTK_DATA=/app/nltk_data

# Expose port for Gradio UI (optional)
EXPOSE 7860

# Set the entrypoint
CMD ["python3", "-X", "utf8", "launch-ui.py", "--share"] 