import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px  # Importar plotly.express

st.title("FUSHIBALL")

def set_background_image(image_url):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url({image_url});
            background-size: cover;  /* Ajusta la imagen para cubrir todo el fondo */
            background-position: center;  /* Centra la imagen */
            background-repeat: no-repeat;  /* Evita que la imagen se repita */
            height: 100vh;  /* Altura del contenedor */
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

set_background_image('https://wallpapers.com/images/hd/uefa-champions-league-intergalactic-stadium-2mxl696eobodolq3.jpg')

# Carga de datos
ballon_dor_data = pd.read_csv('BallonDor-GoldenBall_Winners_v2.csv')
world_cup_data = pd.read_csv('FIFA - World Cup Summary.csv')
ucl_data = pd.read_csv('UCL_AllTime_Performance_Table - UCL_Alltime_Performance_Table.csv')
ucl_finals_data = pd.read_csv('UCL_Finals_1955-2023 - UCL_Finals_1955-2023.csv')

with st.sidebar:
    with st.expander("SOBRE QUÉ", expanded=False):
        st.write(('Esta aplicación se basa en la cultura del fútbol y un poco del conocimiento que se tiene hasta la fecha sobre él. '
                   'Hablándoles un poco sobre estadísticas de grandes equipos, jugadores que han logrado alzar el Balón de Oro y '
                   'países que levantaron la copa más preciada del mundo "La Copa del Mundo".'))
        
    st.sidebar.header("Opciones de Filtro")
    search_title = st.sidebar.text_input("JUGADOR, EQUIPO o PAIS")

# Botón para mostrar enlace
if st.sidebar.button('El mejor jugador del mundo👑'):
    st.sidebar.markdown('[!!LIONEL ANDRES MESSI HERE¡¡](https://www.afa.com.ar/es/posts/premios-the-best-lionel-messi-el-mejor-jugador-del-mundo)')  # Cambia el enlace aquí

def search_data(query):
    results = {
        "Balón de Oro": ballon_dor_data[ballon_dor_data.apply(lambda row: row.astype(str).str.contains(query, case=False).any(), axis=1)],
        "Copa del Mundo": world_cup_data[world_cup_data.apply(lambda row: row.astype(str).str.contains(query, case=False).any(), axis=1)],
        "UCL All-Time": ucl_data[ucl_data.apply(lambda row: row.astype(str).str.contains(query, case=False).any(), axis=1)],
        "UCL Finals": ucl_finals_data[ucl_finals_data.apply(lambda row: row.astype(str).str.contains(query, case=False).any(), axis=1)],
    }
    return results

if search_title:
    results = search_data(search_title)
    for title, result in results.items():
        if not result.empty:
            st.subheader(title)
            st.dataframe(result)

            if title == "UCL Finals":
                team_name = search_title
                
                Winners_data = result[result['Winners'].str.contains(team_name, case=False)]
                
                if not Winners_data.empty:
                    Winners_data['Year'] = Winners_data['Season'].str.split('/').str[0].str.replace('–', '-').str.strip()
                    Winners_data['Year'] = pd.to_numeric(Winners_data['Year'], errors='coerce')
                    Winners_data = Winners_data.dropna(subset=['Year'])

                    # Gráfico interactivo con Plotly
                    fig = px.line(Winners_data, x='Year', y='Score', title=f'Rendimiento de {team_name} en UCL Finals',
                                  labels={'Score': 'Goles', 'Year': 'Año'}, markers=True)
                    st.plotly_chart(fig)  # Mostrar el gráfico interactivo

# Caja de comentarios
st.subheader("Hablemos de futbol⚽")
comment = st.text_area("Deja tu comentario o pensamiento aquí:", height=100)

if st.button("Enviar Comentario"):
    if comment:
        st.success("Comentario enviado con éxito!")
    else:
        st.warning("Por favor, escribe un comentario antes de enviar.")
