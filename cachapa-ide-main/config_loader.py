"""Carga y validación del archivo de configuración externo (JSON)."""

import json
import os


class ConfigLoader:
    def __init__(self):
        self.backup_dir = None
        self.log_dir = None
        self.api_base_url = None
        self.api_endpoint = None
        self.api_key = None
        self.api_model = None
        self.api_timeout = 30
        self.loaded = False

    def load(self, path: str):
        if not os.path.exists(path):
            raise FileNotFoundError(f"No se encontró el archivo de configuración: {path}")

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.backup_dir = data.get("backup_dir", "./backups")
        self.log_dir = data.get("log_dir", "./logs")

        api = data.get("api", {})
        self.api_base_url = api.get("base_url", "")
        self.api_endpoint = api.get("endpoint", "")
        # La clave no se guarda en el repositorio: se toma de la variable de
        # entorno indicada en el JSON (api_key_env).
        self.api_key = os.environ.get(api.get("api_key_env", "SYNTHETIX_API_KEY"), "")
        self.api_model = api.get("model", "")
        self.api_timeout = api.get("timeout_s", 30)

        os.makedirs(self.backup_dir, exist_ok=True)
        os.makedirs(self.log_dir, exist_ok=True)

        self.loaded = True
        return self

    def full_api_url(self) -> str:
        return f"{self.api_base_url}{self.api_endpoint}"

    def __repr__(self):
        return (
            f"ConfigLoader(backup_dir={self.backup_dir}, log_dir={self.log_dir}, "
            f"api_url={self.full_api_url()}, model={self.api_model})"
        )