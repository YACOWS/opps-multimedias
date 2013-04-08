
from django.db.models import Q
from django.utils import timezone

from celery import task
from djcelery.models import TaskMeta


@task
def upload_video(videohost):
    video = videohost.video
    video_info = videohost.api.upload(video.video_file.path, video.title,
                                      video.headline, [])#video.tags)
    videohost.host_id = video_info['id']
    videohost.celery_task = TaskMeta.objects.get(task_id=upload_video.request.id)
    videohost.save()


@task.periodic_task(run_every=timezone.timedelta(minutes=5))
def update_videohost():
    q = Q(status='SUCCESS', videohost__isnull=False)
    error_without_reason = Q(videohost__status='error',
                             videohost__status_message__isnull=True)
    no_url = Q(videohost__url__isnull=True)
    q &= no_url | error_without_reason
    tasks = TaskMeta.objects.filter(q)

    for task in tasks:
        task.videohost.update()