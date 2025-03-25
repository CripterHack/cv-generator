# Guía de Estilo de Código y Documentación

## Estilo de Código TypeScript/JavaScript

### Organización de Archivos

```typescript
// 1. Importaciones
import React from 'react';
import { useTranslation } from 'react-i18next';

// 2. Tipos/Interfaces
interface Props {
  name: string;
  age?: number;
}

// 3. Componente/Función
export const MyComponent: React.FC<Props> = ({ name, age }) => {
  // Implementación
};
```

### Anotaciones de Tipo

```typescript
// Usar anotaciones de tipo explícitas para APIs públicas
export function calculateAge(birthDate: Date): number {
  // Implementación
}

// Dejar que TypeScript infiera tipos para variables internas
const today = new Date();
```

### Comentarios y Documentación

```typescript
/**
 * Genera un CV en el formato especificado.
 * 
 * @param data - Los datos del CV a generar
 * @param format - Formato de salida (pdf, html, markdown)
 * @returns Promise que resuelve al CV generado
 * @throws {ValidationError} Si los datos del CV son inválidos
 */
async function generateCV(
  data: CVData,
  format: OutputFormat
): Promise<GeneratedCV> {
  // Implementación
}

// Usar comentarios en línea con moderación, solo para lógica compleja
function complexCalculation() {
  // Primero, normalizar los valores de entrada
  const normalized = normalizeValues();
  
  // Luego aplicar la matriz de transformación
  const transformed = applyMatrix(normalized);
}
```

## Estilo de Código Python

### Organización de Archivos

```python
"""Docstring del módulo explicando su propósito."""

# 1. Importaciones de biblioteca estándar
import os
from typing import Dict, List

# 2. Importaciones de terceros
from fastapi import FastAPI
import pydantic

# 3. Importaciones locales
from .models import CV
from .utils import generate_pdf

# 4. Constantes
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

# 5. Clases/Funciones
class CVGenerator:
    """Docstring de la clase explicando su propósito."""
```

### Sugerencias de Tipo

```python
from typing import Optional, List, Dict

def process_cv(
    data: Dict[str, any],
    format: str = "pdf",
    include_photo: bool = True
) -> Optional[bytes]:
    """
    Procesa y genera CV en el formato especificado.
    
    Args:
        data: Diccionario conteniendo datos del CV
        format: Formato de salida (pdf, html, markdown)
        include_photo: Si se debe incluir foto en la salida
        
    Returns:
        Bytes del CV generado o None si falla la generación
        
    Raises:
        ValueError: Si el formato no es soportado
    """
    # Implementación
```

### Docstrings

```python
class CVTemplate:
    """
    Maneja la renderización y personalización de plantillas de CV.
    
    Attributes:
        name: Nombre de la plantilla
        style: Estilo CSS para la plantilla
        
    Example:
        >>> template = CVTemplate("modern")
        >>> html = template.render(cv_data)
    """
    
    def render(self, data: Dict[str, any]) -> str:
        """
        Renderiza datos del CV usando la plantilla.
        
        Args:
            data: Diccionario conteniendo datos del CV
            
        Returns:
            Cadena HTML renderizada
            
        Raises:
            TemplateError: Si falla la renderización
        """
        # Implementación
```

## Directrices Generales

### Convenciones de Nombres

```typescript
// TypeScript/JavaScript
const MAX_FILE_SIZE = 5 * 1024 * 1024;  // Constantes en UPPER_SNAKE_CASE
const userData = {};  // Variables en camelCase
function calculateTotal() {}  // Funciones en camelCase
class UserProfile {}  // Clases en PascalCase
interface UserData {}  // Interfaces en PascalCase
```

```python
# Python
MAX_FILE_SIZE = 5 * 1024 * 1024  # Constantes en UPPER_SNAKE_CASE
user_data = {}  # Variables en snake_case
def calculate_total():  # Funciones en snake_case
    pass
class UserProfile:  # Clases en PascalCase
    pass
```

### Manejo de Errores

```typescript
// TypeScript
try {
  await generateCV(data);
} catch (error) {
  if (error instanceof ValidationError) {
    logger.warn('Validación fallida:', error);
    throw new UserFacingError('Datos de CV inválidos');
  }
  logger.error('Error inesperado:', error);
  throw new UserFacingError('Error interno');
}
```

```python
# Python
try:
    generate_cv(data)
except ValidationError as e:
    logger.warning(f"Validación fallida: {e}")
    raise UserFacingError("Datos de CV inválidos")
except Exception as e:
    logger.error(f"Error inesperado: {e}")
    raise UserFacingError("Error interno")
```

### Organización del Código

1. **Agrupación Lógica**
   - Agrupar funcionalidad relacionada
   - Mantener archivos enfocados y con propósito único
   - Usar estructura de directorios significativa

2. **Gestión de Dependencias**
   - Minimizar dependencias externas
   - Mantener dependencias actualizadas
   - Documentar versiones requeridas

3. **Pruebas**
   - Escribir pruebas junto al código
   - Incluir pruebas unitarias y de integración
   - Documentar requisitos y configuración de pruebas

### Mejores Prácticas

1. **Calidad del Código**
   - Seguir el principio DRY (No te repitas)
   - Escribir código autodocumentado
   - Usar nombres de variables significativos

2. **Rendimiento**
   - Optimizar rutas críticas
   - Usar estructuras de datos apropiadas
   - Documentar consideraciones de rendimiento

3. **Seguridad**
   - Validar todas las entradas
   - Sanitizar salidas
   - Manejar datos sensibles apropiadamente

## Proceso de Revisión de Código

### Directrices de Pull Request
- Crear un PR para todos los cambios
- Proporcionar descripción clara de los cambios
- Enlazar issues relacionados
- Incluir cobertura de pruebas
- Actualizar documentación

### Lista de Verificación
1. Calidad del Código
   - Sigue la guía de estilo
   - Sin code smells
   - Manejo apropiado de errores
   
2. Pruebas
   - Pruebas unitarias añadidas/actualizadas
   - Pruebas de integración si son necesarias
   - Todas las pruebas pasan
   
3. Documentación
   - Comentarios de código donde sea necesario
   - Documentación de API actualizada
   - README actualizado si es necesario

4. Seguridad
   - Sin datos sensibles expuestos
   - Validación de entradas
   - Manejo apropiado de errores

### Proceso de Revisión
1. Enviar PR
2. Ejecución de verificaciones automatizadas
3. Se requiere al menos una aprobación
4. Atender feedback
5. Fusionar cuando esté aprobado

## Versionado

Seguimos el Versionado Semántico (MAJOR.MINOR.PATCH):

### Números de Versión
- MAJOR: Cambios incompatibles
- MINOR: Nuevas funcionalidades (compatibles)
- PATCH: Correcciones de errores (compatibles)

### Control de Versiones
- Usar mensajes de commit significativos
- Etiquetar todos los releases
- Mantener el changelog actualizado

### Proceso de Release
1. Actualizar número de versión
2. Actualizar changelog
3. Crear rama de release
4. Ejecutar pruebas
5. Etiquetar release
6. Desplegar