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
        raise ValueError(
            "Vault configuration is incomplete. Make sure vault_addr, vault_token_accessor_id are set."
        )

    client = hvac.Client(url=vault_addr)

    try:
        client.lookup_token(accessor=vault_token_accessor_id)["data"]
        return "pass"
    except (hvac.exceptions.InvalidPath, hvac.exceptions.Forbidden):
        return "fail"
    except Exception as e:
        print(f"Error checking token status: {e}")
        return "fail"


def display_token_info(headers, data):
    table_data = [[header] + [value] for header, value in zip(headers, data)]
    table = tabulate(table_data, tablefmt="grid")
    print("\n"+table+"\n",flush=True)


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
        token_status = check_token_status(vault_addr, token_accessor_id)
        status_icon = logo_mapping.get(token_status, "")

        display_token_info(
            ["Token Accessor ID", "Token Expiration", "Validity"],
            [token_accessor_id, token_ttl, status_icon],
        )

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
        token_info = client.lookup_token(accessor=vault_token_accessor_id)["data"]
        token = token_info.get("id")
        client.revoke_token(token=token)

        status = check_token_status(vault_addr, vault_token_accessor_id)

        if token_info:
            accessor_id = token_info.get("accessor")
            ttl = token_info.get("ttl")
            formatted_ttl = format_ttl(ttl)
            status_icon = logo_mapping.get(status, "")

            display_token_info(
                ["Token Accessor ID", "TTL", "Status"],
                [accessor_id, formatted_ttl, status_icon],
            )
        else:
            print("Token information not available.")

        return status
    except Exception as e:
        print(f"Error revoking token: {e}")
        return "fail"
