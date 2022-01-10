from django.contrib import admin
from django.conf import settings

from django.urls import path, include
from beautyapp import views
from django.conf.urls.static import static

admin.site.site_header = 'Elixir Beauty Spa'
admin.site.site_title = 'Elixir'
admin.site.index_title='Elixir Beauty Spa Administration'

urlpatterns = [

    path('admin/', admin.site.urls),
    path('',views.home,name="home"),
    path('beautyapp/', include('beautyapp.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('spa/dashboard/', include('spadashboard.urls')),
    path('table/',views.table),

]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
