from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.conf import settings

class CustomUser(AbstractUser):

    Role = (
        ('c', 'Жадвал яратувчиси'),
        ('t', 'Жадвал ва фойдаланувчи яратувчиси'),#Tanos
        ('u', 'Фойдаланувчи'),
        #a - ananimus
    )

    role = models.CharField('статус', max_length=1, choices=Role, default='u')
    created_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_created_user', null=True, blank=True)