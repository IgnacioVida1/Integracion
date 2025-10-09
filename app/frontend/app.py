import streamlit as st
import sys
import os

# Añadir el directorio actual al path para importar módulos locales
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from services.api_client import test_api_connection, asignar_pedido, obtener_reporte_eficiencia

# Configuración de la página
st.set_page_config(
    page_title="Microservicio 4 - Integración",
    page_icon="🔄",
    layout="wide"
)

# Título principal
st.title("🧩 Frontend - Microservicio 4: Integración")
st.markdown("---")

# Sidebar para configuración
with st.sidebar:
    st.header("Configuración")
    ms4_url = st.text_input(
        "URL del Microservicio 4",
        value="http://localhost:8003",
        help="URL base donde está corriendo el MS4"
    )
    
    # Configurar variable de entorno temporalmente
    os.environ["MS4_URL"] = ms4_url
    
    st.header("Estado de los Servicios")
    if st.button("Verificar Conexión MS4"):
        with st.spinner("Verificando conexión..."):
            status, message = test_api_connection()
            if status:
                st.success(f"✅ {message}")
            else:
                st.error(f"❌ {message}")

# Sección 1: Probar Endpoint de Asignación de Pedidos
st.header("📦 Asignación de Pedidos")
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Probar Asignación")
    pedido_id = st.text_input("ID del Pedido", value="PED-001")
    
    if st.button("Asignar Pedido", type="primary"):
        if pedido_id:
            with st.spinner(f"Asignando pedido {pedido_id}..."):
                resultado = asignar_pedido(pedido_id)
                st.session_state.resultado_asignacion = resultado
        else:
            st.warning("Por favor, ingresa un ID de pedido")

with col2:
    st.subheader("Resultado de la Asignación")
    if 'resultado_asignacion' in st.session_state:
        resultado = st.session_state.resultado_asignacion
        if resultado.get('success'):
            st.success("✅ Pedido asignado correctamente")
            st.json(resultado.get('data', {}))
        else:
            st.error(f"❌ Error: {resultado.get('error', 'Error desconocido')}")

# Resto del código se mantiene igual...