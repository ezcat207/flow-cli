# Flow CLI Development Setup

Guide for setting up Flow CLI for development.

## Prerequisites

- Python 3.10+
- pip, pipx, or uv
- Git
- Chrome/Chromium browser

## Clone Repository

```bash
git clone https://github.com/yourusername/flow-cli.git
cd flow-cli
```

## Development Installation

### Option 1: Using uv (Recommended)

```bash
# Install uv if not already installed
pip install uv

# Create virtual environment
uv venv

# Activate virtual environment
source .venv/bin/activate  # macOS/Linux
# or
.venv\Scripts\activate  # Windows

# Install in editable mode with dev dependencies
uv pip install -e ".[dev,mcp]"

# Install Playwright browsers
playwright install chromium
```

### Option 2: Using pip

```bash
# Create virtual environment
python -m venv .venv

# Activate
source .venv/bin/activate

# Install
pip install -e ".[dev,mcp]"

# Install Playwright
playwright install chromium
```

## Project Structure

```
flow-cli/
├── src/flow_cli/          # Main package
│   ├── __init__.py
│   ├── auth.py           # Authentication (browser cookies)
│   ├── client.py         # API client
│   ├── cli.py            # CLI commands
│   ├── config.py         # Configuration management
│   ├── models.py         # Data models
│   ├── capture.py        # API capture tool
│   └── mcp_server.py     # MCP server integration
├── tests/                 # Tests
├── docs/                  # Documentation
├── pyproject.toml        # Project configuration
├── README.md
└── LICENSE
```

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=flow_cli --cov-report=html

# Run specific test file
pytest tests/test_models.py

# Run with verbose output
pytest -v
```

## Code Quality

### Formatting with Black

```bash
# Format all code
black src/ tests/

# Check formatting
black --check src/ tests/
```

### Linting with Ruff

```bash
# Lint all code
ruff check src/ tests/

# Auto-fix issues
ruff check --fix src/ tests/
```

### Type Checking with MyPy

```bash
# Type check
mypy src/flow_cli/
```

### Run All Checks

```bash
# Format
black src/ tests/

# Lint
ruff check --fix src/ tests/

# Type check
mypy src/flow_cli/

# Test
pytest
```

## Development Workflow

### 1. Reverse Engineering API Endpoints

The most important development task is documenting Flow's API:

```bash
# Run the capture tool
python -m flow_cli.capture
```

This will:
1. Open browser to Flow
2. Record all API requests
3. Save to `~/.flow-cli/captures/`

Then:
1. Analyze captured requests
2. Update `docs/API_RESEARCH.md`
3. Update `src/flow_cli/client.py` with real endpoints

### 2. Testing Changes

```bash
# Test CLI locally
flow --help
flow login
flow generate image "test"

# Test MCP server
python -m flow_cli.mcp_server
```

### 3. Making Changes

1. Create a feature branch:
   ```bash
   git checkout -b feature/my-feature
   ```

2. Make your changes

3. Run tests and checks:
   ```bash
   pytest
   black src/ tests/
   ruff check src/ tests/
   mypy src/flow_cli/
   ```

4. Commit:
   ```bash
   git add .
   git commit -m "Add feature: description"
   ```

5. Push and create PR:
   ```bash
   git push origin feature/my-feature
   ```

## Building and Publishing

### Build Package

```bash
# Install build tools
pip install build twine

# Build distribution
python -m build

# Check distribution
twine check dist/*
```

### Publish to PyPI

```bash
# Test PyPI first
twine upload --repository testpypi dist/*

# Then real PyPI
twine upload dist/*
```

## Debugging

### Enable Debug Logging

```bash
# Set environment variable
export FLOW_CLI_DEBUG=1

# Run commands
flow generate image "test"
```

### Inspect HTTP Requests

```bash
# Use mitmproxy to intercept requests
mitmproxy

# Configure Flow CLI to use proxy
export HTTPS_PROXY=http://localhost:8080
flow generate image "test"
```

### Browser Debug Mode

```bash
# Run login with visible browser
flow login --no-headless

# Watch network traffic in DevTools
```

## MCP Server Development

### Test MCP Server Locally

```bash
# Run server
python -m flow_cli.mcp_server

# In another terminal, test with MCP client
# (Implementation depends on your MCP client)
```

### Configure in Claude Desktop

Edit `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "flow": {
      "command": "python",
      "args": [
        "-m",
        "flow_cli.mcp_server"
      ],
      "env": {
        "FLOW_CLI_DEBUG": "1"
      }
    }
  }
}
```

Restart Claude Desktop and test:

```
Generate a video of "a sunset" using Flow
```

## Contributing

### Contribution Areas

1. **API Documentation**: Most valuable contribution
   - Run capture tool
   - Document endpoints in API_RESEARCH.md
   - Update client.py

2. **Bug Fixes**: Fix issues from GitHub

3. **Features**: Add new functionality
   - Video editing
   - Batch processing
   - Better error handling

4. **Documentation**: Improve docs and examples

5. **Tests**: Add test coverage

### Pull Request Guidelines

- Write clear commit messages
- Add tests for new features
- Update documentation
- Run all checks before submitting
- Reference related issues

## Resources

- [Flow Official Site](https://labs.google/fx/tools/flow)
- [Flow Help Center](https://support.google.com/flow/)
- [NotebookLM CLI](https://github.com/jacob-bd/notebooklm-cli) - Similar approach
- [MCP Documentation](https://modelcontextprotocol.io/)
- [Typer Documentation](https://typer.tiangolo.com/)
- [Playwright Documentation](https://playwright.dev/python/)

## Getting Help

- Open an issue on GitHub
- Check existing issues and discussions
- Read the documentation
