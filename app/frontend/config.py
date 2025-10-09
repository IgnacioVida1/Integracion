import os

class FrontendConfig:
    """Configuración para el frontend de Streamlit"""
    
    # Configuración de la aplicación
    APP_TITLE = "Microservicio 4 - Integración"
    APP_DESCRIPTION = "Frontend para testing del MS4 - Integración"
    
    # Configuración de APIs
    DEFAULT_MS4_URL = "http://localhost:5003"
    
    # Configuración de tiempo de espera
    REQUEST_TIMEOUT = 30

# Instancia de configuración
config = FrontendConfig()