import httpx
from datetime import datetime
import uuid
from app.config import config


class AsignacionService:
    def __init__(self):
        self.productos_url = config.MS1_PRODUCTOS_URL
        self.logistica_url = config.MS2_LOGISTICA_URL
        self.pedidos_url = config.MS3_PEDIDOS_URL

    # 🔹 1. Obtener pedido desde MS3
    async def obtener_pedido(self, id_pedido: str):
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(f"{self.pedidos_url}/pedidos/{id_pedido}")
                response.raise_for_status()
                return response.json()
            except Exception as e:
                print(f"❌ Error obteniendo pedido {id_pedido}: {e}")
                return None

    # 🔹 2. Verificar stock de producto (MS1)
    async def verificar_stock_producto(self, id_producto: int, cantidad: int):
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(f"{self.productos_url}/api/v1/inventario/{id_producto}")
                response.raise_for_status()
                inventario = response.json()
                stock_disponible = inventario.get("stock_disponible", 0)
                return stock_disponible >= cantidad
            except Exception as e:
                print(f"❌ Error verificando stock del producto {id_producto}: {e}")
                return False

    # 🔹 3. Buscar conductor disponible (MS2)
    async def obtener_conductor_disponible(self):
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(f"{self.logistica_url}/conductores/disponibles")
                response.raise_for_status()
                conductores = response.json()
                return conductores[0] if conductores else None
            except Exception as e:
                print(f"❌ Error obteniendo conductores disponibles: {e}")
                return None

    # 🔹 4. Asignar conductor al pedido (MS3)
    async def asignar_conductor_a_pedido(self, id_pedido: str, id_conductor: int):
        async with httpx.AsyncClient() as client:
            try:
                payload = {"id_conductor": id_conductor, "estado": "asignado"}
                response = await client.put(f"{self.pedidos_url}/pedidos/{id_pedido}", json=payload)
                response.raise_for_status()
                print(f"✅ Pedido {id_pedido} asignado al conductor {id_conductor}")
                return True
            except Exception as e:
                print(f"❌ Error asignando conductor al pedido: {e}")
                return False

    # 🔹 5. Marcar conductor como no disponible (MS2)
    async def actualizar_disponibilidad_conductor(self, id_conductor: int, disponible: bool):
        async with httpx.AsyncClient() as client:
            try:
                payload = {"disponible": True}
                await client.put(f"{self.logistica_url}/conductores/{id_conductor}", json=payload)
                print(f"🚗 Conductor {id_conductor} actualizado a disponible={disponible}")
            except Exception as e:
                print(f"❌ Error actualizando conductor: {e}")

    # 🔹 6. Flujo principal de asignación
    async def asignar_pedido(self, id_pedido: str):
        print(f"🚀 Iniciando asignación de pedido {id_pedido}")

        pedido = await self.obtener_pedido(id_pedido)
        if not pedido:
            return {"error": "Pedido no encontrado"}

        for detalle in pedido.get("detalles", []):
            ok = await self.verificar_stock_producto(detalle["id_producto"], detalle["cantidad"])
            if not ok:
                return {"error": f"Stock insuficiente para producto {detalle['id_producto']}"}

        conductor = await self.obtener_conductor_disponible()
        if not conductor:
            return {"error": "No hay conductores disponibles"}

        asignado = await self.asignar_conductor_a_pedido(id_pedido, conductor["idConductor"])
        if asignado:
            await self.actualizar_disponibilidad_conductor(conductor["idConductor"], False)

        return {
            "id_asignacion": str(uuid.uuid4()),
            "id_pedido": id_pedido,
            "id_conductor": conductor["idConductor"],
            "nombre_conductor": conductor["nombre"],
            "fecha_asignacion": datetime.now().isoformat(),
            "estado": "asignado",
        }

    # 🔹 7. Generar reporte simple de eficiencia
    async def generar_reporte_eficiencia(self):
        async with httpx.AsyncClient() as client:
            try:
                pedidos_resp = await client.get(f"{self.pedidos_url}/pedidos")
                pedidos_resp.raise_for_status()
                pedidos = pedidos_resp.json()
                total = len(pedidos)
                entregados = len([p for p in pedidos if p.get("estado") == "entregado"])

                tasa_exito = round((entregados / total) * 100, 2) if total else 0

                return {
                    "total_pedidos": total,
                    "pedidos_entregados": entregados,
                    "tasa_exito": tasa_exito,
                    "fecha_reporte": datetime.now().isoformat(),
                }
            except Exception as e:
                print(f"❌ Error generando reporte de eficiencia: {e}")
                return {"error": "No se pudo generar el reporte"}
