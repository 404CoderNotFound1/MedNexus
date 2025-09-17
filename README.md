# Fullstack React + FastAPI Application

This is a minimal fullstack application with a React TypeScript frontend and FastAPI backend.

## Project Structure

```
my-fullstack-app/
├── backend/               # FastAPI backend
│   ├── app.py            # Main FastAPI application
│   └── requirements.txt  # Python dependencies
└── frontend/             # React TypeScript frontend
    ├── src/              # Source files
    ├── public/           # Static files
    ├── package.json      # Frontend dependencies
    └── vite.config.ts    # Vite configuration
```

## Getting Started

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create and activate a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Start the FastAPI server:
   ```bash
   uvicorn app:app --reload
   ```
   The backend will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```
   The frontend will be available at `http://localhost:5173`

## Features

- **Backend (FastAPI)**
  - RESTful API endpoints
  - CORS middleware enabled
  - Sample CRUD operations for items

- **Frontend (React + TypeScript + Vite)**
  - Modern React with TypeScript
  - Responsive design with CSS Grid and Flexbox
  - Axios for API requests
  - Clean and maintainable component structure

## Available Scripts

In the frontend directory, you can run:

- `npm run dev` - Start the development server
- `npm run build` - Build for production
- `npm run preview` - Preview the production build

## API Endpoints

- `GET /` - Welcome message
- `GET /items` - Get all items
- `GET /items/{item_id}` - Get a specific item

## License

This project is open source and available under the [MIT License](LICENSE).
