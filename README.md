# News Collection Feishu

A minimal Python command-line application template using Typer and Rich.

## Features

- Basic CLI structure with Typer
- Rich console output
- Python project configuration (pyproject.toml)
- Test setup with pytest

## Installation

```bash
# Create virtual environment
python3 -m venv myenv
python3.12 -m venv myenv
source myenv/bin/activate  # macOS/Linux
# .\myenv\Scripts\Activate.ps1  # Windows

# Install dependencies
pip install -e .
```

## Usage

```bash
cli hello [name]
cli fetch-news
```

## Development

Run tests:
```bash
pytest
```

## Project Structure

```
src/
  news_collection_feishu/
    __init__.py    # Package initialization
    cli.py         # CLI commands
    main.py        # App entry point
tests/             # Test cases
pyproject.toml     # Project configuration
```

## License

MIT
