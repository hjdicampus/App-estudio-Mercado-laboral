# Documentación Técnica

## Arquitectura del Sistema
- **Web:** Aplicación Django con 5 apps modulares (user_management, project_tasks, job_market, ai_component, external_integration).
- **Escritorio:** Aplicación PyQt5 con CRUD conectado a PostgreSQL.
- **Base de Datos:** PostgreSQL con esquema relacional.

## Diagrama ER
(Incluye un diagrama generado con Draw.io mostrando relaciones entre User, Project, Task, JobOffer, Skill, etc.)

## Componentes Modulares
- **user_management:** Autenticación y roles.
- **project_tasks:** Gestión de proyectos y tareas.
- **job_market:** Análisis del mercado laboral.
- **ai_component:** Recomendaciones y predicciones.
- **external_integration:** Scraping de datos.

## Modelo de IA
- **TaskRecommender:** Usa TF-IDF y similitud de coseno para recomendar tareas.
- **SkillPredictor:** Regresión lineal para predecir demanda de habilidades.

## Instalación
```bash
python -m venv venv
source venv/bin/activate  # o venv\Scripts\activate en Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
python desktop_app.py