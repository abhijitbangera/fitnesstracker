"""
If the default usage of the views suits you, simply use a line like
this one in your root URLconf to set up the default URLs::

    (r'^messages/', include('postman.urls', namespace='postman', app_name='postman')),

Otherwise you may customize the behavior by passing extra parameters.

Recipients Max
--------------
Views supporting the parameter are: ``WriteView``, ``ReplyView``.
Example::
    ...View.as_view(max=3), name='write'),
See also the ``POSTMAN_DISALLOW_MULTIRECIPIENTS`` setting

User filter
-----------
Views supporting a user filter are: ``WriteView``, ``ReplyView``.
Example::
    def my_user_filter(user):
        if user.get_profile().is_absent:
            return "is away"
        return None
    ...
    ...View.as_view(user_filter=my_user_filter), name='write'),

function interface:
In: a User instance
Out: None, False, '', 'a reason', or ValidationError

Exchange filter
---------------
Views supporting an exchange filter are: ``WriteView``, ``ReplyView``.
Example::
    def my_exchange_filter(sender, recipient, recipients_list):
        if recipient.relationships.exists(sender, RelationshipStatus.objects.blocking()):
            return "has blacklisted you"
        return None
    ...
    ...View.as_view(exchange_filter=my_exchange_filter), name='write'),

function interface:
In:
    ``sender``: a User instance
    ``recipient``: a User instance
    ``recipients_list``: the full list of recipients or None
Out: None, False, '', 'a reason', or ValidationError

Auto-complete field
-------------------
Views supporting an auto-complete parameter are: ``WriteView``, ``ReplyView``.
Examples::
    ...View.as_view(autocomplete_channels=(None,'anonymous_ac')), name='write'),
    ...View.as_view(autocomplete_channels='write_ac'), name='write'),
    ...View.as_view(autocomplete_channel='reply_ac'), name='reply'),

Auto moderators
---------------
Views supporting an ``auto-moderators`` parameter are: ``WriteView``, ``ReplyView``.
Example::
    def mod1(message):
        # ...
        return None
    def mod2(message):
        # ...
        return None
    mod2.default_reason = 'mod2 default reason'
    ...
    ...View.as_view(auto_moderators=(mod1, mod2)), name='write'),
    ...View.as_view(auto_moderators=mod1), name='reply'),

function interface:
In: ``message``: a Message instance
Out: rating or (rating, "reason")
    with reting: None, 0 or False, 100 or True, 1..99

Others
------
Refer to documentation.
    ...View.as_view(form_classes=(MyCustomWriteForm, MyCustomAnonymousWriteForm)), name='write'),
    ...View.as_view(form_class=MyCustomFullReplyForm), name='reply'),
    ...View.as_view(form_class=MyCustomQuickReplyForm), name='view'),
    ...View.as_view(template_name='my_custom_view.html'), name='view'),
    ...View.as_view(success_url='postman:inbox'), name='reply'),
    ...View.as_view(formatters=(format_subject, format_body)), name='reply'),
    ...View.as_view(formatters=(format_subject, format_body)), name='view'),

"""
from __future__ import unicode_literals

from django.conf.urls import url
from django.views.generic.base import RedirectView

from . import OPTIONS
from .views import (InboxView, SentView, ArchivesView, TrashView,
        WriteView, ReplyView, MessageView, ConversationView,
        ArchiveView, DeleteView, UndeleteView)


urlpatterns = [
    url(r'^inbox/(?:(?P<option>'+OPTIONS+')/)?$', InboxView.as_view(), name='inbox'),
    url(r'^sent/(?:(?P<option>'+OPTIONS+')/)?$', SentView.as_view(), name='sent'),
    url(r'^archives/(?:(?P<option>'+OPTIONS+')/)?$', ArchivesView.as_view(), name='archives'),
    url(r'^trash/(?:(?P<option>'+OPTIONS+')/)?$', TrashView.as_view(), name='trash'),
    url(r'^write/(?:(?P<recipients>[^/#]+)/)?$', WriteView.as_view(), name='write'),
    url(r'^reply/(?P<message_id>[\d]+)/$', ReplyView.as_view(), name='reply'),
    url(r'^view/(?P<message_id>[\d]+)/$', MessageView.as_view(), name='view'),
    url(r'^view/t/(?P<thread_id>[\d]+)/$', ConversationView.as_view(), name='view_conversation'),
    url(r'^archive/$', ArchiveView.as_view(), name='archive'),
    url(r'^delete/$', DeleteView.as_view(), name='delete'),
    url(r'^undelete/$', UndeleteView.as_view(), name='undelete'),
    url(r'^$', RedirectView.as_view(url='inbox/', permanent=True)),
]
