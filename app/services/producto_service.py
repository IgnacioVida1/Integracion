import httpx
from app.config import config

class ProductoService:
    def __init__(self):
        self.base_url = config.MS1_PRODUCTOS_URL
    
    async def consultar_producto(self, id_producto: str):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/productos/{id_producto}")
                return response.json()
        except Exception as e:
            print(f"Error consultando producto: {e}")
            return None
    
    async def verificar_stock(self, id_producto: str, cantidad: int):
        # TODO: Implementar llamada real
        producto = await self.consultar_producto(id_producto)
        if producto and producto.get("stock_disponible", 0) >= cantidad:
            return True
        return False