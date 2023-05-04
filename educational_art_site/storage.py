import os
from urllib.parse import urljoin

from django.conf import settings
from django.core.files.storage import FileSystemStorage


class CustomStorage(FileSystemStorage):

    location = os.path.join(settings.MEDIA_ROOT, "news_content/images//")
    base_url = urljoin(settings.MEDIA_URL, "news_content/images//")