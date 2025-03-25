# Generador de CV 📄✨

Una aplicación moderna full-stack para crear y gestionar CVs profesionales con interfaces web y de escritorio.

## Tabla de Contenidos
1. [Características](#características)
2. [Requisitos del Sistema](#requisitos-del-sistema)
3. [Inicio Rápido](#inicio-rápido)
4. [Configuración de Desarrollo](#configuración-de-desarrollo)
   - [Configuración del Entorno](#configuración-del-entorno)
   - [Herramientas de Desarrollo](#herramientas-de-desarrollo)
   - [Configuración del Sistema de Tipos](#configuración-del-sistema-de-tipos)
5. [Estructura del Proyecto](#estructura-del-proyecto)
6. [Problemas Comunes](#problemas-comunes)
7. [Contribuir](#contribuir)
8. [Documentación](#documentación)
9. [Licencia](#licencia)

## Características

- Soporte bilingüe (Inglés y Español) 🌎
- Vista previa en tiempo real 👀
- Múltiples formatos de exportación:
  - HTML 🌐
  - PDF 📑
  - Markdown ⬇️
- Guardar/cargar datos de CV (JSON) 💾
- Secciones personalizables:
  - Información Personal 👤
  - Experiencia Profesional 💼
  - Experiencia Académica 🎓
  - Habilidades 🛠️
  - Certificados 🏆
- Soporte para foto de perfil 🖼️

### Características Técnicas
- Stack tecnológico moderno:
  - Frontend: React + TypeScript + Material-UI
  - Backend: FastAPI + Python
  - Caché: Redis
  - Contenedores: Docker
- Funcionalidad avanzada:
  - Múltiples plantillas de CV
  - Validación de formularios
  - Multi-idioma (i18n)
  - Vista previa en tiempo real

## Requisitos del Sistema

- Python 3.11.5
- Node.js 18+
- Docker 20.10.0+
- Docker Compose 2.0.0+
- wkhtmltopdf 0.12.6+
- 4GB RAM mínimo
- 10GB espacio libre en disco

### Configuración por Plataforma

<details>
<summary>Configuración Windows</summary>

```bash
# Instalar WSL2 si no está instalado
wsl --install

# Instalar Chocolatey (PowerShell como Admin)
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))

# Instalar dependencias
choco install python nodejs docker-desktop wkhtmltopdf git
```
</details>

<details>
<summary>Configuración macOS</summary>

```bash
# Instalar Homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Instalar dependencias
brew install python@3.11 node docker wkhtmltopdf git
```
</details>

<details>
<summary>Configuración Linux</summary>

```bash
# Actualizar e instalar
sudo apt update
sudo apt install -y python3.11 nodejs docker.io docker-compose wkhtmltopdf git
```
</details>

## Inicio Rápido

1. Clonar y configurar:
   ```bash
   git clone https://github.com/yourusername/cv-generator.git
   cd cv-generator
   ```

2. Configurar entorno:
   ```bash
   cp web/backend/.env.example web/backend/.env
   cp web/frontend/.env.example web/frontend/.env
   ```

3. Iniciar entorno de desarrollo:
   ```bash
   chmod +x dev.sh  # Sistemas Unix
   ./dev.sh start
   ```

## Configuración de Desarrollo

### Usando DevContainers (Recomendado)

#### Prerrequisitos
1. Visual Studio Code
2. Extensión "Dev Containers" en VS Code
3. Docker Desktop (Windows/Mac) o Docker Engine (Linux)
4. Git

#### Pasos de Configuración

1. **Configuración Inicial**
   ```bash
   # Clonar el repositorio
   git clone https://github.com/yourusername/cv-generator.git
   cd cv-generator

   # Copiar archivos de entorno
   cp web/backend/.env.example web/backend/.env
   cp web/frontend/.env.example web/frontend/.env
   ```

2. **Abrir en DevContainer**
   - Abrir VS Code
   - Presionar `F1` o `Ctrl+Shift+P`
   - Escribir "Dev Containers: Open Folder in Container"
   - Seleccionar la carpeta del proyecto

3. **Esperar la Construcción**
   - El contenedor se construirá automáticamente
   - VS Code se reconectará al contenedor
   - Las extensiones se instalarán automáticamente

4. **Iniciar Servicios**
   ```bash
   # Dar permisos de ejecución al script de desarrollo (si es necesario)
   chmod +x dev.sh

   # Iniciar todos los servicios
   ./dev.sh start
   ```

5. **Verificar la Ejecución**
   - Backend API: http://localhost:8000
   - Frontend: http://localhost:3000
   - Documentación API: http://localhost:8000/docs

#### Comandos Útiles para Desarrollo
```bash
# Reiniciar servicios
./dev.sh restart

# Ver logs
./dev.sh logs

# Detener servicios
./dev.sh stop

# Ejecutar pruebas
./dev.sh test

# Limpiar contenedores y caché
./dev.sh clean
```

#### Solución de Problemas

<details>
<summary>Problemas con Puertos</summary>

```bash
# Verificar puertos en uso
sudo lsof -i :8000
sudo lsof -i :3000

# Detener procesos si es necesario
sudo kill -9 <PID>
```
</details>

<details>
<summary>Problemas con Permisos de Docker</summary>

```bash
# Agregar usuario al grupo docker (Linux)
sudo usermod -aG docker $USER
newgrp docker
```
</details>

<details>
<summary>Problemas con Node Modules</summary>

```bash
# Dentro del contenedor
cd web/frontend
rm -rf node_modules package-lock.json
npm install
```
</details>

<details>
<summary>Actualización de Dependencias</summary>

```bash
# Reconstruir contenedor
./dev.sh rebuild
```
</details>

### Configuración Manual (Alternativa)

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

### Herramientas de Desarrollo

1. **Calidad de Código**
   - Linting: `npm run lint`
   - Formateo: `npm run format`
   - Verificación de tipos: `npm run type-check`

2. **Pruebas**
   - Ejecutar pruebas: `npm test`
   - Cobertura: `npm run test:coverage`

3. **Construcción y Análisis**
   - Construcción para producción: `npm run build`
   - Análisis de bundle: `npm run analyze`

### Configuración del Sistema de Tipos

```bash
# Instalar definiciones de tipos principales
npm install --save-dev @types/react @types/react-dom @types/node
npm install --save-dev @types/axios @types/i18next
npm install --save-dev @types/jest @types/testing-library__react

# Verificar instalaciones
npm ls | grep "@types"
```

## Comandos Disponibles

### Comandos de Desarrollo
- `npm start` - Iniciar servidor de desarrollo
- `npm run dev` - Iniciar servidor de desarrollo con recarga en caliente
- `npm run build` - Crear build de producción
- `npm run build:prod` - Crear build de producción con entorno de producción

### Comandos de Pruebas
- `npm test` - Ejecutar pruebas en modo observador
- `npm run test:coverage` - Ejecutar pruebas con reporte de cobertura
- `npm run test:ci` - Ejecutar pruebas en modo CI (una sola vez)

### Comandos de Calidad de Código
- `npm run lint` - Verificar problemas de estilo de código
- `npm run lint:fix` - Corregir problemas de estilo de código automáticamente
- `npm run format` - Formatear código con Prettier
- `npm run format:check` - Verificar formato del código
- `npm run type-check` - Verificar tipos de TypeScript
- `npm run type-check:watch` - Verificar tipos de TypeScript en modo observador

### Comandos de Análisis
- `npm run analyze` - Analizar tamaño del bundle con source-map-explorer
- `npm run clean` - Eliminar directorios de build y caché
- `npm run ci` - Ejecutar todas las verificaciones (tipos, lint, pruebas) - usado en CI

### Comandos de Documentación
- `npm run storybook` - Iniciar servidor de desarrollo de Storybook
- `npm run build-storybook` - Construir documentación estática de Storybook

### Hooks de Git
- `npm run prepare` - Instalar hooks de git con husky
- `npm run precommit` - Ejecutar verificaciones pre-commit (ejecutado automáticamente por husky)

### Ejemplos
```bash
# Iniciar desarrollo
npm run dev

# Ejecutar pruebas con cobertura
npm run test:coverage

# Verificar y corregir estilo de código
npm run lint:fix
npm run format

# Preparar para producción
npm run build:prod

# Ejecutar todas las verificaciones antes de commit
npm run ci
```

## Estructura del Proyecto

```
cv-generator/
├── web/
│   ├── frontend/          # Aplicación React
│   │   ├── src/
│   │   │   ├── components/
│   │   │   ├── services/
│   │   │   ├── i18n/
│   │   │   └── types/
│   │   └── public/
│   └── backend/          # Aplicación FastAPI
├── shared/              # Utilidades compartidas
├── docker/             # Configuración de Docker
└── tests/              # Suites de pruebas
```

## Problemas Comunes

<details>
<summary>Problemas de TypeScript/Linter</summary>

- Declaraciones de módulos faltantes:
  ```bash
  rm -rf node_modules package-lock.json
  npm install
  ```
- Errores de verificación de tipos:
  ```bash
  npm run type-check
  npm run lint:fix
  ```
</details>

<details>
<summary>Problemas de Docker</summary>

- Errores de permisos:
  ```bash
  sudo usermod -aG docker $USER  # Linux/macOS
  ```
- Problemas de caché:
  ```bash
  docker system prune -a
  docker-compose build --no-cache
  ```
</details>

<details>
<summary>Problemas del Servidor de Desarrollo</summary>

- Hot reload no funciona:
  ```bash
  npm run dev
  # O con Docker
  ./dev.sh restart
  ```
</details>

## Contribuir

1. Fork y clonar
2. Crear rama de funcionalidad
3. Realizar cambios
4. Ejecutar pruebas y linting
5. Enviar pull request

Para guías detalladas, ver [CONTRIBUTING.md](CONTRIBUTING.md)

## Documentación

- Documentación API: Endpoint `/docs`
- Documentación Frontend: Generada con Storybook
- Documentación Código: Documentación inline y hints de tipos

## Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.
  