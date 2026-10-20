"""
URL configuration for config project.
"""

from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

from cadastro.views import android_assetlinks


urlpatterns = [
    # Android App Links
    path(
        ".well-known/assetlinks.json",
        android_assetlinks,
        name="android_assetlinks",
    ),

    # Área administrativa
    path("admin/", admin.site.urls),

    # Todas as páginas do aplicativo Turismo de Picuí
    path("", include("cadastro.urls")),
]


# Servir arquivos estáticos e mídia em modo DEBUG
if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT,
    )

    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )