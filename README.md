# Vault Pass

Vault Pass is a streamlined utility built to eliminate the constant friction of master password prompts when using the Bitwarden CLI. It allows you to unlock your vault once and securely reuse that session across multiple terminal windows or Ansible runs until your next reboot.

## Installation in Ansible Projects

To use vault-pass in your project, simply add it to your pip requirements file. 
Add one of the following lines: 

### Using HTTPS:
```
git+https://github.com/marwyg/vault-pass.git@main
```

### Using SSH:
```
git+ssh://git@github.com/marwyg/vault-pass.git@main
```

Then, install the requirements as usual:
```Bash
pip install -r requirements.txt
```

## Forking
Note: Instead of using my main branch, consider forking this project and add your repository to your requirements file. This protects your workflow from upstream changes and ensures you have full control over the version used by your team.

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
- Linux or macOS

## Features

- One-Time Unlock: Securely caches the session key to prevent repetitive master password requests
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
