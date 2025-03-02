# Proyecto: Simulación de Lanzamiento de Dados con Flask y Docker

Este proyecto es una aplicación web desarrollada con Flask que simula el lanzamiento de dados, permitiendo visualizar probabilidades y generar gráficos de densidad. Se ejecuta dentro de un contenedor Docker para facilitar su despliegue.

## Características

- Simulación de lanzamientos de dos dados.
- Cálculo de probabilidades de obtener una suma específica.
- Gráficos interactivos generados con Plotly.
- Almacenamiento de resultados por sesión de usuario.
- Implementación con Flask y Docker.

## Requisitos

- Docker y Docker Compose instalados en el sistema.
- Python 3.9 (si se ejecuta sin Docker).

## Instalación y Ejecución

### Usando Docker

1. Clonar este repositorio:
   ```sh
   git clone https://github.com/tu-usuario/tu-repositorio.git
   cd tu-repositorio
   ```
2. Construir y ejecutar el contenedor:
   ```sh
   docker-compose up --build
   ```
3. Acceder a la aplicación en `http://localhost:5004`

### Sin Docker (Ejecutando localmente)

1. Instalar dependencias:
   ```sh
   pip install -r requirements.txt
   ```
2. Ejecutar la aplicación:
   ```sh
   python app.py
   ```
3. Acceder en `http://localhost:5000`

## Estructura del Proyecto

```plaintext
📂 proyecto
├── app.py              # Código principal de Flask
├── requirements.txt    # Dependencias de Python
├── Dockerfile          # Configuración del contenedor
├── docker-compose.yml  # Configuración de servicios Docker
├── templates/          # Archivos HTML
└── static/             # Archivos estáticos (CSS, JS, imágenes)
```

## Uso de la Aplicación

- Ingresar un nombre y número de lanzamientos para simular.
- Consultar la probabilidad de obtener una suma específica.
- Visualizar gráficos generados con los datos acumulados.
- Reiniciar los datos globales si se desea.

## Contacto

Si tienes preguntas o sugerencias, contáctame 

