from rest_framework import viewsets
from .models import TelegramUser

from .serializers import TelegramUserSerializer

class TelegramUserViewSet(viewsets.ModelViewSet):
    queryset = TelegramUser.objects.all().order_by('-date_joined')
    serializer_class = TelegramUserSerializer
