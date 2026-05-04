"""CLI entry point for vault-pass."""

import sys
import argparse

from vault_pass.core import (
    BW_BIN,
    enforce_os_compatibility,
    get_session_file,
    load_session,
    unlock_vault,
    save_session,
    get_password,
    sync_vault,
)


def main():
    """Main CLI entry point."""
    enforce_os_compatibility()

    parser = argparse.ArgumentParser(
        description="Fetch a password from Bitwarden using the CLI.",
        prog="vault-pass"
    )
    parser.add_argument(
        "vault_entry_id",
        help="The Bitwarden Vault Entry ID (e.g., d98f7g19-h5m1-q9w8-x32c-i3o2p1cg7u41)"
    )
    args = parser.parse_args()

    session_file = get_session_file()

    # Get or create session
    bw_session = load_session(session_file)
    if not bw_session:
        bw_session = unlock_vault(BW_BIN)
        save_session(session_file, bw_session)

    # Fetch password, retry with sync if needed
    success, result = get_password(BW_BIN, bw_session, args.vault_entry_id)
    if success:
        print(result, end="")
        return

    stderr_output = result
    print(f"Failed to retrieve password.\n{stderr_output}", file=sys.stderr)

    if "not found" in stderr_output.lower():
        print("Attempting sync and retry...", file=sys.stderr)
        if sync_vault(BW_BIN, bw_session):
            print("Sync completed, retrying password retrieval...", file=sys.stderr)
            success, result = get_password(BW_BIN, bw_session, args.vault_entry_id)
            if success:
                print(result, end="")
                return
        print("Failed to retrieve password after sync.", file=sys.stderr)

    sys.exit(1)


if __name__ == "__main__":
    main()
