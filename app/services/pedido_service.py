import httpx
from app.config import config

class PedidoService:
    def __init__(self):
        self.base_url = config.MS3_PEDIDOS_URL
    
    async def obtener_pedido(self, id_pedido: str, estado: str):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.put(f"{self.base_url}/pedidos/{id_pedido}", json={"estado": estado})
                return response.json()
        except Exception as e:
            print(f"Error obteniendo pedido: {e}")
            return None
    
    async def actualizar_estado_pedido(self, id_pedido: str, estado: str):
        # TODO: Implementar llamada real
        await self.consultar_producto(id_pedido, estado)
        print(f"Actualizando pedido {id_pedido} a estado: {estado}")
        return {"success": True}