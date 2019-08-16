from django.db.models.signals import post_save
from django.core.serializers import serialize
from channels import Group

from collector import models
import json


def ws_connect(message):
    message.reply_channel.send({"accept": True})
    # Target list channel
    Group('url-common').add(message.reply_channel)
    # Push list on client connection
    ws_send_list()


def ws_message(message):
    # Target id from pushed list
    id = json.loads(message.content['text'])['id']
    # Subscribe client to Target's channel
    Group('url-{}'.format(id)).add(message.reply_channel)
    instance = models.Target.objects.get(id=id)

    # Format Target's fields and push to client
    post_save.send(models.Target, instance=instance, created=False)


def ws_send_list():
    """Target list broadcaster"""
    urls = serialize(
        'json', models.Target.objects.all().only('url'), fields=('url'))
    Group('url-common').send({"text": json.dumps({'urls': urls})})
