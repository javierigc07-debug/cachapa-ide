"""Verificador de balanceo de símbolos de agrupación usando pila propia."""

from stack import Stack


class SyntaxChecker:
    OPEN = {"(": ")", "{": "}", "[": "]"}
    CLOSE = {")": "(", "}": "{", "]": "["}

    def check(self, code: str):
        """
        Valida el balanceo de (), {}, [] en el texto dado.
        Retorna (True, "") si está balanceado,
        o (False, mensaje_con_linea_y_columna) si no lo está.
        """
        stack = Stack()
        line = 1
        col = 0

        for ch in code:
            col += 1
            if ch == "\n":
                line += 1
                col = 0
                continue

            if ch in self.OPEN:
                stack.push((ch, line, col))
            elif ch in self.CLOSE:
                if stack.is_empty():
                    return False, (
                        f"Error: símbolo de cierre '{ch}' sin apertura "
                        f"correspondiente en línea {line}, columna {col}."
                    )
                open_ch, open_line, open_col = stack.pop()
                if self.OPEN[open_ch] != ch:
                    return False, (
                        f"Error: se esperaba '{self.OPEN[open_ch]}' para cerrar "
                        f"'{open_ch}' (abierto en línea {open_line}, col {open_col}), "
                        f"pero se encontró '{ch}' en línea {line}, columna {col}."
                    )

        if not stack.is_empty():
            open_ch, open_line, open_col = stack.pop()
            return False, (
                f"Error: símbolo '{open_ch}' abierto en línea {open_line}, "
                f"columna {open_col} nunca fue cerrado."
            )

        return True, "El código está correctamente balanceado."