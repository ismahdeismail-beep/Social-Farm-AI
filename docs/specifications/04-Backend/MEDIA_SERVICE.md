# MEDIA SERVICE

## Purpose
Orchestrates asynchronous multimedia generation and processing.

## Orchestration Flow
```mermaid
graph LR
    Req[Media Request] --> Proc[Processor]
    Proc --> Render[Rendering Engine]
    Render --> Store[S3 Storage]
    Store --> Notify[Notification]
```
- Images, Videos, Voice, Subtitles.
- Utilizes FFmpeg for heavy lifting.
