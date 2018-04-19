from django.urls import path
from .views import *

urlpatterns = [
    path('', main, name='main'),
    path('classrooms/', classrooms, name='classrooms'),
    path('teachers/', teachers, name='teachers'),
    path('days/', days, name='days'),
    path('createuser/', createuser, name='createuser'),
]