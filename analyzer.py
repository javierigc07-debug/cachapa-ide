"""Análisis estático simple de código para generar diagnósticos."""

from sorting import Diagnostic


class StaticAnalyzer:
    def analyze(self, code: str):
        """Genera una lista de diagnósticos según reglas heurísticas simples."""
        diagnostics = []
        lines = code.split("\n")

        for i, line in enumerate(lines, start=1):
            stripped = line.strip()
            length = len(line)

            if length > 79:
                diagnostics.append(Diagnostic(i, f"Línea excede 79 caracteres ({length}).", "warning"))

            if "TODO" in stripped.upper():
                diagnostics.append(Diagnostic(i, "Comentario TODO pendiente.", "info"))

            if stripped.count("(") != stripped.count(")"):
                diagnostics.append(Diagnostic(i, "Posible paréntesis desbalanceado en la línea.", "error"))

            if "eval(" in stripped or "exec(" in stripped:
                diagnostics.append(Diagnostic(i, "Uso de eval/exec: riesgo de seguridad.", "critical"))

            if stripped.startswith("def ") and "self" not in stripped and i > 1:
                diagnostics.append(Diagnostic(i, "Función definida fuera de clase o sin 'self'.", "info"))

        if not diagnostics:
            diagnostics.append(Diagnostic(0, "No se detectaron problemas evidentes.", "info"))

        return diagnostics