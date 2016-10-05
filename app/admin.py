from django.contrib import admin
from app.models import PublicacionTesis_Comment



admin.site.register(
    PublicacionTesis_Comment,
    list_display=["id", "publicacion", "comentario", "user","create_at","estado","userProfile"],
    ordering=["-id"],
)