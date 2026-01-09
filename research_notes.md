# Research & Best Practices Notes

## 1. Studied Platforms

I analyzed the following global platforms to inform the design of SentinelSight:

### Milestone Systems (XProtect)
*   **Focus**: VMS (Video Management Software), open platform, scalability.
*   **Key Feature**: Centralized management server with recording servers.
*   **Adoption**: Adopted the concept of a "Camera" entity with status management and a centralized configuration database. The separation of ingestion/recording (Management) from viewing (Smart Client) inspired the API vs. UI split.

### BriefCam
*   **Focus**: Video Analytics, "Video Synopsis".
*   **Key Feature**: Review, Respond, Research modules.
*   **Adoption**: The "Event Feed" maps to the "Respond" (real-time alerts) capability. The data model allows for future "Review" (filtering past events) and "Research" (counting objects). The concept of "Zones" for defining rules was directly adopted.

### Frigate NVR
*   **Focus**: Local-first, AI-powered NVR for Home Assistant.
*   **Key Feature**: Efficient object detection, MQTT integration, extensive configuration via YAML.
*   **Adoption**: The "local-first" approach using SQLite and local file storage for snapshots. The idea of processing specific zones to reduce false positives is a core part of the design.

## 2. Features Adopted & Design Decisions

*   **Modular Monolith**: Chosen for the 2-day constraint. It allows for separation of concerns (Ingestion, Inference, API) without the complexity of managing multiple microservices.
*   **YOLOv8**: Selected for its balance of speed and accuracy (SOTA). It's easy to deploy and works well on CPU for MVP loads.
*   **SQLModel / FastAPI**: Python is the standard for AI/ML. FastAPI provides high performance and automatic documentation (OpenAPI), which is crucial for developer experience.
*   **React + Tailwind**: Provides a modern, responsive UI component library that is quick to iterate on.

## 3. Future Roadmap

If given 2 more weeks, I would prioritize:

1.  **Live Streaming**: Implement WebRTC or HLS/MSE to view the live camera feed in the browser. Currently, it's a placeholder.
2.  **Zone Editor**: A graphical editor in the frontend to draw polygons on a reference frame, rather than hardcoding JSON coordinates.
3.  **Queue-Based Processing**: Move inference to a Celery/Redis queue to handle high-throughput streams independently of the main application loop.
4.  **User Authentication**: Add JWT-based auth to secure the API and Dashboard.
5.  **Search & Filtering**: Advanced filtering for events (by time range, confidence score, object class).
6.  **Container Optimization**: Use GPU-accelerated Docker images for inference (CUDA/TensorRT) for production scale.
