import os
import hvac
from factory.utils import load_config, logo_mapping

def vault_login_approle(args):
    config = load_config()
    client = hvac.Client(url=config["vault_addr"])
    approle_id = args.approle_id
    secret_id = args.approle_secret_id

    try:
        response = client.auth.approle.login(role_id=approle_id, secret_id=secret_id)
        client.token = response['auth']['client_token']

        os.environ["VAULT_TOKEN"] = f"{client.token}"

        print(f"Successfully authenticated to Vault. Token: {client.token}")
        print(response)
        return "pass"
    except Exception as e:
        print(f"Error logging in to Vault: {e}")
        return "fail"
