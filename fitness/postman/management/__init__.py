from __future__ import unicode_literals
try:
    from importlib import import_module
except ImportError:
    from django.utils.importlib import import_module  # Django 1.6 / py2.6
import sys

from django import VERSION
from django.conf import settings
from django.db.models import signals
from django.utils.translation import ugettext_noop as _

name = getattr(settings, 'POSTMAN_NOTIFIER_APP', 'notification')
if name and name in settings.INSTALLED_APPS:
    name = name + '.models'
    notification = import_module(name)
    create = notification.NoticeType.create

    def create_notice_types(*args, **kwargs):
        create("postman_rejection", _("Message Rejected"), _("Your message has been rejected"))
        create("postman_message", _("Message Received"), _("You have received a message"))
        create("postman_reply", _("Reply Received"), _("You have received a reply"))

    if VERSION < (1, 7):
        signals.post_syncdb.connect(create_notice_types, sender=notification)
    else:
        signals.post_migrate.connect(create_notice_types, sender=notification)
