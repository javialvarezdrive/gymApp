# pages/gym_booking.py
import streamlit as st
from database.supabase_client import supabase_client
from utils.constants import TIME_SLOTS
import pandas as pd # Importamos pandas para formatear la tabla de reservas

st.set_page_config(page_title="Reservas del Gimnasio", page_icon="🗓️")

# --- Verificar si el usuario está logueado ---
if 'supabase_session' not in st.session_state or not st.session_state.supabase_session:
    st.error("Debes iniciar sesión para acceder a esta página.")
    st.stop()

st.title("🗓️ Reservas del Gimnasio")

# --- Funciones para obtener datos desde Supabase ---
@st.cache_data(ttl=60)
def get_activities_from_supabase():
    """Obtiene todas las actividades para el selector."""
    response = supabase_client.table("activities").select("id, name").execute()
    return response.data if not response.error else []

@st.cache_data(ttl=60)
def get_monitors_from_supabase():
    """Obtiene todos los monitores (agentes con is_monitor=True) para el selector."""
    response = supabase_client.table("agents").select("id, name, surname").eq("is_monitor", True).execute()
    return response.data if not response.error else []

@st.cache_data(ttl=60)
def get_gym_reservations_from_supabase():
    """Obtiene todas las reservas de gimnasio para mostrar en la tabla."""
    response = supabase_client.table("gym_reservations").select(
        "id, reservation_date, time_slot, notes, activities(name), agents(name, surname)"
    ).execute()
    return response.data if not response.error else []

# --- Mostrar reservas existentes ---
st.subheader("Reservas de Gimnasio Existentes")
reservations = get_gym_reservations_from_supabase()
if reservations:
    # Formatear los datos para pandas DataFrame para mejor visualización
    df_reservations = pd.DataFrame(reservations)
    df_reservations.rename(columns={
        'reservation_date': 'Fecha',
        'time_slot': 'Turno',
        'notes': 'Notas',
        'activities': 'Actividad',
        'agents': 'Monitor'
    }, inplace=True)
    # Extraer nombre de actividad y nombre completo del monitor de los diccionarios anidados
    df_reservations['Actividad'] = df_reservations['Actividad'].apply(lambda x: x['name'])
    df_reservations['Monitor'] = df_reservations['Monitor'].apply(lambda x: f"{x['name']} {x['surname']}")
    df_reservations = df_reservations[['Fecha', 'Turno', 'Actividad', 'Monitor', 'Notas']] # Reordenar columnas
    st.dataframe(df_reservations, hide_index=True)
else:
    st.info("No hay reservas de gimnasio registradas aún.")

st.markdown("---")

# --- Formulario para crear una nueva reserva ---
st.subheader("Crear Nueva Reserva de Gimnasio")
with st.form("create_reservation_form"):
    activity_options = get_activities_from_supabase()
    monitor_options = get_monitors_from_supabase()

    if not activity_options or not monitor_options:
        st.error("No hay actividades o monitores disponibles. Regístrelos primero en sus respectivas páginas.")
        st.stop() # Detener si no hay actividades o monitores

    col1, col2 = st.columns(2)

    with col1:
        activity_id = st.selectbox("Actividad", options=activity_options, format_func=lambda x: x['name'], help="Actividad a realizar", key="activity_selector", required=True)
        monitor_id = st.selectbox("Monitor", options=monitor_options, format_func=lambda x: f"{x['name']} {x['surname']}", help="Monitor que imparte la actividad", key="monitor_selector", required=True)
        reservation_date = st.date_input("Fecha de la Reserva", help="Fecha para la reserva del gimnasio", required=True)

    with col2:
        time_slot = st.selectbox("Turno", options=TIME_SLOTS, help="Turno de la reserva", required=True)
        notes = st.text_area("Notas (Opcional)", help="Notas adicionales para la reserva", height=80)

    submit_button = st.form_submit_button("Crear Reserva")

    if submit_button:
        try:
            # Insertar la nueva reserva en la tabla 'gym_reservations'
            new_reservation_data = {
                "activity_id": activity_id['id'],
                "monitor_id": monitor_id['id'],
                "reservation_date": reservation_date.strftime("%Y-%m-%d"), # Formatear fecha a YYYY-MM-DD para Supabase
                "time_slot": time_slot,
                "notes": notes if notes else None,
            }
            response = supabase_client.table("gym_reservations").insert(new_reservation_data).execute()
            if response.error:
                st.error(f"Error al crear reserva: {response.error.message}")
            else:
                st.success("Reserva creada correctamente!")
                st.cache_data.clear() # Limpiar cache para recargar reservas
                st.rerun() # Recargar para mostrar la nueva reserva
        except Exception as e:
            st.error(f"Error inesperado al crear reserva: {e}")
