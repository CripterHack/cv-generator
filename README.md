# CV Generator 📄✨

A modern, full-stack application for creating and managing professional CVs with both web and desktop interfaces.

## Table of Contents
1. [Features](#features)
2. [System Requirements](#system-requirements)
3. [Quick Start](#quick-start)
4. [Development Setup](#development-setup)
   - [Environment Configuration](#environment-configuration)
   - [Development Tools](#development-tools)
   - [Type System Setup](#type-system-setup)
   - [Using DevContainers (Recommended)](#using-devcontainers-recommended)
5. [Project Structure](#project-structure)
6. [Common Issues](#common-issues)
7. [Contributing](#contributing)
8. [Documentation](#documentation)
9. [License](#license)

## Features

- Bilingual support (English and Spanish) 🌎
- Real-time CV preview 👀
- Multiple export formats:
  - HTML 🌐
  - PDF 📑
  - Markdown ⬇️
- Save/load CV data (JSON) 💾
- Customizable sections:
  - Personal Information 👤
  - Professional Experience 💼
  - Academic Experience 🎓
  - Skills 🛠️
  - Certificates 🏆
- Profile photo support 🖼️

### Technical Features
- Modern tech stack:
  - Frontend: React + TypeScript + Material-UI
  - Backend: FastAPI + Python
  - Cache: Redis
  - Containers: Docker
- Advanced functionality:
  - Multiple CV templates
  - Form validation
  - Multi-language (i18n)
  - Real-time preview

## System Requirements

- Python 3.11.5
- Node.js 18+
- Docker 20.10.0+
- Docker Compose 2.0.0+
- wkhtmltopdf 0.12.6+
- 4GB RAM minimum
- 10GB free disk space

### Platform-Specific Setup

<details>
<summary>Windows Setup</summary>

```bash
# Install WSL2 if not installed
wsl --install

# Install Chocolatey (PowerShell as Admin)
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))

# Install dependencies
choco install python nodejs docker-desktop wkhtmltopdf git
```
</details>

<details>
<summary>macOS Setup</summary>

```bash
# Install Homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install dependencies
brew install python@3.11 node docker wkhtmltopdf git
```
</details>

<details>
<summary>Linux Setup</summary>

```bash
# Update and install
sudo apt update
sudo apt install -y python3.11 nodejs docker.io docker-compose wkhtmltopdf git
```
</details>

## Quick Start

1. Clone and setup:
   ```bash
   git clone https://github.com/yourusername/cv-generator.git
   cd cv-generator
   ```

2. Configure environment:
   ```bash
   cp web/backend/.env.example web/backend/.env
   cp web/frontend/.env.example web/frontend/.env
   ```

3. Start development environment:
   ```bash
   chmod +x dev.sh  # Unix-like systems
   ./dev.sh start
   ```

## Development Setup

### Environment Configuration

```bash
# Backend (.env)
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=True
REDIS_HOST=172.19.0.2
REDIS_PORT=6379

# Frontend (.env)
REACT_APP_API_URL=http://localhost:8000
```

### Development Tools

1. **Code Quality**
   - Linting: `npm run lint`
   - Formatting: `npm run format`
   - Type checking: `npm run type-check`

2. **Testing**
   - Run tests: `npm test`
   - Coverage: `npm run test:coverage`

3. **Build and Analysis**
   - Production build: `npm run build`
   - Bundle analysis: `npm run analyze`

### Type System Setup

```bash
# Install core type definitions
npm install --save-dev @types/react @types/react-dom @types/node
npm install --save-dev @types/axios @types/i18next
npm install --save-dev @types/jest @types/testing-library__react

# Verify installations
npm ls | grep "@types"
```

### Available Commands

#### Development Commands
- `npm start` - Start development server
- `npm run dev` - Start development server with hot reload
- `npm run build` - Create production build
- `npm run build:prod` - Create production build with production environment

#### Testing Commands
- `npm test` - Run tests in watch mode
- `npm run test:coverage` - Run tests with coverage report
- `npm run test:ci` - Run tests in CI mode (single run)

#### Code Quality Commands
- `npm run lint` - Check code style issues
- `npm run lint:fix` - Fix code style issues automatically
- `npm run format` - Format code with Prettier
- `npm run format:check` - Check code formatting
- `npm run type-check` - Check TypeScript types
- `npm run type-check:watch` - Check TypeScript types in watch mode

#### Analysis Commands
- `npm run analyze` - Analyze bundle size with source-map-explorer
- `npm run clean` - Remove build directories and cache
- `npm run ci` - Run all checks (types, lint, tests) - used in CI

#### Documentation Commands
- `npm run storybook` - Start Storybook development server
- `npm run build-storybook` - Build static Storybook documentation

#### Git Hooks
- `npm run prepare` - Install husky git hooks
- `npm run precommit` - Run pre-commit checks (automatically run by husky)

#### Examples
```bash
# Start development
npm run dev

# Run tests with coverage
npm run test:coverage

# Check and fix code style
npm run lint:fix
npm run format

# Prepare for production
npm run build:prod

# Run all checks before committing
npm run ci
```

### Using DevContainers (Recommended)

#### Prerequisites
1. Visual Studio Code
2. "Dev Containers" extension in VS Code
3. Docker Desktop (Windows/Mac) or Docker Engine (Linux)
4. Git

#### Setup Steps

1. **Initial Setup**
   ```bash
   # Clone the repository
   git clone https://github.com/yourusername/cv-generator.git
   cd cv-generator

   # Copy environment files
   cp web/backend/.env.example web/backend/.env
   cp web/frontend/.env.example web/frontend/.env
   ```

2. **Open in DevContainer**
   - Open VS Code
   - Press `F1` or `Ctrl+Shift+P`
   - Type "Dev Containers: Open Folder in Container"
   - Select the project folder

3. **Wait for Build**
   - Container will build automatically
   - VS Code will reconnect to container
   - Extensions will install automatically

4. **Start Services**
   ```bash
   # Grant execution permissions to dev script (if needed)
   chmod +x dev.sh

   # Start all services
   ./dev.sh start
   ```

5. **Verify Execution**
   - Backend API: http://localhost:8000
   - Frontend: http://localhost:3000
   - API Documentation: http://localhost:8000/docs

#### Useful Development Commands
```bash
# Restart services
./dev.sh restart

# View logs
./dev.sh logs

# Stop services
./dev.sh stop

# Run tests
./dev.sh test

# Clean containers and cache
./dev.sh clean
```

#### Troubleshooting

<details>
<summary>Port Issues</summary>

```bash
# Check ports in use
sudo lsof -i :8000
sudo lsof -i :3000

# Kill processes if needed
sudo kill -9 <PID>
```
</details>

<details>
<summary>Docker Permission Issues</summary>

```bash
# Add user to docker group (Linux)
sudo usermod -aG docker $USER
newgrp docker
```
</details>

<details>
<summary>Node Modules Issues</summary>

```bash
# Inside the container
cd web/frontend
rm -rf node_modules package-lock.json
npm install
```
</details>

<details>
<summary>Dependency Updates</summary>

```bash
# Rebuild container
./dev.sh rebuild
```
</details>

### Manual Setup (Alternative)

```bash
# Clone the repository
git clone https://github.com/yourusername/cv-generator.git
cd cv-generator

# Copy environment files
cp web/backend/.env.example web/backend/.env
cp web/frontend/.env.example web/frontend/.env

# Start development environment
chmod +x dev.sh
./dev.sh start
```

## Project Structure

```
cv-generator/
├── web/
│   ├── frontend/          # React application
│   │   ├── src/
│   │   │   ├── components/
│   │   │   ├── services/
│   │   │   ├── i18n/
│   │   │   └── types/
│   │   └── public/
│   └── backend/          # FastAPI application
├── shared/              # Shared utilities
├── docker/             # Docker configuration
└── tests/              # Test suites
```

## Common Issues

<details>
<summary>TypeScript/Linter Issues</summary>

- Missing module declarations:
  ```bash
  rm -rf node_modules package-lock.json
  npm install
  ```
- Type checking errors:
  ```bash
  npm run type-check
  npm run lint:fix
  ```
</details>

<details>
<summary>Docker Issues</summary>

- Permission errors:
  ```bash
  sudo usermod -aG docker $USER  # Linux/macOS
  ```
- Cache problems:
  ```bash
  docker system prune -a
  docker-compose build --no-cache
  ```
</details>

<details>
<summary>Development Server Issues</summary>

- Hot reload not working:
  ```bash
  npm run dev
  # Or with Docker
  ./dev.sh restart
  ```
</details>

## Contributing

1. Fork and clone
2. Create feature branch
3. Make changes
4. Run tests and linting
5. Submit pull request

For detailed guidelines, see [CONTRIBUTING.md](CONTRIBUTING.md)

## Documentation

- API Documentation: `/docs` endpoint
- Frontend Documentation: Generated with Storybook
- Code Documentation: Inline documentation and type hints

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
