"""Vault Pass - A Bitwarden password retrieval CLI tool."""

__version__ = "1.0.0"

from vault_pass.core import (
    enforce_os_compatibility,
    get_session_file,
    load_session,
    unlock_vault,
    save_session,
    get_password,
    sync_vault,
)

__all__ = [
    "__version__",
    "enforce_os_compatibility",
    "get_session_file",
    "load_session",
    "unlock_vault",
    "save_session",
    "get_password",
    "sync_vault",
]
