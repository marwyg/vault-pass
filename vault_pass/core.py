"""Core functionality for vault-pass."""

import os
import sys
import getpass
import subprocess
import platform
from pathlib import Path

# Constants
BW_BIN = "bw"


def enforce_os_compatibility():
    """Fail fast if the user is running Windows."""
    if platform.system().lower() == "windows":
        print("Error: Windows is not supported. Please run this inside Linux, or macOS.", file=sys.stderr)
        sys.exit(1)


def get_session_file():
    """Return an OS-specific volatile path to the user's Bitwarden session file."""
    user = getpass.getuser()
    filename = f"bw_session_ansible_{user}"
    system = platform.system().lower()

    if system == "linux":
        # True RAM disk, wiped on power loss/reboot
        base_dir = Path("/dev/shm")
    elif system == "darwin":
        # macOS clears /tmp automatically on reboot
        base_dir = Path("/tmp")
    else:
        print(f"Error: Unsupported operating system '{platform.system()}'. Please use Linux or macOS.", file=sys.stderr)
        sys.exit(1)

    return base_dir / filename


def load_session(session_file):
    """Load session from file if it exists. Returns None if not found."""
    if session_file.is_file():
        print(f"Using stored Bitwarden Session: {session_file}", file=sys.stderr)
        return session_file.read_text().strip()
    return None


def unlock_vault(bw_bin):
    """Unlock Bitwarden vault and return the session key."""
    print("Vault locked. Requesting Bitwarden unlock...", file=sys.stderr)
    try:
        # Notice we do NOT capture stderr here. We let Bitwarden own it.
        result = subprocess.run(
            [bw_bin, "unlock", "--raw"],
            stdout=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        # We cannot read e.stderr here, but we know the command failed.
        # Bitwarden already printed its ugly error to the screen, so we just add context.
        print("Unlock failed. If you see a Decryption error above, you likely typed the wrong master password.", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print(f"Error: '{bw_bin}' command not found. Ensure Bitwarden CLI is installed.", file=sys.stderr)
        sys.exit(1)


def save_session(session_file, session_key):
    """Save session key to file with secure permissions."""
    if not session_key:
        print("Unlock failed: No session key returned.", file=sys.stderr)
        sys.exit(1)

    # Create the file securely with -rw------- permissions
    session_file.touch(mode=0o600, exist_ok=True)
    session_file.write_text(session_key)
    # Ensure permissions are correct even if file already existed
    session_file.chmod(0o600)
    print(f"Bitwarden Session stored: {session_file}", file=sys.stderr)


def get_password(bw_bin, session, entry_id):
    """Fetch password from Bitwarden. Returns (success, password_or_error)."""
    try:
        result = subprocess.run(
            [bw_bin, "get", "password", entry_id, "--session", session, "--raw"],
            capture_output=True,
            text=True,
            check=True
        )
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr


def sync_vault(bw_bin, session):
    """Sync Bitwarden vault. Returns True on success."""
    try:
        subprocess.run(
            [bw_bin, "sync", "--session", session],
            capture_output=True,
            text=True,
            check=True
        )
        return True
    except subprocess.CalledProcessError as e:
        stderr_msg = e.stderr if e.stderr else "unknown error"
        print(f"Sync failed: {stderr_msg}", file=sys.stderr)
        return False
