from fastapi import FastAPI, HTTPException
from app.services.asignacion_service import AsignacionService

# Inicializar aplicación FastAPI
app = FastAPI(
    title="Microservicio 4 - Orquestador Logístico",
    description="Coordina pedidos, productos y logística entre microservicios.",
    version="2.0.0"
)

# Inicializar servicio principal
asignacion_service = AsignacionService()


@app.get("/")
async def root():
    return {"message": "🟢 Microservicio 4 (Orquestador) operativo"}


@app.post("/asignar/{id_pedido}")
async def asignar_pedido(id_pedido: str):
    try:
        resultado = await asignacion_service.asignar_pedido(id_pedido)
        if "error" in resultado:
            raise HTTPException(status_code=400, detail=resultado["error"])
        return resultado
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/reporte/eficiencia")
async def obtener_reporte_eficiencia():

    try:
        reporte = await asignacion_service.generar_reporte_eficiencia()
        return reporte
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "ms4-orquestador"}


if __name__ == "__main__":
    import uvicorn
    from app.config import config
    uvicorn.run(app, host=config.HOST, port=config.PORT)
