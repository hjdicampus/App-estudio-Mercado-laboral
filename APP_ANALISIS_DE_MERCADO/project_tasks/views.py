from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from user_management.permissions import ProjectManagerRequiredMixin
from .models import Project, Task
from .forms import ProjectForm, TaskForm
from django.contrib import messages

# Vistas para Proyectos
class ProjectListView(LoginRequiredMixin, ListView):
    model = Project
    template_name = 'project_tasks/project_list.html'
    context_object_name = 'projects'
    
    def get_queryset(self):
        user = self.request.user
        if user.is_admin() or user.is_project_manager():
            return Project.objects.all()
        else:
            return Project.objects.filter(members=user)

class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = Project
    template_name = 'project_tasks/project_detail.html'
    context_object_name = 'project'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = Task.objects.filter(project=self.object)
        return context

class ProjectCreateView(LoginRequiredMixin, ProjectManagerRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'project_tasks/project_form.html'
    success_url = reverse_lazy('project_list')
    
    def form_valid(self, form):
        form.instance.manager = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, "Proyecto creado exitosamente.")
        return response

class ProjectUpdateView(LoginRequiredMixin, ProjectManagerRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'project_tasks/project_form.html'
    success_url = reverse_lazy('project_list')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Proyecto actualizado exitosamente.")
        return response

class ProjectDeleteView(LoginRequiredMixin, ProjectManagerRequiredMixin, DeleteView):
    model = Project
    template_name = 'project_tasks/project_confirm_delete.html'
    success_url = reverse_lazy('project_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Proyecto eliminado exitosamente.")
        return super().delete(request, *args, **kwargs)

# Vistas para Tareas
class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'project_tasks/task_list.html'
    context_object_name = 'tasks'
    
    def get_queryset(self):
        user = self.request.user
        if user.is_admin() or user.is_project_manager():
            return Task.objects.all()
        else:
            return Task.objects.filter(assigned_to=user)

class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'project_tasks/task_detail.html'
    context_object_name = 'task'

class TaskCreateView(LoginRequiredMixin, ProjectManagerRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'project_tasks/task_form.html'
    
    def get_success_url(self):
        return reverse_lazy('project_detail', kwargs={'pk': self.object.project.id})
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, "Tarea creada exitosamente.")
        return response

class TaskUpdateView(LoginRequiredMixin, ProjectManagerRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'project_tasks/task_form.html'
    
    def get_success_url(self):
        return reverse_lazy('project_detail', kwargs={'pk': self.object.project.id})
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Tarea actualizada exitosamente.")
        return response

class TaskDeleteView(LoginRequiredMixin, ProjectManagerRequiredMixin, DeleteView):
    model = Task
    template_name = 'project_tasks/task_confirm_delete.html'
    
    def get_success_url(self):
        return reverse_lazy('project_detail', kwargs={'pk': self.object.project.id})
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Tarea eliminada exitosamente.")
        return super().delete(request, *args, **kwargs)