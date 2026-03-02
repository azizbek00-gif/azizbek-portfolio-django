from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import About, Project, Contact
from .serializers import AboutSerializer, ProjectSerializer, ContactSerializer
from .telegram_bot import send_notification  # Telegram bot ulandi

class AboutViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = About.objects.all()
    serializer_class = AboutSerializer

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    
    def get_queryset(self):
        queryset = Project.objects.all()
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category=category)
        return queryset

@api_view(['POST'])
@csrf_exempt
def contact_submit(request):
    """Kontakt formani qabul qilish"""
    serializer = ContactSerializer(data=request.data)
    
    if serializer.is_valid():
        # Ma'lumotlarni bazaga saqlash
        contact = serializer.save()
        
        # Telegram'ga xabar yuborish
        try:
            result = send_notification(
                name=contact.name,
                email=contact.email,
                message_text=contact.message
            )
            if result:
                print("✅ Telegram xabar yuborildi")
            else:
                print("⚠️ Telegram xabar yuborilmadi")
        except Exception as e:
            print(f"❌ Telegram xatolik: {e}")
        
        return Response({
            'status': 'success',
            'message': 'Xabaringiz qabul qilindi va Telegramga yuborildi!'
        }, status=status.HTTP_201_CREATED)
    
    return Response({
        'status': 'error',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)
