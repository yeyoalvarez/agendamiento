from datetime import datetime
from uuid import uuid4

from django.db import models


def gen_uuid() -> str:
    timestamp = hex(int(datetime.utcnow().timestamp() * 1000000))[2:]
    uid = str(uuid4())
    return f"{timestamp[:8]}-{timestamp[8:-1]}-{uid[14:]}"


class UuidAsPkModel(models.Model):
    id = models.UUIDField(default=gen_uuid, editable=False, primary_key=True)

    class Meta:
        abstract = True


class TimestampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
