from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from documents import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/upload/', views.upload_document, name='upload'),
    path('api/search/', views.search_documents, name='search'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
