# Flow API Research

This document tracks the reverse engineering process for Google Flow's internal API.

## Status

🔴 **In Progress** - Endpoints need to be discovered and documented.

## How to Capture API Endpoints

Since Flow doesn't have a public API, we need to reverse engineer the endpoints by analyzing network requests from the web interface.

### Method 1: Using the Capture Tool

Run the included capture tool to automatically record all API requests:

```bash
cd flow-cli
python -m flow_cli.capture
```

This will:
1. Open a browser to Flow
2. Record all network requests as you use the interface
3. Save requests to `~/.flow-cli/captures/capture_TIMESTAMP.json`
4. Show a summary of discovered endpoints

### Method 2: Manual Browser DevTools

1. Open Flow in Chrome: https://labs.google/fx/tools/flow
2. Open DevTools (F12) → Network tab
3. Filter by "Fetch/XHR"
4. Perform actions:
   - Generate an image
   - Generate a video
   - List your assets
   - Download an asset
5. Right-click on API requests → Copy as cURL
6. Document the endpoints below

## Discovered Endpoints

### Base URL

```
https://labs.google.com/api/flow/v1
```

*Note: This is a placeholder. Update after capturing actual requests.*

### Authentication

**Method:** Cookie-based authentication

**Required Cookies:**
- `SID`: Session ID
- `HSID`: Host Session ID
- `SSID`: Secure Session ID
- `APISID`: API Session ID
- `SAPISID`: Secure API Session ID
- *Others TBD...*

### Image Generation

**Endpoint:** `POST /images/generate` *(TBD)*

**Request:**
```json
{
  "prompt": "a serene mountain landscape at sunset",
  "aspectRatio": "16:9",
  "style": "photorealistic",
  "negativePrompt": "blurry, distorted",
  "seed": 12345
}
```

**Response:**
```json
{
  "jobId": "abc123def456",
  "status": "pending",
  "createdAt": "2026-05-15T10:30:00Z"
}
```

### Video Generation

**Endpoint:** `POST /videos/generate` *(TBD)*

**Request:**
```json
{
  "prompt": "a drone shot flying over a futuristic city",
  "duration": 5,
  "aspectRatio": "16:9",
  "cameraMovement": "zoom_in",
  "seed": 67890
}
```

**Response:**
```json
{
  "jobId": "xyz789abc123",
  "status": "pending",
  "createdAt": "2026-05-15T10:31:00Z"
}
```

### Job Status

**Endpoint:** `GET /jobs/{jobId}` *(TBD)*

**Response:**
```json
{
  "id": "abc123def456",
  "type": "image",
  "status": "completed",
  "progress": 100.0,
  "assetId": "asset_123456",
  "createdAt": "2026-05-15T10:30:00Z",
  "updatedAt": "2026-05-15T10:31:30Z"
}
```

**Status Values:**
- `pending`: Job queued
- `processing`: Generation in progress
- `completed`: Successfully completed
- `failed`: Generation failed

### List Assets

**Endpoint:** `GET /assets` *(TBD)*

**Query Parameters:**
- `type`: Filter by asset type (`image`, `video`)
- `limit`: Maximum results (default: 50)
- `offset`: Pagination offset

**Response:**
```json
{
  "assets": [
    {
      "id": "asset_123456",
      "type": "image",
      "prompt": "a serene mountain landscape at sunset",
      "url": "https://storage.googleapis.com/flow-assets/...",
      "thumbnailUrl": "https://storage.googleapis.com/flow-thumbnails/...",
      "status": "completed",
      "createdAt": "2026-05-15T10:30:00Z",
      "metadata": {
        "aspectRatio": "16:9",
        "width": 1920,
        "height": 1080
      }
    }
  ],
  "total": 42,
  "hasMore": true
}
```

### Get Asset

**Endpoint:** `GET /assets/{assetId}` *(TBD)*

**Response:**
```json
{
  "id": "asset_123456",
  "type": "video",
  "prompt": "a drone shot flying over a futuristic city",
  "url": "https://storage.googleapis.com/flow-assets/...",
  "thumbnailUrl": "https://storage.googleapis.com/flow-thumbnails/...",
  "status": "completed",
  "createdAt": "2026-05-15T10:31:00Z",
  "metadata": {
    "duration": 5,
    "aspectRatio": "16:9",
    "width": 1920,
    "height": 1080,
    "fps": 30
  }
}
```

### Delete Asset

**Endpoint:** `DELETE /assets/{assetId}` *(TBD)*

**Response:**
```json
{
  "success": true
}
```

### Upload Image (for image-to-video)

**Endpoint:** `POST /images/upload` *(TBD)*

**Request:** Multipart form data with image file

**Response:**
```json
{
  "url": "https://storage.googleapis.com/flow-temp/...",
  "id": "temp_image_123"
}
```

## Rate Limits

*TBD - Document any rate limiting headers or behaviors*

Potential headers to check:
- `X-RateLimit-Limit`
- `X-RateLimit-Remaining`
- `X-RateLimit-Reset`

## Credits/Quota

Flow uses a credit system:
- **Free**: 100 initial + 50 daily credits
- **Pro ($19.99/mo)**: 1,000 monthly credits
- **Ultra ($249.99/mo)**: 25,000 monthly credits

*TBD - How credits are tracked in API responses*

## Error Responses

Standard error format (assumed):

```json
{
  "error": {
    "code": "INVALID_REQUEST",
    "message": "Invalid aspect ratio",
    "details": {...}
  }
}
```

**Common Error Codes:**
- `UNAUTHORIZED`: Invalid or expired authentication
- `INVALID_REQUEST`: Malformed request
- `QUOTA_EXCEEDED`: Out of credits
- `RATE_LIMIT_EXCEEDED`: Too many requests
- `INTERNAL_ERROR`: Server error

## Implementation Checklist

- [ ] Capture actual API requests using browser DevTools
- [ ] Document real endpoint URLs
- [ ] Document real request/response formats
- [ ] Document authentication headers
- [ ] Update `client.py` with correct endpoints
- [ ] Update request models in `models.py`
- [ ] Test authentication flow
- [ ] Test image generation
- [ ] Test video generation
- [ ] Test job status polling
- [ ] Test asset management
- [ ] Handle errors gracefully
- [ ] Add retry logic for transient failures

## References

- [NotebookLM CLI](https://github.com/jacob-bd/notebooklm-cli) - Similar reverse engineering approach
- [Flow Official Site](https://labs.google/fx/tools/flow)
- [Flow Help Center](https://support.google.com/flow/)

## Notes

- Flow's API is undocumented and internal
- Endpoints may change without notice
- Cookie-based auth requires periodic re-authentication
- Some features may only be available via web interface
