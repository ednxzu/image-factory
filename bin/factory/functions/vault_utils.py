import os
import hvac
from tabulate import tabulate
from datetime import timedelta


def format_ttl(seconds):
    delta = timedelta(seconds=seconds)
    days, hours, minutes = delta.days, delta.seconds // 3600, (delta.seconds // 60) % 60
    seconds = delta.seconds % 60

    if days > 0:
        return f"{days} days, {hours} hours, {minutes} minutes"
    else:
        return f"{hours} hours, {minutes} minutes, {seconds} seconds"


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
        accessor_id = token_info.get("accessor")
        ttl = format_ttl(token_info.get("ttl"))

        table_data = [
            ["Token Accessor ID", "Token", "Token Expiration"],
            [accessor_id, client.token, ttl],
        ]
        table = tabulate(table_data, headers="firstrow", tablefmt="fancy_grid")
        print(table)

        return "pass"
    except Exception as e:
        print(f"Error logging in to Vault: {e}")
        return "fail"
