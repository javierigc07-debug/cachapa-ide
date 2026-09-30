"""Buffer de peticiones hacia la API de IA usando cola FIFO propia."""

from queue_fifo import FIFOQueue


class AnalysisRequest:
    def __init__(self, request_id: int, filename: str, code_snapshot: str):
        self.request_id = request_id
        self.filename = filename
        self.code_snapshot = code_snapshot

    def __repr__(self):
        return f"Request#{self.request_id}({self.filename})"


class RequestBuffer:
    """Administra peticiones de análisis de forma estrictamente secuencial."""

    def __init__(self, ai_client):
        self._queue = FIFOQueue()
        self._ai_client = ai_client
        self._next_id = 1

    def enqueue_request(self, filename: str, code_snapshot: str) -> AnalysisRequest:
        req = AnalysisRequest(self._next_id, filename, code_snapshot)
        self._next_id += 1
        self._queue.enqueue(req)
        return req

    def status(self):
        pending = self._queue.to_list_snapshot()
        return {
            "pendientes": len(pending),
            "detalle": [repr(r) for r in pending]
        }

    def process_next(self):
        """Despacha y procesa la siguiente petición pendiente (FIFO)."""
        if self._queue.is_empty():
            return None
        req = self._queue.dequeue()
        result = self._ai_client.analyze_code(req.code_snapshot)
        return req, result

    def process_all(self):
        """Procesa todas las peticiones pendientes de forma secuencial."""
        results = []
        while not self._queue.is_empty():
            results.append(self.process_next())
        return results