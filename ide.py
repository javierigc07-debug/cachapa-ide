"""Clase principal del Mini IDE: orquesta módulos y dispatchea comandos (Command Pattern)."""

from linked_list import FileLinkedList
from syntax_checker import SyntaxChecker
from history_manager import HistoryManager
from config_loader import ConfigLoader
from ai_client import AIClient
from request_buffer import RequestBuffer
from analyzer import StaticAnalyzer

import commands


class SynthetixIDE:
    def __init__(self):
        self.file_list = FileLinkedList()
        self.syntax_checker = SyntaxChecker()
        self.config = ConfigLoader()
        self.ai_client = AIClient(self.config)
        self.request_buffer = RequestBuffer(self.ai_client)
        self.analyzer = StaticAnalyzer()

        self._histories = {}  # nombre_archivo -> HistoryManager

        self._command_map = {
            "new": commands.NewFileCommand(self),
            "list": commands.ListFilesCommand(self),
            "switch": commands.SwitchFileCommand(self),
            "delete": commands.DeleteFileCommand(self),
            "config": commands.ConfigCommand(self),
            "check": commands.CheckCommand(self),
            "undo": commands.UndoCommand(self),
            "redo": commands.RedoCommand(self),
            "edit": commands.EditCommand(self),
            "sort": commands.SortCommand(self),
            "queue-status": commands.QueueStatusCommand(self),
            "analyze": commands.AnalyzeCommand(self),
            "help": commands.HelpCommand(self),
        }

    def get_history(self, filename: str) -> HistoryManager:
        if filename not in self._histories:
            self._histories[filename] = HistoryManager()
        return self._histories[filename]

    def save_backup(self, filename: str, content: str):
        """Guarda un respaldo físico del archivo si la configuración fue cargada."""
        if not self.config.loaded or not self.config.backup_dir:
            return
        try:
            import os
            path = os.path.join(self.config.backup_dir, filename)
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
        except Exception as e:
            self.log_error(f"Error al crear respaldo de {filename}: {e}")

    def log_error(self, message: str):
        """Escribe un mensaje de error en el archivo de log configurado."""
        if not self.config.loaded or not self.config.log_dir:
            return
        try:
            import os
            from datetime import datetime
            path = os.path.join(self.config.log_dir, "syntax_errors.log")
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open(path, "a", encoding="utf-8") as f:
                f.write(f"[{timestamp}] {message}\n")
        except Exception:
            pass

    def ai_client_refresh(self):
        self.ai_client = AIClient(self.config)
        self.request_buffer = RequestBuffer(self.ai_client)

    def read_block(self) -> str:
        """Lee contenido multilínea desde la consola hasta una línea ':fin'."""
        print("Escriba el contenido (termine con una línea ':fin'):")
        lines = ""
        while True:
            try:
                line = input()
            except EOFError:
                break
            if line.strip() == ":fin":
                break
            lines += line + "\n"
        return lines.rstrip("\n")

    def dispatch(self, line: str):
        """Parsea una línea de entrada y ejecuta el comando (Command Pattern)."""
        parts = line.strip().split()
        if not parts:
            return
        cmd_name = parts[0]
        args = parts[1:]

        command = self._command_map.get(cmd_name)
        if command is None:
            print(f"Comando desconocido: '{cmd_name}'. Escriba 'help' para ver la lista.")
            return
        command.execute(args)

    def help_text(self) -> str:
        return (
            "Comandos disponibles:\n"
            "  new <nombre_archivo>               - Crea un archivo (contenido hasta ':fin')\n"
            "  list                               - Lista archivos abiertos\n"
            "  switch <id/nombre>                 - Cambia archivo activo\n"
            "  delete <id/nombre>                 - Elimina un archivo\n"
            "  config <ruta_archivo>              - Carga configuración externa\n"
            "  check                              - Valida balanceo de símbolos\n"
            "  edit                               - Reescribe el archivo activo (hasta ':fin')\n"
            "  undo                               - Deshace el último cambio\n"
            "  redo                               - Rehace el cambio deshecho\n"
            "  sort <line|severity> <mergesort|shellsort> - Ordena diagnósticos\n"
            "  queue-status                       - Estado de la cola de peticiones IA\n"
            "  analyze                            - Envía código activo a la API de IA\n"
            "  help                               - Muestra esta ayuda\n"
            "  exit                               - Sale del programa\n"
        )