# database/supabase_client.py
import streamlit as st
from supabase import create_client, Client

@st.cache_resource  # Cache para inicializar el cliente una sola vez
def get_supabase_client() -> Client:
    """
    Inicializa y devuelve el cliente Supabase.
    Utiliza st.secrets para obtener las credenciales de forma segura.
    """
    url: str = st.secrets["supabase_url"]
    key: str = st.secrets["supabase_anon_key"] # ¡Clave ANON para el frontend!
    return create_client(url, key)

supabase_client = get_supabase_client() # Instancia global del cliente para usar en toda la app
