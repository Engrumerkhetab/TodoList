from django.urls import path
# from . import views
from .views import TaskList, TaskDetail, TaskCreate, TaskUpdate, TaskDelete, CustomLoginView,RegisterPage
from django.contrib.auth.views import LogoutView
urlpatterns = [
 
    # path('', views.home),
    # display the list of task
    path('', TaskList.as_view(), name='task'),
    # display the Detail of task
    path('task/<int:pk>/',TaskDetail.as_view(), name='task-detail' ),
    # create new task
    path('task-create/',TaskCreate.as_view(), name='task-create'),
    # update the taks 
    path('task-update/<int:pk>/',TaskUpdate.as_view(), name='task-update' ),
    # delete the task
    path('task-delete/<int:pk>/', TaskDelete.as_view(), name='task-delete'),
    #For Login Page
    path('login/', CustomLoginView.as_view(), name='login' ),
    # For Logout 
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    # Register new user
    path('register/', RegisterPage.as_view(), name='register'),
     
    
]
