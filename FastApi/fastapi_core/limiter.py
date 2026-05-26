from slowapi import Limiter
from slowapi.util import get_remote_address

# Inicializa el limiter basándose en la IP del cliente (remote address)
# Si el Redis está inalcanzable, esto usará almacenamiento en memoria por defecto
# lo cual cumple con el requerimiento de Graceful Degradation (no tirar la API).
limiter = Limiter(key_func=get_remote_address)
