# streamlit_app.py
import streamlit as st
from auth import auth_ui, auth_controller
from database.supabase_client import supabase_client # Importa para asegurar inicialización
from utils import constants # Importa para tener acceso a constantes

# --- Configuración de la página ---
st.set_page_config(
    page_title="Gimnasio Policía Local Vigo",
    page_icon="👮‍♂️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Inicialización del estado de la sesión ---
if 'supabase_session' not in st.session_state:
    st.session_state.supabase_session = None
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# --- Barra lateral ---
with st.sidebar:
    st.title("👮‍♂️ Gimnasio PL Vigo")
    st.markdown("Gestión de Actividades y Usuarios")
    logout_button = auth_ui.logout_button() # Botón de logout en la sidebar

# --- Contenido principal ---
def main():
    if not st.session_state.logged_in:
        auth_ui.login_form() # Muestra el formulario de login si no está logueado
    else:
        # --- Aplicación principal para usuarios logueados ---
        st.header("Panel de Control del Gimnasio")
        st.write("Bienvenido, Monitor!")

        user = auth_controller.get_current_user()
        if user:
            st.write(f"Usuario autenticado: {user.email}")
        else:
            st.warning("No se pudo obtener la información del usuario.")

        # ---  Ejemplo básico de acceso a datos (¡reemplaza con tu lógica!) ---
        try:
            response = supabase_client.table("activities").select("*").execute()
            if response.error:
                st.error(f"Error al obtener actividades: {response.error.message}")
            else:
                activities_data = response.data
                st.subheader("Actividades Disponibles")
                st.dataframe(activities_data) # Muestra las actividades en una tabla
        except Exception as e:
            st.error(f"Error al consultar la base de datos: {e}")


if __name__ == "__main__":
    main()
