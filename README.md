# Proyecto Vehículos - Análisis y Dashboard Interactivo

Este proyecto realiza un **análisis exploratorio de datos** de anuncios de coches en Estados Unidos y crea un **dashboard interactivo** usando Streamlit.

## Funcionalidades

- Histograma de kilometraje de los vehículos.
- Gráfico de dispersión (precio vs año / precio vs kilometraje).
- Interactividad mediante botones o checkboxes.
- Dashboard desplegado online en Streamlit Cloud.

## Tecnologías utilizadas

- Python
- pandas
- plotly-express
- Streamlit

## Cómo ejecutar el proyecto localmente

```bash
# Clonar el repositorio
git clone https://github.com/tu_usuario/proyecto_vehiculos.git
cd proyecto_vehiculos

# Crear entorno virtual
python -m venv vehicles_env
vehicles_env\Scripts\activate    # Windows
source vehicles_env/bin/activate # Mac/Linux

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar app
streamlit run app.py
