# SentinelSight

SentinelSight is an MVP AI Video Analytics Platform designed to ingest RTSP streams, detect objects (people), and enforce rules (intrusion) to generate alerts.

## Features
- **Video Ingestion**: Supports RTSP streams with auto-reconnect.
- **AI Inference**: Uses YOLOv8 for object detection.
- **Rule Engine**: Intrusion detection in defined zones.
- **Event Management**: SQLite database for event persistence.
- **Dashboard**: Real-time camera status and event feed.

## Setup Instructions

### Prerequisites
- Docker and Docker Compose
- Or: Python 3.10+ and Node.js 18+

### Running with Docker (Recommended)
1. Clone the repository.
2. Run `docker-compose up --build`.
3. Access the Dashboard at `http://localhost:3000`.
4. Access the API Docs at `http://localhost:8000/docs`.

### Running Locally
**Backend:**
1. `cd backend`
2. `pip install -r requirements.txt`
3. `python -m uvicorn app.main:app --reload`

**Frontend:**
1. `cd frontend`
2. `npm install`
3. `npm run dev`

## Usage
1. Open the dashboard.
2. Add a camera using the "Add Camera" form.
   - For testing without a real camera, you can use a local video file path if running locally (e.g., `/path/to/video.mp4`) or a public RTSP stream.
3. The system will automatically start processing frames.
4. Events (Intrusion) will appear in the Event Feed.

## Architecture
- **Backend**: FastAPI (Python)
- **Database**: SQLite (SQLModel)
- **AI**: YOLOv8 (Ultralytics) + OpenCV
- **Frontend**: React + Vite + TailwindCSS

## Known Limitations
- The "Live Preview" in the dashboard is currently a placeholder.
- Zone configuration is hardcoded to the full frame for the MVP entry.
- Snapshot images are stored locally and served via static file serving (needs configuration in production).
