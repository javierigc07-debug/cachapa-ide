"""Cliente HTTP para comunicación con la API de IA (análisis de código)."""

import json
import urllib.request
import urllib.error


class AIClient:
    def __init__(self, config):
        self.config = config

    def analyze_code(self, source_code: str) -> dict:
        """
        Envía el código a la API de IA para obtener métricas de complejidad
        (Big O) y propuestas de refactorización.
        Soporta formato OpenAI (OpenRouter) y formato Google Gemini API.
        """
        if not self.config.loaded or not self.config.api_key:
            return self._local_fallback(source_code, reason="Config de API no establecida (modo offline).")

        url = self.config.full_api_url()

        # Si es la API oficial de Google Gemini
        if "generativelanguage.googleapis.com" in url:
            if "?" in url:
                url += f"&key={self.config.api_key}"
            else:
                url += f"?key={self.config.api_key}"

            payload = {
                "contents": [
                    {
                        "parts": [
                            {
                                "text": (
                                    "Eres un analizador estático de código. Analiza el siguiente código fuente "
                                    "e indica su complejidad temporal Big O (ejemplo: O(1), O(n), O(n^2)) y "
                                    "da sugerencias breves de refactorización:\n\n" + source_code
                                )
                            }
                        ]
                    }
                ]
            }
            headers = {"Content-Type": "application/json"}

        # De lo contrario se usa el formato estándar OpenAI / OpenRouter
        else:
            payload = {
                "model": self.config.api_model,
                "messages": [
                    {
                        "role": "system",
                        "content": "Eres un analizador de código. Da la complejidad Big O "
                                    "y sugerencias breves de refactorización."
                    },
                    {"role": "user", "content": source_code}
                ]
            }
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.config.api_key}"
            }

        try:
            req = urllib.request.Request(
                url, data=json.dumps(payload).encode("utf-8"),
                headers=headers, method="POST"
            )
            with urllib.request.urlopen(req, timeout=self.config.api_timeout) as resp:
                body = json.loads(resp.read().decode("utf-8"))

                # Parsear respuesta según la API receptora
                if "candidates" in body:
                    content = body["candidates"][0]["content"]["parts"][0]["text"]
                elif "choices" in body:
                    content = body["choices"][0]["message"]["content"]
                else:
                    content = str(body)

                return {"ok": True, "source": "api", "result": content}
        except (urllib.error.URLError, urllib.error.HTTPError, KeyError, TimeoutError, Exception) as e:
            return self._local_fallback(source_code, reason=f"Fallo de conexión con la API: {e}")

    def _local_fallback(self, source_code: str, reason: str) -> dict:
        """Estimación local simple cuando la API no está disponible."""
        loops = source_code.count("for") + source_code.count("while")
        if loops >= 2:
            complexity = "O(n^2) (estimado, múltiples bucles anidados posibles)"
        elif loops == 1:
            complexity = "O(n) (estimado, un bucle principal)"
        else:
            complexity = "O(1) (estimado, sin bucles detectados)"

        suggestion = "Considere extraer funciones y reducir anidamiento de condicionales."
        return {
            "ok": False,
            "source": "local_fallback",
            "reason": reason,
            "result": f"Complejidad estimada: {complexity}. Sugerencia: {suggestion}"
        }