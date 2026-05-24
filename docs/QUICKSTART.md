# Flow CLI Quick Start Guide

Get started with Flow CLI in 5 minutes.

## Prerequisites

- Python 3.10 or higher
- Google account with Flow access
- Flow subscription (Free/Pro/Ultra)

## Installation

### Option 1: Using pipx (Recommended)

```bash
pipx install flow-cli
```

### Option 2: Using pip

```bash
pip install flow-cli
```

### Option 3: From source

```bash
git clone https://github.com/yourusername/flow-cli.git
cd flow-cli
pip install -e .
```

## First-Time Setup

### 1. Install Playwright Browsers

Flow CLI uses Playwright for authentication:

```bash
playwright install chromium
```

### 2. Authenticate

```bash
flow login
```

This will:
1. Open a Chrome browser
2. Navigate to Flow
3. Wait for you to log in
4. Save your authentication cookies
5. Close the browser automatically

Your credentials are saved to `~/.flow-cli/profiles.json`.

## Basic Usage

### Generate an Image

```bash
flow generate image "a serene mountain landscape at sunset"
```

The CLI will:
1. Submit the generation job
2. Wait for it to complete
3. Display the result with asset ID and URL

### Generate a Video

```bash
flow generate video "a drone shot flying over a futuristic city"
```

### List Your Assets

```bash
flow list
```

### Download an Asset

```bash
flow download <asset-id> --output my-video.mp4
```

## Advanced Examples

### Image with Custom Settings

```bash
flow generate image "a portrait photo" \
  --ratio 16:9 \
  --style photorealistic \
  --negative "blurry, distorted"
```

### Video with Camera Movement

```bash
flow generate video "nature scene" \
  --duration 8 \
  --camera zoom_in \
  --ratio 16:9
```

### Image-to-Video

```bash
flow generate video "camera pans left slowly" \
  --from-image path/to/image.jpg \
  --duration 5
```

### Async Generation (No Wait)

```bash
# Submit job without waiting
flow generate video "city at night" --no-wait

# Check status later
flow status <job-id>

# Download when complete
flow download <asset-id>
```

### JSON Output (for scripting)

```bash
flow generate image "abstract art" --output json | jq '.asset_id'
```

## Using with Claude (MCP)

### 1. Install MCP Support

```bash
pip install 'flow-cli[mcp]'
```

### 2. Configure Claude Desktop

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "flow": {
      "command": "python",
      "args": ["-m", "flow_cli.mcp_server"]
    }
  }
}
```

### 3. Use in Claude

```
Generate a video of "a sunset over the ocean" using Flow
```

Claude will automatically:
1. Call the Flow MCP server
2. Generate the video
3. Show you the result

## Multiple Accounts

### Add Additional Profiles

```bash
flow login --profile work@example.com
flow login --profile personal@gmail.com
```

### List Profiles

```bash
flow profiles
```

### Switch Default Profile

```bash
flow config set-default work@example.com
```

## Troubleshooting

### "No authenticated profile found"

Run `flow login` to authenticate.

### "Session expired"

Flow cookies expire periodically. Re-authenticate:

```bash
flow logout
flow login
```

### Browser doesn't open

Try running with visible browser:

```bash
flow login --no-headless
```

### API endpoints not working

Flow CLI uses reverse-engineered endpoints that may change. Check for updates:

```bash
pip install --upgrade flow-cli
```

Or help improve the tool by capturing API requests (see API_RESEARCH.md).

## Next Steps

- Read [API_RESEARCH.md](API_RESEARCH.md) to help document Flow's API
- Check out [EXAMPLES.md](EXAMPLES.md) for more usage patterns
- Contribute to the project on GitHub

## Getting Help

- Check the [README](../README.md)
- Open an issue on GitHub
- Read the [Flow Help Center](https://support.google.com/flow/)
