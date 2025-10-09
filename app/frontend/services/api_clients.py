import requests
import os

def get_base_url():
    """
    Determina la URL base según el entorno
    """
    # Para desarrollo local en VS Code
    return os.getenv("MS4_URL", "http://localhost:8003")

def test_api_connection():
    """
    Verifica que el Microservicio 4 esté respondiendo
    """
    base_url = get_base_url()
    try:
        response = requests.get(f"{base_url}/health", timeout=10)
        if response.status_code == 200:
            return True, f"Microservicio 4 está en línea en {base_url}"
        else:
            return False, f"Error HTTP {response.status_code} desde {base_url}"
    except requests.exceptions.RequestException as e:
        return False, f"No se puede conectar al MS4 en {base_url}: {str(e)}"

def asignar_pedido(pedido_id):
    """
    Llama al endpoint /asignarPedido/{id_pedido} del MS4
    """
    base_url = get_base_url()
    try:
        response = requests.post(
            f"{base_url}/asignarPedido/{pedido_id}",
            timeout=30
        )
        
        if response.status_code == 200:
            return {
                'success': True,
                'data': response.json()
            }
        else:
            return {
                'success': False,
                'error': f"Error {response.status_code} desde {base_url}: {response.text}"
            }
            
    except requests.exceptions.RequestException as e:
        return {
            'success': False,
            'error': f"Error de conexión con {base_url}: {str(e)}"
        }

def obtener_reporte_eficiencia(periodo):
    """
    Llama al endpoint /reportes/eficiencia/{periodo} del MS4
    """
    base_url = get_base_url()
    try:
        response = requests.get(
            f"{base_url}/reportes/eficiencia/{periodo}",
            timeout=30
        )
        
        if response.status_code == 200:
            return {
                'success': True,
                'data': response.json()
            }
        else:
            return {
                'success': False,
                'error': f"Error {response.status_code} desde {base_url}: {response.text}"
            }
            
    except requests.exceptions.RequestException as e:
        return {
            'success': False,
            'error': f"Error de conexión con {base_url}: {str(e)}"
        }