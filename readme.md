# Onion Decision Support System

A prototype decision support system (DSS) that combines a Django backend with a
React frontend to explore onion production scenarios. The goal is to provide a
foundation for integrating APSIM or AquaCrop crop growth models while giving
researchers and extension specialists an accessible web interface.

## Project structure

```text
backend/   # Django project exposing simulation and preset endpoints
frontend/  # React single-page application for interacting with the DSS
```

### Can't find these files on GitHub?

All of the scaffolding described here lives on the `work` branch. If you only
see the initial repository skeleton on GitHub, switch to that branch (or the
latest commit `87d3cea`) in the web UI or locally:

```bash
git fetch origin
git checkout work
```

Once the branch is checked out you should see the `backend/` and `frontend/`
directories together with the rest of the generated project files.

## Backend quick start

1. Create and activate a Python virtual environment.
2. Install dependencies:
   ```bash
   pip install -r backend/requirements.txt
   ```
3. Apply migrations and run the development server:
   ```bash
   python backend/manage.py migrate
   python backend/manage.py runserver
   ```

The backend exposes two endpoints under `/api/`:

- `POST /api/simulations/run` — runs the heuristic simulator with the provided
  management plan.
- `GET /api/simulations/presets` — returns sample scenarios that can be loaded
  from the UI.

## Frontend quick start

1. Install Node.js dependencies:
   ```bash
   cd frontend
   npm install
   ```
2. Start the Vite development server:
   ```bash
   npm run dev
   ```

The React app is configured to proxy API calls to `http://localhost:8000`, which
matches Django's default development server address.

## Next steps

- Replace the heuristic simulator with an APSIM or AquaCrop integration.
- Persist simulation runs for later comparison and download.
- Add authentication and role-based access control for collaborative use.
