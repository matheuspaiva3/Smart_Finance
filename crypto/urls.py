from django.urls import path
from .views import Index, CreateAccount, Login, Assets

app_name = 'crypto'

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('create_account/', CreateAccount.as_view(), name='create_account'),
    path('login/', Login.as_view(), name='login'),
    path('assets/', Assets.as_view(), name='assets'),
]
