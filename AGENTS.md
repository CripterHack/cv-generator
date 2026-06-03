# AGENTS.md

## Project Overview

Full-stack CV generator with three interfaces sharing common Python code:
- **Web frontend**: React 17 + TypeScript 4.9 + MUI 5 (CRA, in `web/frontend/`)
- **Web backend**: FastAPI + Redis (in `web/backend/`)
- **Desktop**: Tkinter GUI (in `desktop/`)
- **Shared Python**: CV generation logic (in `shared/`)

## Commands

### Frontend (`web/frontend/`)

```bash
npm start             # Dev server on :3000
npm run build         # Production build
npm test              # Tests (watch mode, CRA)
npm run test:ci       # Tests single-run (CI mode)
npm run test:coverage # Tests with coverage (single-run)
npm run type-check    # TypeScript type checking (tsc --noEmit)
npm run lint          # ESLint on src/**/*.{ts,tsx}
npm run lint:fix      # ESLint with auto-fix
npm run format        # Prettier write on src/**/*.{ts,tsx,css,scss}
```

### Backend (`web/backend/`)

```bash
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload   # Dev server
pytest web/backend/tests/                                           # Backend unit tests
```

### Root-level (from repo root)

```bash
pytest tests/ --cov=web/backend --cov=shared    # Integration tests with coverage
```

### Python Linting (from repo root)

```bash
black --check web/backend shared    # Check formatting
flake8 web/backend shared           # Lint
black web/backend shared            # Auto-format
```

### Docker

```bash
docker-compose -f docker-compose.dev.yml up   # All services (frontend, backend, redis, adminer)
docker-compose up                              # Production build (frontend, backend, redis)
```

## Architecture & Key Files

- **Backend entrypoint**: `web/backend/main.py` — FastAPI app, mounts `api/cv_endpoints.py` at `/api` prefix, connects to Redis
- **Frontend entrypoint**: `web/frontend/src/index.tsx`
- **CV generation logic**: `shared/services/cv_generator.py` — used by both desktop and web backend
- **Data model (backend)**: `web/backend/models/cv.py` (Pydantic v1) — required fields: `full_name`, `email` (EmailStr)
- **Data model (frontend)**: `web/frontend/src/types/cv.ts` (TypeScript) — mirrors backend model in camelCase; includes `toApiFormat()` transform utility to convert camelCase → snake_case for API calls
- **Export service**: `web/backend/services/export_service.py`, also `shared/utils/` for file handling
- **i18n**: `web/frontend/src/i18n/` (frontend), inline dictionaries in `desktop/cv-generator.py` (desktop)
- **Templates**: `shared/templates/` (Jinja2 HTML templates — used by desktop app with its own field names: `name`, `title`, `professional_experience`, etc.)
- **CV data format (desktop)**: JSON with fields: name, title, phone, age, city, summary, foto_encoded, professional_experience, academic_experience, skills, certificates

## Setup Requirements

- Python 3.11.5
- Node.js 18+
- Redis must be running for backend to function (Docker or standalone)
- `wkhtmltopdf` must be installed on the system for PDF export (pdfkit dependency)
- Copy `.env.example` to `.env` in both `web/frontend/` and `web/backend/` before running
- DevContainer setup is available and recommended (`.devcontainer/`) — auto-starts Redis only; run `./dev.sh` or start backend/frontend manually

## API Routes

All backend endpoints are mounted under `/api`:
- `POST /api/cv/` — Create CV
- `GET /api/cv/{email}` — Get CV by email
- `POST /api/cv/generate` — Generate CV from data
- `POST /api/cv/export?format=pdf|html|md` — Export CV
- `POST /api/cv/upload-photo` — Upload photo
- `GET /api/cv/templates` — List templates

## CI Pipeline (`.github/workflows/ci.yml`)

Runs on push/PR to `main`:
1. **backend-tests**: `pytest tests/ web/backend/tests/ --cov`, Redis service container
2. **frontend-tests**: `npm run test:ci` + `npm run type-check`
3. **lint**: `black --check --target-version py311` + `flake8` on `web/backend` and `shared`; `npx eslint` on frontend
4. **docker-build**: Docker builds for all three images (on push only)
5. **build-executables**: Multi-platform PyInstaller builds (on version tags only)
6. **release**: GitHub Release with Windows/Linux/macOS binaries (on version tags)

### Building Desktop Executables

```bash
python scripts/build.py          # Build for current platform
python scripts/build.py clean    # Clean build artifacts
```

PyInstaller spec file: `cv-generator.spec`
- Excludes web dependencies (FastAPI, Redis, etc.)
- Bundles shared templates and constants
- Windows: `dist/CVGenerator.exe` (~20MB)
- macOS: `dist/CVGenerator.app` (app bundle)
- Linux: `dist/CVGenerator` (single binary)

### Releasing

Tag a release to trigger multi-platform builds:
```bash
git tag v1.0.2
git push origin v1.0.2
```

This creates a GitHub Release with downloadable archives for all three platforms.

## Gotchas

- The Pydantic CV model (`web/backend/models/cv.py`) is the source of truth — the frontend mirrors it in camelCase via `web/frontend/src/types/cv.ts` and uses `toApiFormat()` to transform for API calls
- The desktop app uses a different field schema (`name`/`title`/`professional_experience`) — the shared Jinja2 template expects this format; the web backend's export_service uses the Pydantic model directly
- There are two separate Python requirements files: root `requirements.txt` (desktop/shared) and `web/backend/requirements.txt` (backend-specific)
- Backend `.env` defaults to `REDIS_HOST=localhost` — Docker Compose overrides this to `redis` (service name)
- `curriculum_data.json` is gitignored — the desktop app looks for it next to the script
- Frontend uses `react-scripts` (CRA) with `baseUrl: src` in tsconfig — imports resolve from `src/`
- All Python packages under `web/`, `shared/`, and `tests/` have `__init__.py` files for relative imports
- ESLint config extends `react-app`; `react/react-in-jsx-scope` is explicitly off
- Prettier: single quotes, semicolons, trailing commas (es5), 100 char print width
- Python formatting: `black`

## Test Locations

- `web/backend/tests/` — Backend API tests (FastAPI TestClient)
- `tests/integration/` — Root-level integration tests
- `tests/test_files/` — Test fixtures (e.g., test photos)
- `web/frontend/src/services/__tests__/` — Frontend service tests

## DevContainer Notes

- Only Redis auto-starts via `startup.sh` — backend and frontend are started manually
- `bin/dev` starts Redis + backend + frontend (uses `REPO_ROOT` auto-detection, no hardcoded paths)
- `.env` files are only created on first setup (not overwritten on rebuild)
- Healthcheck (`healthcheck.sh`) checks Redis as required, backend/frontend as optional
