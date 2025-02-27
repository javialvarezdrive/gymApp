# pages/activities.py
import streamlit as st
from database.supabase_client import supabase_client

st.set_page_config(page_title="Gestión de Actividades", page_icon="🏋️")

# --- Verificar si el usuario está logueado ---
if 'supabase_session' not in st.session_state or not st.session_state.supabase_session:
    st.error("Debes iniciar sesión para acceder a esta página.")
    st.stop()

st.title("🏋️ Gestión de Actividades del Gimnasio")

# --- Función para obtener las actividades desde Supabase ---
@st.cache_data(ttl=60)  # Cachear por 60 segundos para no sobrecargar la DB en cada rerun
def get_activities_from_supabase():
    """
    Obtiene todas las actividades de la tabla 'activities' desde Supabase.
    Retorna una lista de diccionarios con la información de las actividades.
    """
    try:
        response = supabase_client.table("activities").select("*").execute()
        if response.error:
            st.error(f"Error al obtener actividades: {response.error.message}")
            return []
        return response.data
    except Exception as e:
        st.error(f"Error inesperado al obtener actividades: {e}")
        return []

# --- Mostrar actividades existentes ---
st.subheader("Actividades Existentes")
activities = get_activities_from_supabase()
if activities:
    st.dataframe(activities, hide_index=True) # Muestra las actividades en una tabla Streamlit
else:
    st.info("No hay actividades registradas aún.")

st.markdown("---")

# --- Formulario para añadir una nueva actividad ---
st.subheader("Añadir Nueva Actividad")
with st.form("add_activity_form"):
    new_activity_name = st.text_input("Nombre de la Actividad", help="Ej: Zumba, Yoga, etc.", max_chars=255, required=True)
    new_activity_description = st.text_area("Descripción (Opcional)", help="Descripción detallada de la actividad.", height=100)
    submit_button = st.form_submit_button("Añadir Actividad")

    if submit_button:
        if new_activity_name:
            try:
                # Insertar la nueva actividad en la tabla 'activities'
                response = supabase_client.table("activities").insert({"name": new_activity_name, "description": new_activity_description}).execute()
                if response.error:
                    st.error(f"Error al añadir actividad: {response.error.message}")
                else:
                    st.success(f"Actividad '{new_activity_name}' añadida correctamente!")
                    st.cache_data.clear() # Limpiar el cache para que se recarguen las actividades
                    st.rerun() # Recargar la página para mostrar la nueva actividad en la tabla
            except Exception as e:
                st.error(f"Error inesperado al añadir actividad: {e}")
        else:
            st.warning("El nombre de la actividad es obligatorio.")
