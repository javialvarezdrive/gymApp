# pages/agents.py
import streamlit as st
from database.supabase_client import supabase_client
from utils.constants import SECTIONS_LIST, GROUPS_LIST

st.set_page_config(page_title="Gestión de Agentes", page_icon="👮")

# --- Verificar si el usuario está logueado ---
if 'supabase_session' not in st.session_state or not st.session_state.supabase_session:
    st.error("Debes iniciar sesión para acceder a esta página.")
    st.stop()

st.title("👮 Gestión de Agentes")

# --- Función para obtener los agentes desde Supabase ---
@st.cache_data(ttl=60)
def get_agents_from_supabase():
    """
    Obtiene todos los agentes de la tabla 'agents' desde Supabase.
    Retorna una lista de diccionarios con la información de los agentes.
    """
    try:
        response = supabase_client.table("agents").select("*").execute()
        if response.error:
            st.error(f"Error al obtener agentes: {response.error.message}")
            return []
        return response.data
    except Exception as e:
        st.error(f"Error inesperado al obtener agentes: {e}")
        return []

# --- Mostrar agentes existentes ---
st.subheader("Agentes Registrados")
agents = get_agents_from_supabase()
if agents:
    st.dataframe(agents, hide_index=True)
else:
    st.info("No hay agentes registrados aún.")

st.markdown("---")

# --- Formulario para registrar un nuevo agente ---
st.subheader("Registrar Nuevo Agente")
with st.form("register_agent_form"):
    col1, col2 = st.columns(2) # Dividir el formulario en 2 columnas para mejor layout

    with col1:
        agent_nip = st.text_input("NIP (6 dígitos)", max_chars=6, min_chars=6, required=True, help="Número de Identificación Profesional (6 dígitos)")
        agent_name = st.text_input("Nombre", required=True)
        agent_surname = st.text_input("Apellidos", required=True)
        agent_section = st.selectbox("Sección", options=[""] + SECTIONS_LIST, index=0, help="Sección a la que pertenece el agente (opcional)") # "" para opción vacía inicial
        agent_group = st.selectbox("Grupo", options=[""] + GROUPS_LIST, index=0, help="Grupo del agente (opcional)") # "" para opción vacía inicial

    with col2:
        agent_email = st.text_input("Email", type="email", help="Email del agente (opcional)")
        agent_phone = st.text_input("Teléfono", help="Número de teléfono del agente (opcional)")
        is_monitor = st.checkbox("¿Es Monitor?", value=False, help="Marcar si este agente también es monitor")

    submit_button = st.form_submit_button("Registrar Agente")

    if submit_button:
        if agent_nip and agent_name and agent_surname: # NIP, Nombre y Apellidos son obligatorios
            try:
                # Insertar el nuevo agente en la tabla 'agents'
                new_agent_data = {
                    "nip": agent_nip,
                    "name": agent_name,
                    "surname": agent_surname,
                    "section": agent_section if agent_section != "" else None, # Enviar None si está vacío para evitar string vacía en DB
                    "grupo": agent_group if agent_group != "" else None,     # Enviar None si está vacío
                    "email": agent_email if agent_email else None,          # Enviar None si está vacío
                    "phone": agent_phone if agent_phone else None,          # Enviar None si está vacío
                    "is_monitor": is_monitor
                }
                response = supabase_client.table("agents").insert(new_agent_data).execute()
                if response.error:
                    st.error(f"Error al registrar agente: {response.error.message}")
                else:
                    st.success(f"Agente '{agent_name} {agent_surname}' registrado correctamente!")
                    st.cache_data.clear() # Limpiar el cache para que se recarguen los agentes
                    st.rerun() # Recargar la página para mostrar el nuevo agente en la tabla
            except Exception as e:
                st.error(f"Error inesperado al registrar agente: {e}")
        else:
            st.warning("NIP, Nombre y Apellidos son campos obligatorios.")
