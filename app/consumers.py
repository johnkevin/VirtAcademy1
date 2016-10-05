import json
from channels import Group
from app.models import PublicacionTesis
#from .models import Liveblog

def connect_blog(message, slug):
    try:
        publicaciontesis = PublicacionTesis.objects.get(slug=slug)
    except PublicacionTesis.DoesNotExist:
        message.reply_channel.send({
            "text": json.dumps({"error": "bad_slug"}),
            "close": True,
        })
        return
    Group(publicaciontesis.group_name).add(message.reply_channel)

def disconnect_blog(message, slug):
    try:
        publicaciontesis = PublicacionTesis.objects.get(slug=slug)
    except PublicacionTesis.DoesNotExist:
        return
    Group(publicaciontesis.group_name).discard(message.reply_channel)
