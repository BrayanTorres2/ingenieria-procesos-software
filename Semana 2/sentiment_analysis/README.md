# Proyecto: Análisis de Sentimientos en Cloud Run

## Descripción general

Este proyecto implementa una aplicación web para el análisis de sentimientos a partir de comentarios en texto contenidos en archivos Excel (.xlsx). La aplicación permite cargar un archivo, procesar y limpiar los comentarios, analizar su sentimiento utilizando Google Cloud Natural Language API y entregar los resultados de forma visual y descargable.

La solución está diseñada para ejecutarse de manera serverless en Google Cloud Run, con control de versiones en Bitbucket Cloud y despliegue automático mediante Cloud Build.

---

## Objetivo del proyecto

El objetivo principal es facilitar el análisis de opiniones y comentarios de usuarios de forma rápida y automatizada, permitiendo a las organizaciones:

- Analizar grandes volúmenes de texto sin procesamiento manual
- Identificar percepciones positivas, negativas y neutrales
- Obtener resultados visuales y exportables
- Apoyar la toma de decisiones basada en datos
- Integrar la solución en arquitecturas cloud modernas

---

## Funcionalidades principales

- Carga de archivos Excel (.xlsx) con una única columna de comentarios
- Validación estructural del archivo
- Limpieza y normalización avanzada del texto
- Filtrado de comentarios irrelevantes o inválidos
- Análisis de sentimientos en idioma español
- Generación de gráfico estadístico de resultados
- Exportación de resultados en formato Excel
- Ejecución serverless en Google Cloud Run

---

## Arquitectura de la solución

La solución utiliza una arquitectura desacoplada y orientada a servicios:

- Frontend renderizado mediante plantillas HTML y CSS
- Backend desarrollado en Python con Flask y Functions Framework
- Servicio de análisis de lenguaje natural de Google Cloud
- Contenerización mediante Docker
- Integración y despliegue continuo con Cloud Build
- Ejecución sobre Google Cloud Run
- Control de versiones con Bitbucket Cloud

---

## Estructura del proyecto

```
sentimientos-cloudrun/
├── app/
│   ├── main.py
│   ├── sentiment.py
│   ├── text_utils.py
│   ├── templates/
│   │   ├── index.html
│   │   └── result.html
│   └── static/
│       └── styles.css
├── requirements.txt
├── Dockerfile
├── cloudbuild.yaml
└── README.md
```


---

## Descripción de archivos

### main.py

Archivo principal de la aplicación. Gestiona las solicitudes HTTP, procesa el archivo Excel cargado por el usuario, ejecuta la lógica de limpieza y análisis de sentimientos, genera los gráficos estadísticos y construye la respuesta HTML.

### sentiment.py

Contiene la lógica encargada de interactuar con Google Cloud Natural Language API para analizar el sentimiento de cada comentario.

### text_utils.py

Incluye funciones auxiliares para la normalización del texto, eliminación de ruido, validación de contenido y filtrado de comentarios no relevantes.

### templates/

Contiene las plantillas HTML utilizadas para renderizar la interfaz web y mostrar los resultados al usuario.

### static/

Incluye los archivos CSS responsables del estilo visual de la aplicación.

---

## Flujo de ejecución

1. El usuario accede a la aplicación web publicada en Cloud Run
2. Se carga un archivo Excel con comentarios
3. El sistema valida que el archivo tenga una sola columna
4. Se limpian y normalizan los comentarios
5. Se filtran textos inválidos o irrelevantes
6. Se analiza el sentimiento de cada comentario
7. Se calculan métricas y porcentajes
8. Se genera un gráfico estadístico
9. Se muestran los resultados y se habilita la descarga del Excel

---

## Requisitos técnicos

- Python 3.11
- Docker
- Cuenta activa en Google Cloud Platform
- Google Cloud Natural Language API habilitada
- Cloud Build habilitado
- Repositorio en Bitbucket Cloud

---

## Dependencias del proyecto

Las dependencias se gestionan mediante el archivo `requirements.txt`:

functions-framework==3.*
flask
pandas
matplotlib
openpyxl
google-cloud-language


---

## Contenerización con Docker

El proyecto se ejecuta dentro de un contenedor Docker optimizado para Cloud Run.

FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ .

ENV PORT=8080

CMD ["functions-framework", "--target=analizar_estados", "--port=8080"]


---

## Integración continua y despliegue con Cloud Build

El archivo `cloudbuild.yaml` define el proceso automático de construcción y despliegue de la aplicación en Cloud Run cada vez que se realiza un push al repositorio.

steps:

name: gcr.io/cloud-builders/docker
args: ["build", "-t", "gcr.io/$PROJECT_ID/sentimientos", "."]

name: gcr.io/cloud-builders/docker
args: ["push", "gcr.io/$PROJECT_ID/sentimientos"]

name: gcr.io/google.com/cloudsdktool/cloud-sdk
args:
[
"gcloud", "run", "deploy", "sentimientos",
"--image", "gcr.io/$PROJECT_ID/sentimientos",
"--region", "us-central1",
"--platform", "managed",
"--allow-unauthenticated"
]


---

## Control de versiones y despliegue

El proyecto se versiona en Bitbucket Cloud. Cada push a la rama principal dispara automáticamente el pipeline de Cloud Build, que construye la imagen Docker y despliega la nueva versión en Cloud Run.

---

## Seguridad y buenas prácticas

- Uso de Service Accounts para autenticación con Google Cloud
- Credenciales gestionadas por el entorno de Cloud Run
- Separación de responsabilidades entre capas
- Validación estricta de archivos de entrada
- Uso de contenedores livianos para reducir tiempos de arranque

---

## Casos de uso

- Análisis de encuestas de satisfacción
- Evaluación de comentarios de clientes
- Monitoreo de percepción de servicios
- Procesamiento de feedback interno o externo

---

## Mantenimiento y escalabilidad

La aplicación es completamente escalable de forma automática gracias a Cloud Run. No requiere gestión de servidores y se adapta a la carga de usuarios sin intervención manual.

---





