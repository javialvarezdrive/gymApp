# auth/auth_ui.py
import streamlit as st
from auth.auth_controller import login, logout

def login_form():
    """
    Muestra el formulario de login.
    Retorna True si el login fue exitoso, False si no.
    """
    if not st.session_state.logged_in:
        with st.form("login_form"):
            st.subheader("Login de Monitores")
            email = st.text_input("Email")
            password = st.text_input("Contraseña", type="password")
            submitted = st.form_submit_button("Iniciar Sesión")

            if submitted:
                if login(email, password): # Llama a la función de login del controlador
                    st.success("Login exitoso!")
                    st.session_state.logged_in = True # Actualiza la variable de estado
                    st.rerun() # Recarga la app para mostrar contenido autenticado
                    return True
                else:
                    return False # Login fallido (el error ya se muestra en auth_controller)
    return False # No se intentó el login o ya estaba logueado

def logout_button():
    """
    Muestra un botón de logout en la sidebar.
    """
    if st.session_state.logged_in:
        if st.sidebar.button("Cerrar Sesión"):
            logout() # Llama a la función de logout del controlador
            st.session_state.logged_in = False # Actualiza la variable de estado
            st.rerun() # Recarga la app para volver a la pantalla de login
