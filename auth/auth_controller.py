# auth/auth_controller.py
import streamlit as st
from database.supabase_client import supabase_client

def login(email, password):
    """
    Intenta iniciar sesión con email y contraseña usando Supabase Auth.
    Guarda la sesión en st.session_state si es exitoso.
    """
    try:
        response = supabase_client.auth.sign_in_with_password({"email": email, "password": password})
        if response.error:
            st.error(f"Error de login: {response.error.message}")
            return False
        else:
            st.session_state.supabase_session = response.data.session # Guarda la sesión
            return True
    except Exception as e:
        st.error(f"Error inesperado durante el login: {e}")
        return False

def logout():
    """
    Cierra la sesión del usuario y limpia st.session_state.
    """
    supabase_client.auth.sign_out() # Cierra sesión en Supabase (opcional, pero buena práctica)
    st.session_state.supabase_session = None
    st.session_state.logged_in = False # Asegura que la variable de estado también se actualice

def is_logged_in():
    """
    Verifica si hay una sesión de usuario en st.session_state.
    """
    return st.session_state.get("supabase_session") is not None

def get_current_user():
    """
    Obtiene la información del usuario autenticado actual desde Supabase Auth.
    Retorna None si no hay usuario autenticado o si hay un error.
    """
    if is_logged_in():
        try:
            user_response = supabase_client.auth.get_user()
            if user_response.error:
                st.error(f"Error al obtener información del usuario: {user_response.error.message}")
                return None
            return user_response.data.user
        except Exception as e:
            st.error(f"Error al obtener información del usuario: {e}")
            return None
    return None
