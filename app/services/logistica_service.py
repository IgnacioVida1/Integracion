import httpx
from app.config import config

class LogisticaService:
    def __init__(self):
        self.base_url = config.MS2_LOGISTICA_URL
    
    async def buscar_conductor_disponible(self):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/conductores/disponibles")
                return response.json()
        except Exception as e:
            print(f"Error buscando conductor: {e}")
            return None
    