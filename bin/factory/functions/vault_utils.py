import os
import hvac
from tabulate import tabulate
from datetime import timedelta
from factory.utils import logo_mapping


def format_ttl(seconds):
    delta = timedelta(seconds=seconds)
    days, hours, minutes = delta.days, delta.seconds // 3600, (delta.seconds // 60) % 60
    seconds = delta.seconds % 60

    if days > 0:
        return f"{days} days, {hours} hours, {minutes} minutes"
    else:
        return f"{hours} hours, {minutes} minutes, {seconds} seconds"


def check_token_status(vault_addr: str, vault_token_accessor_id: str):
    if any(arg is None for arg in (vault_addr, vault_token_accessor_id)):
        raise ValueError("Vault configuration is incomplete. Make sure vault_addr, vault_token_accessor_id are set.")

    client = hvac.Client(url=vault_addr)

    try:
        token_info = client.lookup_token(accessor=vault_token_accessor_id)['data']

        if token_info.get("renewable") and not token_info.get("orphan"):
            print("Token is valid and not revoked.")
        else:
            print("Token is either revoked or expired.")
    except Exception as e:
        print(f"Error checking token status: {e}")


def vault_login_approle(vault_addr, vault_approle_id, vault_approle_secret_id):
    if any(
        arg is None for arg in (vault_addr, vault_approle_id, vault_approle_secret_id)
    ):
        raise ValueError(
            "Vault configuration is incomplete. Make sure vault_addr, vault_approle_id, and vault_approle_secret_id are set."
        )

    client = hvac.Client(url=vault_addr)

    try:
        response = client.auth.approle.login(
            role_id=vault_approle_id, secret_id=vault_approle_secret_id
        )
        client.token = response["auth"]["client_token"]

        os.environ["VAULT_TOKEN"] = f"{client.token}"

        token_info = client.lookup_token()["data"]
        token_accessor_id = token_info.get("accessor")
        token_ttl = format_ttl(token_info.get("ttl"))

        table_data = [
            ["Token Accessor ID", "Token", "Token Expiration"],
            [token_accessor_id, client.token, token_ttl],
        ]
        table = tabulate(table_data, headers="firstrow", tablefmt="fancy_grid")
        print(table)
        return token_accessor_id
    except Exception as e:
        print(f"Error logging in to Vault: {e}")


def vault_logout_approle(vault_addr: str, vault_token_accessor_id: str):
    if any(arg is None for arg in (vault_addr, vault_token_accessor_id)):
        raise ValueError(
            "Vault configuration is incomplete. Make sure vault_addr, vault_token_accessor_id are set."
        )

    client = hvac.Client(url=vault_addr)

    try:
        client.revoke_token(accessor=vault_token_accessor_id)

        print(f"Successfully revoked token with accessor ID: {vault_token_accessor_id}")
        return "pass"
    except Exception as e:
        print(f"Error revoking token: {e}")
