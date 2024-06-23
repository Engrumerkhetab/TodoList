from django.shortcuts import render
#For Function based views
from django.http import HttpRequest, HttpResponse
#Fom Class-based views useing ListViews(To show task list)
from django.views.generic.list import ListView
#From Class-based views using DetailView(To show the detail of task)
from django.views.generic.detail import DetailView
#To create new task , update task or delete task
from django.views.generic.edit import CreateView, UpdateView, DeleteView
#To active login button 
from django.contrib.auth.views import LoginView
#To redirect to Task list page
from django.urls import reverse_lazy 
# To require login first 
from django.contrib.auth.mixins import LoginRequiredMixin
# To register new user
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
# To redirect already register user
from django.shortcuts import redirect
# import models from models.py
from .models import Task
# Create your views here.
# def home(request):
#     return HttpResponse("Working")
class TaskList(LoginRequiredMixin, ListView):
    model = Task # it returns 'object_list' called context_object_name
    # set context_object_name as 'taks'
    context_object_name = 'task' 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # print("context====", context)
        context['task'] = context['task'].filter(user=self.request.user)
        context['count'] = context['task'].filter(complete=False).count()
        # to search from task list
        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['task'] = context['task'].filter(title__icontains = search_input)
            context['search_input'] = search_input
            # print(context['search_input'])
            # print("context====", context)
          
        return context
    
    
    
    

class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task' 
    template_name = 'todo/task.html'
    
class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    # fields = '__all__'
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('task')
    # To get user auto for form data
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)
    
    
class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    # fields = "__all__"
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('task')
    

class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task' 
    success_url = reverse_lazy('task')

class CustomLoginView(LoginView):
    template_name = 'todo/login.html'
    fields = "__all__"
    redirect_authenticated_user = False
    
    def get_success_url(self):
        return reverse_lazy('task')

class RegisterPage(FormView):
    template_name = 'todo/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('task')
    # New Register go to taks list page
    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)
    # Already register user goes to Task list when attempting to get register page
    
    def get(self, *args , **kwargs):
        if self.request.user.is_authenticated:
            return redirect('task')
        return super(RegisterPage, self).get(*args, **kwargs)
    
