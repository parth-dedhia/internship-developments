from django.urls import path , include
from . import views


app_name='toDoList'

urlpatterns = [
    path('',views.toDoList,name='home'),
    path('accounts/signup/', views.signup, name='signup'),
    path('mail/',views.mailPage,name='mailPage'),
    path('mailOthers/',views.mailOthers,name='mailOthers'),
    path('mailSelf/',views.mailSelf,name='mailSelf'),
    path('addTask/',views.addTask,name='addTask'),
    path('taskCompleted/',views.taskCompleted,name='taskCompleted'),
    path('deleteCompletedTask/',views.deleteCompletedTask,name='deleteCompletedTask'),
    path('deleteAllTasks/',views.deleteAllTasks,name='deleteAllTasks'),
]
