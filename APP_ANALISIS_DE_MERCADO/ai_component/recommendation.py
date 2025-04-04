# ai_component/recommendation.py

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from project_tasks.models import Task
from user_management.models import User
from job_market.models import Skill
import pandas as pd

class TaskRecommender:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(stop_words='english')
    
    def get_recommendations_for_user(self, user_id, max_recommendations=5):
        """Recomienda tareas para un usuario basado en sus habilidades"""
        try:
            user = User.objects.get(id=user_id)
            user_skills = list(user.skills.all().values_list('name', flat=True))
            
            if not user_skills:
                return []
            
            # Obtener tareas sin asignar
            unassigned_tasks = Task.objects.filter(assigned_to=None, status='todo')
            
            if not unassigned_tasks:
                return []
            
            # Preparar datos para vectorización
            task_data = []
            task_ids = []
            
            for task in unassigned_tasks:
                task_skills = list(task.skills_required.all().values_list('name', flat=True))
                task_text = f"{task.title} {task.description} {' '.join(task_skills)}"
                task_data.append(task_text)
                task_ids.append(task.id)
            
            user_text = ' '.join(user_skills)
            
            # Vectorizar
            all_data = task_data + [user_text]
            tfidf_matrix = self.vectorizer.fit_transform(all_data)
            
            # Calcular similitud
            cosine_similarities = cosine_similarity(tfidf_matrix[-1:], tfidf_matrix[:-1]).flatten()
            
            # Obtener índices de las tareas más similares
            similar_indices = cosine_similarities.argsort()[::-1]
            
            # Obtener las tareas recomendadas
            recommended_tasks = []
            for idx in similar_indices[:max_recommendations]:
                if cosine_similarities[idx] > 0.1:  # Umbral mínimo de similitud
                    task_id = task_ids[idx]
                    recommended_tasks.append(Task.objects.get(id=task_id))
            
            return recommended_tasks
        
        except Exception as e:
            print(f"Error en recomendaciones: {str(e)}")
            return []

class SkillPredictor:
    def train_model(self):
        """Entrena un modelo para predecir tendencias de habilidades"""
        from sklearn.linear_model import LinearRegression
        from job_market.models import MarketTrend
        import datetime
        
        # Obtener datos históricos
        end_date = datetime.date.today()
        start_date = end_date - datetime.timedelta(days=180)  # 6 meses de datos
        
        trends = MarketTrend.objects.filter(date__range=[start_date, end_date])
        
        if not trends:
            return None
        
        # Preparar datos para el modelo
        df = pd.DataFrame(list(trends.values('skill__name', 'date', 'demand_count')))
        
        # Convertir fechas a números (días desde el inicio)
        df['days'] = (df['date'] - start_date).dt.days
        
        # Agrupar por habilidad
        skills = df['skill__name'].unique()
        
        models = {}
        predictions = {}
        
        for skill in skills:
            skill_data = df[df['skill__name'] == skill]
            
            if len(skill_data) < 10:  # Necesitamos suficientes datos
                continue
            
            X = skill_data[['days']].values
            y = skill_data['demand_count'].values
            
            model = LinearRegression()
            model.fit(X, y)
            
            models[skill] = model
            
            # Predecir para los próximos 90 días
            future_days = np.array(range(df['days'].max() + 1, df['days'].max() + 91)).reshape(-1, 1)
            future_demand = model.predict(future_days)
            
            # Guardar predicciones
            future_dates = [start_date + datetime.timedelta(days=int(day)) for day in future_days.flatten()]
            predictions[skill] = list(zip(future_dates, future_demand))
        
        return predictions
