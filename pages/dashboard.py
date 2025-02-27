# pages/dashboard.py
import streamlit as st
from database.supabase_client import supabase_client

st.set_page_config(page_title="Panel de Control", page_icon="📊")

# --- Verificar si el usuario está logueado ---
if 'supabase_session' not in st.session_state or not st.session_state.supabase_session:
    st.error("Debes iniciar sesión para acceder a esta página.")
    st.stop()

st.title("📊 Panel de Control del Gimnasio")

# --- Obtener información del usuario autenticado ---
user = st.session_state.supabase_session.user
if user:
    st.write(f"¡Bienvenido/a, **{user.email}**!") # Saludo personalizado con el email del usuario
else:
    st.warning("No se pudo obtener la información del usuario.")

st.markdown("---")

# --- Métricas clave (Ejemplo: conteo de actividades y agentes) ---
col1, col2 = st.columns(2)

with col1:
    activities_count = supabase_client.table("activities").select("*", count="exact").execute().count
    st.metric(label="Actividades Registradas", value=activities_count)

with col2:
    agents_count = supabase_client.table("agents").select("*", count="exact").execute().count
    st.metric(label="Agentes Registrados", value=agents_count)

st.markdown("---")

# --- Últimas Reservas de Gimnasio (Ejemplo) ---
st.subheader("Últimas Reservas de Gimnasio")
try:
    response = supabase_client.table("gym_reservations").select(
        "id, reservation_date, time_slot, activities(name), agents(name, surname)", order_by="created_at", ascending=False, limit=5 # Ordenar por fecha de creación descendente y limitar a 5
    ).execute()
    reservations = response.data
    if reservations:
        import pandas as pd # Importar pandas aquí para no cargarlo al inicio si no es necesario
        df_reservations = pd.DataFrame(reservations)
        df_reservations.rename(columns={
            'reservation_date': 'Fecha',
            'time_slot': 'Turno',
            'activities': 'Actividad',
            'agents': 'Monitor'
        }, inplace=True)
        df_reservations['Actividad'] = df_reservations['Actividad'].apply(lambda x: x['name'])
        df_reservations['Monitor'] = df_reservations['Monitor'].apply(lambda x: f"{x['name']} {x['surname']}")
        df_reservations = df_reservations[['Fecha', 'Turno', 'Actividad', 'Monitor']]
        st.dataframe(df_reservations, hide_index=True)
    else:
        st.info("No hay reservas de gimnasio recientes.")
except Exception as e:
    st.error(f"Error al obtener las últimas reservas: {e}")

st.markdown("---")

# --- Enlaces rápidos a otras páginas ---
st.subheader("Acceso Rápido")
col3, col4, col5 = st.columns(3) # Dividir en 3 columnas para los enlaces

with col3:
    if st.button("Gestionar Actividades", use_container_width=True):
        st.switch_page("pages/activities.py") # Navegación a la página de actividades

with col4:
    if st.button("Gestionar Agentes", use_container_width=True):
        st.switch_page("pages/agents.py") # Navegación a la página de agentes

with col5:
    if st.button("Reservar Gimnasio", use_container_width=True):
        st.switch_page("pages/gym_booking.py") # Navegación a la página de reservas
