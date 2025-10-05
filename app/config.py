import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # 🔄 URLs actualizadas de los microservicios (usar variables de entorno)
    MS1_PRODUCTOS_URL = os.getenv("MS1_PRODUCTOS_URL", "http://api_productos:8001")  # ProductosYAlmacen
    MS2_LOGISTICA_URL = os.getenv("MS2_LOGISTICA_URL", "http://api_logistica:8002")   # Micrologistica
    MS3_PEDIDOS_URL = os.getenv("MS3_PEDIDOS_URL", "http://api_pedidos:8003")       # PedidosYClientes
    
    # Configuración del servidor (se mantiene igual)
    PORT = int(os.getenv("PORT", 8004))
    HOST = os.getenv("HOST", "0.0.0.0")

config = Config()