# Contributing to Flow CLI

Thank you for your interest in contributing to Flow CLI!

## Most Valuable Contribution: API Documentation

Since Flow doesn't have a public API, the most valuable contribution you can make is **documenting the internal API endpoints**.

### How to Help

1. **Run the Capture Tool**:
   ```bash
   python -m flow_cli.capture
   ```

2. **Use Flow Normally**:
   - Generate images
   - Generate videos
   - List assets
   - Download files
   - Delete assets

3. **Review Captured Data**:
   - Open `~/.flow-cli/captures/capture_*.json`
   - Analyze request/response formats

4. **Document Your Findings**:
   - Update `docs/API_RESEARCH.md` with:
     - Endpoint URLs
     - Request formats
     - Response formats
     - Headers required
     - Error responses

5. **Update the Client**:
   - Update `src/flow_cli/client.py` with correct endpoints
   - Test the changes
   - Submit a PR

## Other Ways to Contribute

### Bug Reports

Found a bug? Please open an issue with:

- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Your environment (OS, Python version, Flow CLI version)
- Relevant logs/error messages

### Feature Requests

Have an idea? Open an issue with:

- Clear description of the feature
- Use cases
- How it would benefit users
- (Optional) Implementation suggestions

### Code Contributions

#### Setup

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/YOUR_USERNAME/flow-cli.git
   cd flow-cli
   ```
3. Set up development environment:
   ```bash
   uv venv
   source .venv/bin/activate
   uv pip install -e ".[dev,mcp]"
   playwright install chromium
   ```

#### Making Changes

1. Create a branch:
   ```bash
   git checkout -b feature/my-feature
   ```

2. Make your changes

3. Add tests:
   ```bash
   # Add tests in tests/
   pytest tests/
   ```

4. Run code quality checks:
   ```bash
   black src/ tests/
   ruff check --fix src/ tests/
   mypy src/flow_cli/
   ```

5. Update documentation if needed

6. Commit with clear message:
   ```bash
   git commit -m "Add feature: clear description"
   ```

7. Push and create PR:
   ```bash
   git push origin feature/my-feature
   ```

#### Pull Request Guidelines

- Write clear, descriptive commit messages
- Add tests for new features
- Update documentation
- Run all checks (tests, linting, type checking)
- Reference related issues
- Keep PRs focused (one feature/fix per PR)

### Documentation

Help improve documentation:

- Fix typos
- Clarify confusing sections
- Add examples
- Improve setup instructions
- Write tutorials

Update files in:
- `README.md`
- `docs/`
- Code docstrings
- CLI help text

### Examples

Share useful examples in `docs/EXAMPLES.md`:

- Creative workflows
- Integration scripts
- Automation setups
- Tips and tricks

## Code Style

We use:

- **Black** for formatting (line length: 100)
- **Ruff** for linting
- **MyPy** for type checking
- **Pytest** for testing

Run all checks:
```bash
make check  # or manually:
black src/ tests/
ruff check --fix src/ tests/
mypy src/flow_cli/
pytest
```

## Commit Message Format

Use clear, imperative messages:

```
Add image-to-video support

- Implement upload_image endpoint
- Add --from-image flag to CLI
- Update tests and docs
```

Good:
- "Add feature X"
- "Fix bug in Y"
- "Update documentation for Z"

Bad:
- "stuff"
- "fixes"
- "WIP"

## Testing

All code changes should include tests:

```bash
# Run tests
pytest

# Run specific test
pytest tests/test_client.py

# Run with coverage
pytest --cov=flow_cli --cov-report=html
```

Test files go in `tests/` and should:
- Test one thing clearly
- Use descriptive names
- Include docstrings
- Use fixtures for setup
- Mock external dependencies

## Development Process

1. **Check Issues**: Look for existing issues or create one
2. **Discuss**: Comment on the issue to discuss approach
3. **Implement**: Make your changes
4. **Test**: Add tests and ensure all pass
5. **Document**: Update docs
6. **Submit**: Create PR with clear description
7. **Review**: Address feedback
8. **Merge**: Maintainer will merge when ready

## Release Process

Maintainers handle releases:

1. Update version in `pyproject.toml` and `src/flow_cli/__init__.py`
2. Update `CHANGELOG.md`
3. Create git tag
4. Build and publish to PyPI
5. Create GitHub release

## Questions?

- Open an issue for questions
- Check existing documentation
- Look at similar projects (NotebookLM CLI)

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Recognition

Contributors will be:
- Listed in README.md
- Mentioned in release notes
- Appreciated! 🎉

Thank you for helping make Flow CLI better!
