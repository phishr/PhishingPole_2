from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('Phishr.urls')),
    path('admin/', admin.site.urls),
    path('dashboard/', include('Phishr.urls')),
    path('login/', include('Phishr.urls'))
]
