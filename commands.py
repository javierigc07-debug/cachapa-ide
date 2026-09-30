"""Implementación del patrón de diseño Command para las operaciones del IDE."""

from abc import ABC, abstractmethod


class Command(ABC):
    """Interfaz base del patrón Command."""

    @abstractmethod
    def execute(self, *args):
        raise NotImplementedError


class NewFileCommand(Command):
    def __init__(self, ide):
        self.ide = ide

    def execute(self, args):
        if not args:
            print("Uso: new <nombre_archivo>")
            return
        name = args[0]
        content = " ".join(args[1:]) if len(args) > 1 else self.ide.read_block()
        node = self.ide.file_list.create_file(name, content)
        self.ide.save_backup(node.name, node.content)
        print(f"Archivo '{node.name}' creado y establecido como activo.")


class ListFilesCommand(Command):
    def __init__(self, ide):
        self.ide = ide

    def execute(self, args):
        files = self.ide.file_list.list_files()
        if not files:
            print("No hay archivos abiertos.")
            return
        print("Archivos abiertos en la sesión:")
        for pos, name, is_active in files:
            marker = " (ACTIVO)" if is_active else ""
            print(f"  [{pos}] {name}{marker}")


class SwitchFileCommand(Command):
    def __init__(self, ide):
        self.ide = ide

    def execute(self, args):
        if not args:
            print("Uso: switch <id/nombre>")
            return
        identifier = args[0]
        if self.ide.file_list.switch_active(identifier):
            node = self.ide.file_list.active_node
            print(f"Archivo activo cambiado a '{node.name}'.")
            print(f"--- Contenido ---\n{node.content}\n-----------------")
        else:
            print(f"No se encontró el archivo '{identifier}'.")


class DeleteFileCommand(Command):
    def __init__(self, ide):
        self.ide = ide

    def execute(self, args):
        if not args:
            print("Uso: delete <id/nombre>")
            return
        identifier = args[0]
        if self.ide.file_list.delete_file(identifier):
            print(f"Archivo '{identifier}' eliminado y memoria liberada.")
        else:
            print(f"No se encontró el archivo '{identifier}'.")


class ConfigCommand(Command):
    def __init__(self, ide):
        self.ide = ide

    def execute(self, args):
        if not args:
            print("Uso: config <ruta_archivo>")
            return
        path = args[0]
        try:
            self.ide.config.load(path)
            self.ide.ai_client_refresh()
            print("Configuración cargada exitosamente:")
            print(f"  {self.ide.config}")
        except Exception as e:
            print(f"Error al cargar configuración: {e}")


class CheckCommand(Command):
    def __init__(self, ide):
        self.ide = ide

    def execute(self, args):
        active = self.ide.file_list.active_node
        if active is None:
            print("No hay archivo activo. Use 'new' primero.")
            return
        ok, message = self.ide.syntax_checker.check(active.content)
        if not ok:
            self.ide.log_error(f"[{active.name}] {message}")
        print(message)


class UndoCommand(Command):
    def __init__(self, ide):
        self.ide = ide

    def execute(self, args):
        active = self.ide.file_list.active_node
        if active is None:
            print("No hay archivo activo.")
            return
        history = self.ide.get_history(active.name)
        previous = history.undo(active.content)
        if previous is None:
            print("No hay cambios para deshacer.")
        else:
            active.content = previous
            self.ide.save_backup(active.name, active.content)
            print(f"Undo aplicado. Contenido actual:\n{active.content}")


class RedoCommand(Command):
    def __init__(self, ide):
        self.ide = ide

    def execute(self, args):
        active = self.ide.file_list.active_node
        if active is None:
            print("No hay archivo activo.")
            return
        history = self.ide.get_history(active.name)
        nxt = history.redo(active.content)
        if nxt is None:
            print("No hay cambios para rehacer.")
        else:
            active.content = nxt
            self.ide.save_backup(active.name, active.content)
            print(f"Redo aplicado. Contenido actual:\n{active.content}")


class EditCommand(Command):
    """Comando adicional necesario para modificar el archivo activo y alimentar Undo/Redo."""

    def __init__(self, ide):
        self.ide = ide

    def execute(self, args):
        active = self.ide.file_list.active_node
        if active is None:
            print("No hay archivo activo. Use 'new' primero.")
            return
        new_content = " ".join(args) if args else self.ide.read_block()
        history = self.ide.get_history(active.name)
        history.register_change(active.content)
        active.content = new_content
        self.ide.save_backup(active.name, active.content)
        print(f"Contenido de '{active.name}' actualizado.")


class SortCommand(Command):
    def __init__(self, ide):
        self.ide = ide

    def execute(self, args):
        if len(args) < 2:
            print("Uso: sort <line|severity> <mergesort|shellsort>")
            return
        criterio, algoritmo = args[0], args[1]
        active = self.ide.file_list.active_node
        if active is None:
            print("No hay archivo activo.")
            return

        diagnostics = self.ide.analyzer.analyze(active.content)

        from sorting import Sorter
        try:
            if algoritmo == "mergesort":
                ordered = Sorter.mergesort(diagnostics, criterio)
            elif algoritmo == "shellsort":
                ordered = Sorter.shellsort(diagnostics, criterio)
            else:
                print("Algoritmo inválido. Use 'mergesort' o 'shellsort'.")
                return
        except ValueError as e:
            print(e)
            return

        print(f"Diagnósticos ordenados por '{criterio}' usando {algoritmo}:")
        for diag in ordered:
            print(f"  {diag}")


class QueueStatusCommand(Command):
    def __init__(self, ide):
        self.ide = ide

    def execute(self, args):
        status = self.ide.request_buffer.status()
        print(f"Peticiones pendientes en la cola: {status['pendientes']}")
        for item in status["detalle"]:
            print(f"  - {item}")


class AnalyzeCommand(Command):
    def __init__(self, ide):
        self.ide = ide

    def execute(self, args):
        active = self.ide.file_list.active_node
        if active is None:
            print("No hay archivo activo.")
            return
        req = self.ide.request_buffer.enqueue_request(active.name, active.content)
        print(f"Petición encolada: {req}. Procesando cola de forma secuencial...")
        results = self.ide.request_buffer.process_all()
        for r in results:
            if r is None:
                continue
            processed_req, response = r
            print(f"\nResultado de {processed_req}:")
            print(f"  Fuente: {response['source']}")
            print(f"  {response['result']}")


class HelpCommand(Command):
    def __init__(self, ide):
        self.ide = ide

    def execute(self, args):
        print(self.ide.help_text())