# Vault Pass

A CLI tool to fetch passwords from Bitwarden vault.

## Installation

```bash
pip install vault-pass
```

## Usage

```bash
vault-pass <vault_entry_id>
```

### Example

```bash
vault-pass d98f7g19-h5m1-q9w8-x32c-i3o2p1cg7u41
```

## Requirements

- Python 3.8+
- Bitwarden CLI (`bw`) installed and available in PATH
- Linux or macOS (Windows not supported, use WSL on Windows)

## Features

- Secure session storage in RAM (`/dev/shm` on Linux, `/tmp` on macOS)
- Automatic vault sync retry when entry not found locally
- Secure file permissions (0600) for session files
- Helpful error messages for common issues

## Development

```bash
# Install in editable mode
pip install -e .

# Run tests
pytest
```

## License

MIT
