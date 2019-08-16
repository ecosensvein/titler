from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from django.db import models
from channels import Group
import datetime
import json

from collector.tasks import fill_target_task
from collector.consumers import ws_send_list


class Target(models.Model):
    url = models.URLField('Url-адрес', unique=True, max_length=500)
    created_at = models.DateTimeField('Дата добавления', auto_now_add=True)
    handled_at = models.DateTimeField('Дата обработки', null=True)
    timeshift = models.DurationField(
        'До исполнения', default=datetime.timedelta(seconds=0))
    # Handle flag
    to_handle = models.BooleanField('Ожидает исполнения', default=False)
    # Parsed data
    title = models.CharField('Заголовок', blank=True, max_length=200)
    heading = models.CharField('Тег H1', blank=True, null=True, max_length=400)
    encoding = models.CharField('Кодировка', blank=True, max_length=40)
    # For celery purposes
    # Calculated datetime for execute current celery task
    shed_at = models.DateTimeField(null=True)
    # Last and actual task (others will be ignored)
    task_id = models.CharField(blank=True, null=True, max_length=40)

    def __str__(self):
        return self.url


@receiver(post_save, sender=Target)
def update_data_on_channels(sender, **kwargs):
    """
        This function is for formatting and pushing single
        Target data to client channel
    """
    # Avoiding of the save recursion
    if not kwargs.get('raw', False):
        ins = kwargs.get('instance')
        # Data for the first textarea
        model_data = {'log_area': {}, 'urls_area': {}}
        model_data['log_area']['<дата %s>: ' % ins.created_at.strftime(
            '%d.%m.%Y %H:%M:%S')] = 'Url-адрес добавлен'

        # Data for the second textarea
        if not kwargs.get('created', False):
            model_data['urls_area'].update({ins.url: ' - ',
                                            'Title ': ins.title,
                                            'H1 ': ins.heading,
                                            'Encoding ': ins.encoding})
            if ins.handled_at:
                if ins.title:
                    msg = 'Url-адрес обработан успешно'
                else:
                    msg = 'Url-адрес не обработан успешно'
                model_data['log_area']['<дата %s>:  ' % ins.handled_at.strftime(
                    '%d.%m.%Y %H:%M:%S')] = msg

        # Renew Target data on it's channel (bad idea)
        Group('url-{}'.format(ins.id)).send({"text": json.dumps(model_data)})
        # Renew Target list's channel too
        ws_send_list()

        # Create new celery task for this instance
        if ins.to_handle:
            eta = datetime.datetime.now() + ins.timeshift
            # New actual celery task
            task_id = fill_target_task.apply_async([ins.id, ], eta=eta)
            # shed_at represents eta of actual celery task
            ins.shed_at = eta
            # For comparing with old task ids inside the fired celery task
            ins.task_id = task_id
            # No save recursion
            ins.save_base(raw=True)


@receiver(post_delete, sender=Target)
def delete_data_on_channels(sender, **kwargs):
    ws_send_list()
