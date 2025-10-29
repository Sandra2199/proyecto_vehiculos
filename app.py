# ==============================================
# Panel interactivo para el análisis de anuncios de venta de vehículos
# Autor: Sandra Quiñones
# ==============================================

import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st

# -------------------------------
# CONFIGURACIÓN INICIAL
# -------------------------------
st.set_page_config(page_title="Análisis de Vehículos en EE.UU.", layout="wide")

st.title("Panel interactivo para el análisis de anuncios de venta de vehículos")
st.markdown("""
Este analisis permite explorar un conjunto de datos de anuncios de vehículos usados en EE.UU.  
Podremos visualizar la distribución del **kilometraje**, **precios**, y la relación entre **precio y kilometraje**  según el año de fabricación o tipo de vehículo.

Usa los filtros y menús para interactuar con los datos.  
""")

# -------------------------------
# CARGA Y LIMPIEZA DE DATOS
# -------------------------------
try:
    car_data = pd.read_csv("vehicles_us.csv")
except FileNotFoundError:
    st.error("❌ No se encontró el archivo 'vehicles_us.csv'. Asegúrate de colocarlo en la carpeta del proyecto.")
    st.stop()

# Estandarizar nombres de columnas
car_data.columns = [c.strip().lower().replace(' ', '_') for c in car_data.columns]

# Convertir tipos
for col in ['price', 'odometer', 'model_year']:
    if col in car_data.columns:
        car_data[col] = pd.to_numeric(car_data[col], errors='coerce')

# Limpiar datos nulos críticos
car_data = car_data.dropna(subset=['price', 'odometer'])

# Crear bucket de año
bins = [1900, 1990, 2000, 2010, 2015, 2018, 2020, 2022, 2025]
labels = ['<1990','1990s','2000s','2010-14','2015-17','2018-19','2020-21','2022+']
car_data['year_bucket'] = pd.cut(car_data['model_year'].astype(float), bins=bins, labels=labels, include_lowest=True)

# -------------------------------
# FILTROS INTERACTIVOS
# -------------------------------
st.sidebar.header("Filtros")
selected_bucket = st.sidebar.multiselect(
    "Selecciona el rango de años de fabricación:",
    options=car_data['year_bucket'].dropna().unique(),
    default=car_data['year_bucket'].dropna().unique()
)
filtered_data = car_data[car_data['year_bucket'].isin(selected_bucket)]

# -------------------------------
# GRÁFICO 1: HISTOGRAMA DE KILOMETRAJE
# -------------------------------
# Ordenar las categorías del año (para que salgan cronológicamente)
car_data['year_bucket'] = pd.Categorical(
    car_data['year_bucket'],
    categories=['<1990', '1990s', '2000s', '2010-14', '2015-17', '2018-19', '2020-21', '2022+'],
    ordered=True
)
st.subheader("Distribución del kilometraje por año de fabricación")

fig1 = px.histogram(
    filtered_data,
    x='odometer',
    color='year_bucket',
    nbins=50,
    title='Distribución del kilometraje por año de fabricación',
    labels={'odometer':'Kilometraje', 'count':'Cantidad'},
    color_discrete_sequence=px.colors.qualitative.Pastel,
    category_orders={'year_bucket': ['<1990','1990s','2000s','2010-14','2015-17','2018-19','2020-21','2022+']}
    
)
fig1.update_layout(
    barmode='stack',
    title={'text': 'Distribución del kilometraje por año de fabricación', 'x': 0.5, 'xanchor': 'center'},
    legend_title='Año (bucket)',
    title_font=dict(size=18, family='Arial', color='black')
)
st.plotly_chart(fig1, use_container_width=True)

# -------------------------------
# GRÁFICO 2: HISTOGRAMA DE PRECIOS
# -------------------------------
st.subheader("Distribución de precios (recortado al 99%)")

fig2 = px.histogram(
    filtered_data.query("price <= price.quantile(0.99)"),
    x='price',
    nbins=50,
    title='Distribución de precios (sin valores extremos)',
    color_discrete_sequence=['#0072B2']
)
fig2.update_layout(
    title={'text': 'Distribución de precios (sin valores extremos)', 'x': 0.5, 'xanchor': 'center'},
    xaxis_title='Precio (USD)',
    yaxis_title='Cantidad de vehículos',
    title_font=dict(size=18, family='Arial', color='black')
)
st.plotly_chart(fig2, use_container_width=True)

# -------------------------------
# GRÁFICO 3: DISPERSIÓN PRECIO VS KILOMETRAJE
# -------------------------------
st.subheader("Relación entre precio y kilometraje")

# Selector de color
color_option = st.selectbox(
    "Selecciona la variable para colorear los puntos:",
    ['year_bucket', 'type', 'fuel', 'condition']
)

sample_data = filtered_data.copy()
sample_data['model_year_filled'] = sample_data['model_year'].fillna(0)

fig3 = px.scatter(
    sample_data,
    x='odometer',
    y='price',
    color=color_option,
    size='model_year_filled',
    opacity=0.7,
    hover_data=['model', 'model_year', 'fuel'],
    title=f'Relación entre precio y kilometraje según {color_option}',
    color_discrete_sequence=px.colors.qualitative.Set2,
    category_orders={'year_bucket': ['<1990','1990s','2000s','2010-14','2015-17','2018-19','2020-21','2022+']}
)
fig3.update_layout(
    title={'text': f'Relación entre precio y kilometraje según {color_option}', 'x': 0.5, 'xanchor': 'center'},
    legend_title_text=color_option,
    title_font=dict(size=18, family='Arial', color='black')
)
st.plotly_chart(fig3, use_container_width=True)

# -------------------------------
# PIE DE PÁGINA
# -------------------------------
st.markdown("---")
st.markdown(
    "<p style='text-align:center; font-size:14px;'>Desarrollado por <b>Sandra Quiñones</b> | Proyecto Bootcamp Data Analytics</p>",
    unsafe_allow_html=True
)