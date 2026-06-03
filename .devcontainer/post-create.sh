#!/bin/bash
set -e

echo "🚀 Iniciando configuración del entorno de desarrollo..."

# Configurar permisos de npm para el usuario vscode
echo "🔧 Configurando permisos de npm..."
mkdir -p /home/vscode/.npm-global
npm config set prefix '/home/vscode/.npm-global'
export PATH=/home/vscode/.npm-global/bin:$PATH
echo 'export PATH=/home/vscode/.npm-global/bin:$PATH' >> /home/vscode/.bashrc

# Verificar requisitos del sistema
echo "📋 Verificando requisitos del sistema..."
python3 --version
node --version
npm --version
docker --version
docker-compose --version

# Configurar git
echo "🔧 Configurando git..."
git config --global pull.rebase true
git config --global core.autocrlf input

# Crear estructura de directorios si no existe
echo "📁 Creando estructura de directorios..."
mkdir -p web/backend
mkdir -p web/frontend

# Instalar dependencias del backend
echo "📦 Instalando dependencias del backend..."
cd web/backend
if [ ! -f "requirements.txt" ]; then
    cat > requirements.txt << EOL
fastapi==0.95.2
uvicorn==0.22.0
python-multipart==0.0.6
pydantic==1.10.12
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-dotenv==1.0.0
redis==4.5.5
starlette==0.27.0
EOL
fi

# Instalar pip y las dependencias
python3 -m pip install --upgrade pip
pip install -r requirements.txt

# Instalar dependencias del frontend
echo "📦 Instalando dependencias del frontend..."
cd ../frontend
if [ ! -f "package.json" ]; then
    # Crear package.json inicial
    cat > package.json << EOL
{
  "name": "cv-generator-frontend",
  "version": "0.1.0",
  "private": true,
  "dependencies": {
    "@emotion/react": "^11.11.3",
    "@emotion/styled": "^11.11.0",
    "@mui/icons-material": "^5.15.1",
    "@mui/material": "^5.15.1",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-hook-form": "^7.49.2",
    "web-vitals": "^2.1.4"
  },
  "devDependencies": {
    "@types/node": "^20.10.6",
    "@types/react": "^18.2.45",
    "@types/react-dom": "^18.2.18",
    "react-scripts": "5.0.1",
    "typescript": "^4.9.5"
  },
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test",
    "eject": "react-scripts eject"
  },
  "eslintConfig": {
    "extends": [
      "react-app",
      "react-app/jest"
    ]
  },
  "browserslist": {
    "production": [
      ">0.2%",
      "not dead",
      "not op_mini all"
    ],
    "development": [
      "last 1 chrome version",
      "last 1 firefox version",
      "last 1 safari version"
    ]
  }
}
EOL

    # Instalar todas las dependencias
    npm install --legacy-peer-deps

    # Crear carpetas necesarias
    mkdir -p src public
    mkdir -p node_modules/.bin

    # Asegurar que react-scripts esté disponible
    npm install -g npm@latest
    npm install --save-dev react-scripts@5.0.1
    npm link react-scripts

    # Configurar TypeScript
    cat > tsconfig.json << EOL
{
  "compilerOptions": {
    "target": "es5",
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": true,
    "skipLibCheck": true,
    "esModuleInterop": true,
    "allowSyntheticDefaultImports": true,
    "strict": true,
    "forceConsistentCasingInFileNames": true,
    "noFallthroughCasesInSwitch": true,
    "module": "esnext",
    "moduleResolution": "node",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx"
  },
  "include": ["src"]
}
EOL
fi

# Crear archivos iniciales si no existen
echo "📝 Creando archivos iniciales..."

# Backend
cd ../backend
if [ ! -f "main.py" ]; then
    cat > main.py << EOL
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
import redis

load_dotenv()

app = FastAPI(title="CV Generator API")

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configurar Redis
redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "172.19.0.2"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    password=os.getenv("REDIS_PASSWORD", "RedisPassword123!"),
    decode_responses=True
)

@app.get("/")
async def root():
    try:
        redis_client.ping()
        redis_status = "conectado"
    except:
        redis_status = "desconectado"
    return {
        "message": "CV Generator API está funcionando!",
        "redis_status": redis_status
    }
EOL
fi

# Frontend
cd ../frontend
mkdir -p src public
if [ ! -f "src/index.tsx" ]; then
    cat > src/index.tsx << EOL
import React from 'react';
import ReactDOM from 'react-dom/client';
import { ThemeProvider, createTheme } from '@mui/material';
import App from './App';

const theme = createTheme({
  palette: {
    mode: 'light',
  },
});

const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);

root.render(
  <React.StrictMode>
    <ThemeProvider theme={theme}>
      <App />
    </ThemeProvider>
  </React.StrictMode>
);
EOL

    cat > src/App.tsx << EOL
