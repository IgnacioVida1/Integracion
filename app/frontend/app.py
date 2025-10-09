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

# Sección 2: Reportes Analíticos
st.header("📊 Reportes Analíticos")
reporte_periodo = st.selectbox(
    "Seleccionar Período para el Reporte",
    ["diario", "semanal", "mensual", "anual"],
    index=2
)

if st.button("Generar Reporte de Eficiencia"):
    with st.spinner(f"Generando reporte {reporte_periodo}..."):
        reporte = obtener_reporte_eficiencia(ms4_url, reporte_periodo)
        if reporte.get('success'):
            st.success("✅ Reporte generado correctamente")
            
            # Mostrar métricas principales
            datos = reporte.get('data', {})
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Pedidos", datos.get('total_pedidos', 0))
            with col2:
                st.metric("Pedidos Asignados", datos.get('pedidos_asignados', 0))
            with col3:
                st.metric("Pedidos Entregados", datos.get('pedidos_entregados', 0))
            with col4:
                eficiencia = datos.get('eficiencia_asignacion', 0)
                st.metric("Eficiencia Asignación", f"{eficiencia}%")
            
            # Mostrar datos completos
            with st.expander("Ver datos completos del reporte"):
                st.json(datos)
        else:
            st.error(f"❌ Error al generar reporte: {reporte.get('error', 'Error desconocido')}")

# Sección 3: Estado General del Sistema
st.header("🔍 Estado del Sistema")
if st.button("Verificar Salud de Microservicios"):
    with st.spinner("Verificando estado de todos los servicios..."):
        status, message = test_api_connection(ms4_url)
        if status:
            st.success("✅ Microservicio 4: En línea")
            
            # Aquí podrías agregar verificaciones para MS1, MS2, MS3
            st.info("""
            **Estado de los Microservicios:**
            - MS4 (Integración): ✅ En línea
            - MS1 (Productos): ⚠️ Por verificar
            - MS2 (Logística): ⚠️ Por verificar  
            - MS3 (Pedidos): ⚠️ Por verificar
            """)
        else:
            st.error("❌ Microservicio 4: Fuera de línea")

# Información de ayuda
with st.expander("ℹ️ Instrucciones de Uso"):
    st.markdown("""
    1. **Asegúrate** de que el Microservicio 4 esté corriendo en la URL especificada
    2. **Verifica la conexión** usando el botón en la barra lateral
    3. **Para probar asignación de pedidos:**
       - Ingresa un ID de pedido existente en MS3
       - El sistema verificará stock (MS1) y asignará conductor (MS2)
    4. **Para generar reportes:**
       - Selecciona el período y genera el reporte analítico
    """)

if __name__ == "__main__":
    # Limpiar resultados previos al recargar
    if 'resultado_asignacion' in st.session_state:
        del st.session_state.resultado_asignacion