# Code Style and Documentation Guidelines

## TypeScript/JavaScript Code Style

### File Organization

```typescript
// 1. Imports
import React from 'react';
import { useTranslation } from 'react-i18next';

// 2. Types/Interfaces
interface Props {
  name: string;
  age?: number;
}

// 3. Component/Function
export const MyComponent: React.FC<Props> = ({ name, age }) => {
  // Implementation
};
```

### Type Annotations

```typescript
// Use explicit type annotations for public APIs
export function calculateAge(birthDate: Date): number {
  // Implementation
}

// Let TypeScript infer types for internal variables
const today = new Date();
```

### Comments and Documentation

```typescript
/**
 * Generates a CV in the specified format.
 * 
 * @param data - The CV data to generate
 * @param format - Output format (pdf, html, markdown)
 * @returns Promise resolving to the generated CV
 * @throws {ValidationError} If the CV data is invalid
 */
async function generateCV(
  data: CVData,
  format: OutputFormat
): Promise<GeneratedCV> {
  // Implementation
}

// Use inline comments sparingly, only for complex logic
function complexCalculation() {
  // First, normalize the input values
  const normalized = normalizeValues();
  
  // Then apply the transformation matrix
  const transformed = applyMatrix(normalized);
}
```

## Python Code Style

### File Organization

```python
"""Module docstring explaining the purpose of the module."""

# 1. Standard library imports
import os
from typing import Dict, List

# 2. Third party imports
from fastapi import FastAPI
import pydantic

# 3. Local imports
from .models import CV
from .utils import generate_pdf

# 4. Constants
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

# 5. Classes/Functions
class CVGenerator:
    """Class docstring explaining the purpose of the class."""
```

### Type Hints

```python
from typing import Optional, List, Dict

def process_cv(
    data: Dict[str, any],
    format: str = "pdf",
    include_photo: bool = True
) -> Optional[bytes]:
    """
    Process and generate CV in the specified format.
    
    Args:
        data: Dictionary containing CV data
        format: Output format (pdf, html, markdown)
        include_photo: Whether to include photo in output
        
    Returns:
        Bytes of generated CV or None if generation fails
        
    Raises:
        ValueError: If format is not supported
    """
    # Implementation
```

### Docstrings

```python
class CVTemplate:
    """
    Handles CV template rendering and customization.
    
    Attributes:
        name: Template name
        style: CSS styling for the template
        
    Example:
        >>> template = CVTemplate("modern")
        >>> html = template.render(cv_data)
    """
    
    def render(self, data: Dict[str, any]) -> str:
        """
        Render CV data using the template.
        
        Args:
            data: Dictionary containing CV data
            
        Returns:
            Rendered HTML string
            
        Raises:
            TemplateError: If rendering fails
        """
        # Implementation
```

## General Guidelines

### Naming Conventions

```typescript
// TypeScript/JavaScript
const MAX_FILE_SIZE = 5 * 1024 * 1024;  // Constants in UPPER_SNAKE_CASE
const userData = {};  // Variables in camelCase
function calculateTotal() {}  // Functions in camelCase
class UserProfile {}  // Classes in PascalCase
interface UserData {}  // Interfaces in PascalCase
```

```python
# Python
MAX_FILE_SIZE = 5 * 1024 * 1024  # Constants in UPPER_SNAKE_CASE
user_data = {}  # Variables in snake_case
def calculate_total():  # Functions in snake_case
    pass
class UserProfile:  # Classes in PascalCase
    pass
```

### Error Handling

```typescript
// TypeScript
try {
  await generateCV(data);
} catch (error) {
  if (error instanceof ValidationError) {
    logger.warn('Validation failed:', error);
    throw new UserFacingError('Invalid CV data');
  }
  logger.error('Unexpected error:', error);
  throw new UserFacingError('Internal error');
}
```

```python
# Python
try:
    generate_cv(data)
except ValidationError as e:
    logger.warning(f"Validation failed: {e}")
    raise UserFacingError("Invalid CV data")
except Exception as e:
    logger.error(f"Unexpected error: {e}")
    raise UserFacingError("Internal error")
```

### Code Organization

1. **Logical Grouping**
   - Group related functionality together
   - Keep files focused and single-purpose
   - Use meaningful directory structure

2. **Dependency Management**
   - Minimize external dependencies
   - Keep dependencies up-to-date
   - Document required versions

3. **Testing**
   - Write tests alongside code
   - Include both unit and integration tests
   - Document test requirements and setup

### Best Practices

1. **Code Quality**
   - Follow DRY (Don't Repeat Yourself) principle
   - Write self-documenting code
   - Use meaningful variable names

2. **Performance**
   - Optimize critical paths
   - Use appropriate data structures
   - Document performance considerations

3. **Security**
   - Validate all inputs
   - Sanitize outputs
   - Handle sensitive data appropriately

## Code Review Process

### Pull Request Guidelines
- Create a PR for all changes
- Provide clear description of changes
- Link related issues
- Include test coverage
- Update documentation

### Review Checklist
1. Code Quality
   - Follows style guide
   - No code smells
   - Proper error handling
   
2. Testing
   - Unit tests added/updated
   - Integration tests if needed
   - All tests passing
   
3. Documentation
   - Code comments where needed
   - API documentation updated
   - README updated if needed

4. Security
   - No sensitive data exposed
   - Input validation
   - Proper error handling

### Review Process
1. Submit PR
2. Automated checks run
3. At least one approval required
4. Address feedback
5. Merge when approved

## Versioning

We follow Semantic Versioning (MAJOR.MINOR.PATCH):

### Version Numbers
- MAJOR: Breaking changes
- MINOR: New features (backwards compatible)
- PATCH: Bug fixes (backwards compatible)

### Version Control
- Use meaningful commit messages
- Tag all releases
- Keep changelog updated

### Release Process
1. Update version number
2. Update changelog
3. Create release branch
4. Run tests
5. Tag release
6. Deploy