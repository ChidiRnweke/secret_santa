from dotenv import load_dotenv
import os
from dataclasses import dataclass
from enum import Enum
from infisical_client import (
    ClientSettings,
    InfisicalClient,
    GetSecretOptions,
    AuthenticationOptions,
    UniversalAuthMethod,
)


class RuntimeMode(Enum):
    DEV = "DEV"
    PROD = "PROD"


class AppStartupError(Exception):
    pass


def get_env_or_raise(env_var: str) -> str:
    value = os.getenv(env_var)
    if value is None:
        raise AppStartupError(f"Environment variable {env_var} not set")
    return value


@dataclass
class AppConfig:
    connection_string: str
    migrations_connection_string: str
    telemetry_endpoint: str
    mode: RuntimeMode = RuntimeMode.PROD

    @classmethod
    def from_config(cls) -> "AppConfig":
        load_dotenv()
        if os.getenv("ENV") == "LOCAL":
            conf = cls._from_env()
        else:
            conf = cls._from_vault()
        return conf

    @classmethod
    def _from_env(cls) -> "AppConfig":
        conn_str = get_env_or_raise("CONNECTION_STRING")
        telemetry_endpoint = get_env_or_raise("TELEMETRY_ENDPOINT")
        migrations_conn_str = get_env_or_raise("MIGRATIONS_DATABASE_CONNECTION_STRING")
        return cls(
            connection_string=conn_str,
            telemetry_endpoint=telemetry_endpoint,
            migrations_connection_string=migrations_conn_str,
            mode=RuntimeMode.DEV,
        )

    @classmethod
    def _from_vault(cls) -> "AppConfig":
        client_id = get_env_or_raise("INFISICAL_CLIENT_ID")
        client_secret = get_env_or_raise("INFISICAL_CLIENT_SECRET")
        project_id = get_env_or_raise("INFISICAL_PROJECT_ID")
        environment = get_env_or_raise("INFISICAL_ENVIRONMENT")
        url = get_env_or_raise("INFISICAL_URL")

        auth = UniversalAuthMethod(client_id=client_id, client_secret=client_secret)
        auth_options = AuthenticationOptions(universal_auth=auth)
        client_settings = ClientSettings(auth=auth_options, site_url=url)
        try:
            client = InfisicalClient(client_settings)
            conn_str = client.getSecret(
                options=GetSecretOptions(
                    environment=environment,
                    project_id=project_id,
                    secret_name="DATABASE_CONNECTION_STRING",
                )
            )

            telemetry_endpoint = client.getSecret(
                options=GetSecretOptions(
                    environment=environment,
                    project_id=project_id,
                    secret_name="TELEMETRY_ENDPOINT",
                )
            )
            migrations_conn_str = client.getSecret(
                options=GetSecretOptions(
                    environment=environment,
                    project_id=project_id,
                    secret_name="MIGRATIONS_DATABASE_CONNECTION_STRING",
                )
            )
            conn_str = conn_str.secret_value
            telemetry_endpoint = telemetry_endpoint.secret_value
            migrations_conn_str = migrations_conn_str.secret_value
        except Exception as e:
            raise AppStartupError(f"Error reading secret from infisical: {e}") from e
        return cls(
            connection_string=conn_str,
            telemetry_endpoint=telemetry_endpoint,
            migrations_connection_string=migrations_conn_str,
        )

    def _read_secret(
        self,
        secret_name: str,
        client: InfisicalClient,
        project_id: str,
        environment: str,
    ) -> str:
        secret = client.getSecret(
            options=GetSecretOptions(
                environment=environment,
                project_id=project_id,
                secret_name=secret_name,
            )
        )
        return secret.secret_value
