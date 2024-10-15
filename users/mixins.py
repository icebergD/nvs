from django.contrib.auth import get_user_model
from django.views.generic import View

class UserStatus(View):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            User = get_user_model()
            user_data = User.objects.filter(id=request.user.id).values('role', 'first_name').first()
            m_user = user_data['role']
            m_user = 'a'#ananimus
            m_user_name = ' '
        self.m_user = m_user
        self.user_name = m_user_name
        return super().dispatch(request, *args, **kwargs)