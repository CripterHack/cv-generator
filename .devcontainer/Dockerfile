FROM mcr.microsoft.com/vscode/devcontainers/python:3.11

# Instalar Node.js y herramientas adicionales
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get update \
    && apt-get install -y nodejs netcat-traditional \
    && npm install -g npm@latest \
    && (which yarn || npm install -g yarn)

# Instalar Docker CLI
RUN apt-get update && apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    lsb-release \
    && curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg \
    && echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/debian $(lsb_release -cs) stable" > /etc/apt/sources.list.d/docker.list \
    && apt-get update \
    && apt-get install -y docker-ce-cli

# Instalar dependencias del sistema con cleanup
RUN apt-get update && apt-get install -y \
    wkhtmltopdf \
    xvfb \
    libgl1-mesa-glx \
    git \
    curl \
    wget \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Crear usuario no root y configurar Docker
ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID

RUN if ! getent group docker >/dev/null; then \
    groupadd docker; \
    fi \
    && if ! getent group vscode >/dev/null; then \
    groupadd --gid 1000 vscode; \
    fi \
    && if ! getent passwd vscode >/dev/null; then \
    useradd --uid 1000 --gid 1000 -m vscode; \
    fi \
    && usermod -aG docker vscode \
    && apt-get update \
    && apt-get install -y sudo \
    && echo vscode ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/vscode \
    && chmod 0440 /etc/sudoers.d/vscode

# Configurar el directorio de trabajo
WORKDIR /workspace

# Instalar herramientas de desarrollo Python
RUN pip install --no-cache-dir black pylint mypy pytest coverage

# Configurar git para el usuario vscode
USER $USERNAME
RUN git config --global core.editor "code --wait" \
    && git config --global init.defaultBranch main

USER root

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