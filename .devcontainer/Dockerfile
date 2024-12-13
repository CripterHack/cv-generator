FROM mcr.microsoft.com/vscode/devcontainers/python:3.11

# Install wkhtmltopdf and X11/GUI dependencies
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends \
    wkhtmltopdf \
    python3-tk \
    python3-pil.imagetk \
    libx11-6 \
    x11-utils \
    xauth \
    libxext6 \
    libxrender1 \
    libxtst6 \
    libxi6 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install additional Python packages
RUN pip install --no-cache-dir black pylint

# Create the workspace directory
WORKDIR /workspace

# Copy requirements
COPY requirements.txt /tmp/pip-tmp/
RUN pip3 --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/requirements.txt \
    && rm -rf /tmp/pip-tmp

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV QT_X11_NO_MITSHM=1
ENV DISPLAY=host.docker.internal:0.0

# Create .Xauthority file
RUN touch /home/vscode/.Xauthority \
    && chown vscode:vscode /home/vscode/.Xauthority