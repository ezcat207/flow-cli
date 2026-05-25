# How to Capture Flow API Endpoints

Since Flow doesn't have a public API, we need to reverse engineer the endpoints from the web interface. Here's a step-by-step guide.

## Method 1: Using Browser DevTools (Easiest)

### Step 1: Open Flow in Chrome

1. Open Chrome browser
2. Navigate to: https://labs.google/fx/tools/flow
3. Log in with your Google account

### Step 2: Open DevTools

1. Press `F12` (or `Cmd+Option+I` on Mac)
2. Click on the **Network** tab
3. Click the filter icon and select **Fetch/XHR** to show only API requests

### Step 3: Perform Actions

Try these actions while watching the Network tab:

**Generate an Image:**
1. Click "Create" or "Generate"
2. Enter a prompt like "a beautiful sunset"
3. Click generate
4. Watch for API requests in the Network tab

**Generate a Video:**
1. Try video generation
2. Monitor the network requests

**List Assets:**
1. View your assets/gallery
2. Check what API is called

### Step 4: Inspect API Requests

For each interesting request:

1. Click on the request in the Network tab
2. Note the **Request URL** (e.g., `https://labs.google.com/api/flow/v1/images/generate`)
3. Click on **Headers** tab:
   - Note the **Request Method** (GET, POST, etc.)
   - Copy **Request Headers** (especially cookies)
4. Click on **Payload** tab:
   - Copy the request body/parameters
5. Click on **Response** tab:
   - Copy the response format

### Step 5: Document Your Findings

Update `docs/API_RESEARCH.md` with:

```markdown
### Image Generation

**Endpoint:** `POST https://labs.google.com/api/flow/v1/images/generate`

**Request Headers:**
- Cookie: [your session cookies]
- Content-Type: application/json

**Request Body:**
\`\`\`json
{
  "prompt": "a beautiful sunset",
  "aspectRatio": "16:9"
}
\`\`\`

**Response:**
\`\`\`json
{
  "jobId": "abc123",
  "status": "pending"
}
\`\`\`
```

### Step 6: Update the Code

Update `src/flow_cli/client.py`:

```python
async def generate_image(self, request: ImageGenerationRequest) -> Job:
    # Change this URL to the real endpoint you discovered
    url = f"{self.base_url}/images/generate"  # Update this!

    # Update payload format based on what you captured
    payload = {
        "prompt": request.prompt,
        "aspectRatio": request.aspect_ratio.value,
    }

    response = await self.client.post(url, json=payload)
    data = response.json()

    # Update parsing based on real response format
    return Job(
        id=data["jobId"],  # Use actual field name
        type=AssetType.IMAGE,
        status=JobStatus(data["status"]),
        # ... etc
    )
```

## Method 2: Using the Capture Tool

### Run the Capture Script

```bash
cd flow-cli
source .venv/bin/activate
python -m flow_cli.capture
```

This will:
1. Open a browser
2. Navigate to Flow
3. Record all network requests
4. Save to `~/.flow-cli/captures/capture_TIMESTAMP.json`

### Analyze Captured Data

```bash
# View captured requests
cat ~/.flow-cli/captures/capture_*.json | jq '.'

# Find image generation endpoints
cat ~/.flow-cli/captures/capture_*.json | jq '.[] | select(.request.url | contains("image"))'

# Find video generation endpoints
cat ~/.flow-cli/captures/capture_*.json | jq '.[] | select(.request.url | contains("video"))'
```

## Method 3: Using Proxy (Advanced)

### Setup mitmproxy

```bash
# Install mitmproxy
brew install mitmproxy

# Run mitmproxy
mitmproxy
```

### Configure Browser

1. Set browser proxy to `localhost:8080`
2. Install mitmproxy certificate
3. Visit Flow and perform actions
4. All requests will be captured in mitmproxy

### Export Requests

In mitmproxy:
1. Press `w` to save flows
2. Save as `flow_requests.mitm`
3. Export to JSON:
   ```bash
   mitmdump -r flow_requests.mitm -w flow_requests.json
   ```

## Method 4: Using the Simple Capture Script

I've created a simple script at `capture_flow_api.py`:

```bash
cd flow-cli
source .venv/bin/activate
python capture_flow_api.py
```

This will:
1. Open Chrome
2. Navigate to Flow
3. Give you 60 seconds to interact
4. Save captured requests to `flow_api_captured.json`

## What to Look For

### Image Generation

Look for requests containing:
- `/image`
- `/generate`
- `POST` method
- Request body with `prompt` field

### Video Generation

Look for requests containing:
- `/video`
- `/generate`
- `veo` (model name)
- Request body with `prompt`, `duration`

### Job Status

Look for:
- `/job`
- `/status`
- `GET` method with job ID in URL

### Asset Management

Look for:
- `/assets` or `/gallery`
- `/download`
- `/delete`

## Common API Patterns

Flow likely uses patterns similar to other Google services:

### Base URL
```
https://labs.google.com/api/flow/v1
```

### Authentication
Cookie-based with these common cookies:
- `SID`, `HSID`, `SSID`
- `APISID`, `SAPISID`
- Custom Flow session cookies

### Request Format
```json
{
  "requests": [{
    "action": "generate",
    "model": "imagen4",
    "params": {
      "prompt": "..."
    }
  }]
}
```

### Response Format
```json
{
  "responses": [{
    "jobId": "...",
    "status": "pending"
  }]
}
```

## Tips

1. **Clear Network Tab**: Clear it before each action to see only relevant requests
2. **Disable Cache**: Check "Disable cache" in DevTools to ensure fresh requests
3. **Preserve Log**: Check "Preserve log" to keep requests across page navigations
4. **Copy as cURL**: Right-click request → Copy → Copy as cURL to see full request
5. **Search/Filter**: Use the search box to filter requests by keyword

## Next Steps

Once you've captured the endpoints:

1. Update `docs/API_RESEARCH.md` with your findings
2. Update `src/flow_cli/client.py` with real endpoints
3. Test with: `flow generate image "test"`
4. Share your findings via Pull Request!

## Contributing

If you successfully capture Flow's API endpoints, please contribute:

1. Fork the repo
2. Update API_RESEARCH.md with your findings
3. Update client.py with working endpoints
4. Test thoroughly
5. Submit a Pull Request

Your contribution will help everyone use Flow CLI!