import React from 'react';
import { Container, Typography, Box, TextField, Button, Paper } from '@mui/material';
import { useForm } from 'react-hook-form';

interface FormData {
  name: string;
  email: string;
}

function App() {
  const { register, handleSubmit, formState: { errors } } = useForm<FormData>();

  const onSubmit = (data: FormData) => {
    console.log(data);
  };

  return (
    <Container maxWidth="lg">
      <Box sx={{ my: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          CV Generator
        </Typography>
        <Paper sx={{ p: 3 }}>
          <form onSubmit={handleSubmit(onSubmit)}>
            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
              <TextField
                label="Nombre"
                {...register("name", { required: "El nombre es requerido" })}
                error={!!errors.name}
                helperText={errors.name?.message}
              />
              <TextField
                label="Email"
                {...register("email", {
                  required: "El email es requerido",
                  pattern: {
                    value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
                    message: "Email inválido"
                  }
                })}
                error={!!errors.email}
                helperText={errors.email?.message}
              />
              <Button type="submit" variant="contained" color="primary">
                Enviar
              </Button>
            </Box>
          </form>
        </Paper>
      </Box>
    </Container>
  );
}

export default App;
EOL

    cat > public/index.html << EOL
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="utf-8" />
    <link rel="icon" type="image/png" href="%PUBLIC_URL%/favicon-96x96.png" sizes="96x96" />
    <link rel="icon" type="image/svg+xml" href="%PUBLIC_URL%/favicon.svg" />
    <link rel="shortcut icon" href="%PUBLIC_URL%/favicon.ico" />
    <link rel="apple-touch-icon" sizes="180x180" href="%PUBLIC_URL%/apple-touch-icon.png" />
    <meta name="apple-mobile-web-app-title" content="IzignaMx" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="theme-color" content="#000000" />
    <meta
      name="description"
      content="CV Generator - Crea tu currículum vitae profesional"
    />
    <link rel="manifest" href="%PUBLIC_URL%/manifest.json" />
    <title>CV Generator</title>
  </head>
  <body>
    <noscript>Necesitas habilitar JavaScript para ejecutar esta aplicación.</noscript>
    <div id="root"></div>
  </body>
</html> 
EOL

    # Crear manifest.json
    cat > public/manifest.json << EOL
{
  "short_name": "CV Generator",
  "name": "CV Generator - Crea tu CV profesional",
  "start_url": ".",
  "display": "standalone",
  "theme_color": "#000000",
  "background_color": "#ffffff"
}
EOL

    # Crear .gitignore
    cat > .gitignore << EOL
# dependencies
/node_modules
/.pnp
.pnp.js

# testing
/coverage

# production
/build

# misc
.DS_Store
.env.local
.env.development.local
.env.test.local
.env.production.local

npm-debug.log*
yarn-debug.log*
yarn-error.log*
EOL

    # Crear README.md
    cat > README.md << EOL
# CV Generator Frontend

Este es el frontend de la aplicación CV Generator, construido con React y Material-UI.

## Scripts Disponibles

En el directorio del proyecto, puedes ejecutar:

### \`npm start\`

Ejecuta la aplicación en modo desarrollo.
Abre [http://localhost:3000](http://localhost:3000) para verla en el navegador.

### \`npm test\`

Ejecuta los tests en modo interactivo.

### \`npm run build\`

Construye la aplicación para producción en la carpeta \`build\`.
EOL
fi

# Configurar entornos
echo "⚙️ Configurando variables de entorno..."

# Backend (only if .env doesn't exist)
if [ ! -f ../backend/.env ]; then
    cat > ../backend/.env << EOL
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=True
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=
CORS_ORIGINS=["http://localhost:3000"]
EOL
fi

# Frontend (only if .env doesn't exist)
if [ ! -f ../frontend/.env ]; then
    cat > ../frontend/.env << EOL
REACT_APP_API_URL=http://localhost:8000
REACT_APP_DEFAULT_LANGUAGE=es
REACT_APP_ENABLE_MOCK_API=false
EOL
fi

# Crear y configurar scripts de desarrollo
echo "📝 Creando scripts de desarrollo..."

# Crear dev.sh si no existe
cd ../..
cat > dev.sh << EOL
#!/bin/bash

# Función para manejar la señal SIGINT (Ctrl+C)
trap 'kill 0' SIGINT

# Iniciar servicios en paralelo
echo "🚀 Iniciando servicios..."

# Iniciar backend
cd web/backend
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload &

# Iniciar frontend
cd ../frontend
npm start &

# Esperar a que todos los procesos terminen
wait
EOL

# Dar permisos de ejecución
chmod +x dev.sh
if [ -f ".devcontainer/startup.sh" ]; then
    chmod +x .devcontainer/startup.sh
fi

echo "✅ Configuración completada exitosamente!"