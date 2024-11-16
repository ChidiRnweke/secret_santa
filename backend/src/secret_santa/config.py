from dotenv import load_dotenv
import os
from dataclasses import dataclass
import hvac


class AppStartupError(Exception):
    pass


def get_env_or_raise(env_var: str) -> str:
    value = os.getenv(env_var)
    if value is None:
        raise AppStartupError(f"Environment variable {env_var} not set")
    return value


def validate_config() -> None:
    AppConfig.from_config()


@dataclass
class AppConfig:
    connection_string: str

    @classmethod
    def from_config(cls) -> "AppConfig":
        load_dotenv()
        if os.getenv("DEV"):
            conf = cls._from_env()
        else:
            conf = cls._from_vault()
        return conf

    @classmethod
    def _from_env(cls) -> "AppConfig":
        conn_str = get_env_or_raise("CONNECTION_STRING")
        return cls(connection_string=conn_str)

    @classmethod
    def _from_vault(cls) -> "AppConfig":
        vault_addr = get_env_or_raise("VAULT_ADDR")
        role_id = get_env_or_raise("VAULT_ROLE_ID")
        secret_id = get_env_or_raise("VAULT_SECRET_ID")
        vault_path = get_env_or_raise("VAULT_PATH")
        try:
            client = hvac.Client(url=vault_addr)
            client.auth.approle.login(role_id, secret_id)

            if not client.is_authenticated():
                raise AppStartupError("Vault authentication failed.")
            secret = client.read(vault_path)

            if not isinstance(secret, dict) or "data" not in secret:
                raise AppStartupError("Secret not found in vault")

            conn_str = secret["data"]["connection_string"]
        except Exception as e:
            raise AppStartupError(f"Error reading secret from vault: {e}") from e
        return cls(connection_string=conn_str)
