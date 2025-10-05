from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class AsignacionPedidoRequest(BaseModel):
    id_pedido: str
    id_cliente_final: str
    direccion_entrega: str
    ventana_horaria: str

class AsignacionPedidoResponse(BaseModel):
    id_asignacion: str
    id_pedido: str
    id_conductor: Optional[str] = None
    id_vehiculo: Optional[str] = None
    id_almacen: Optional[str] = None
    estado: str
    fecha_asignacion: datetime
    detalles: List[dict] = []

class ReporteEficiencia(BaseModel):
    periodo: str
    total_pedidos: int
    pedidos_entregados: int
    tasa_exito: float
    tiempo_promedio_entrega: float