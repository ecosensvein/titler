from celery import shared_task
import logging

from collector import models
from collector.utils import fill_target


logger = logging.getLogger(__name__)


@shared_task(name='fill')
def fill_target_task(target_id):
    # This needs for be able to compare ids
    target = models.Target.objects.get(id=target_id)
    # Current task id
    task_id = fill_target_task.request.id
    # Run actual tasks only
    if target.task_id == task_id and target.to_handle:
        fill_target(target)
        logger.info('Started filling task for Target<%s> by task<%s>' %
                    (target_id, task_id))
