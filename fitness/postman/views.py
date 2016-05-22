from __future__ import unicode_literals

from django import VERSION
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
try:
    from django.contrib.sites.shortcuts import get_current_site  # Django 1.7
except ImportError:
    from django.contrib.sites.models import get_current_site
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect,render,render_to_response
from django.utils.decorators import method_decorator
from django.utils.encoding import force_text
try:
    from django.utils.six.moves.urllib.parse import urlsplit, urlunsplit  # Django 1.4.11, 1.5.5
except ImportError:
    from urlparse import urlsplit, urlunsplit
from django.utils.timezone import now
from django.utils.translation import ugettext as _, ugettext_lazy
from django.views.decorators.csrf import csrf_protect
from django.views.generic import FormView, TemplateView, View

from . import OPTION_MESSAGES
from .fields import autocompleter_app
from .forms import WriteForm, AnonymousWriteForm, QuickReplyForm, FullReplyForm
from .models import Message, get_order_by
from .utils import format_subject, format_body
import requests 
from tracker.models import userprofile_extended
from tracker.forms import userprofile_extended_goalsettings_Form,userprofile_extended_profilesettings_Form
from django.http import HttpResponseRedirect


login_required_m = method_decorator(login_required)
csrf_protect_m = method_decorator(csrf_protect)


##########
# Helpers
##########
def _get_referer(request):
    """Return the HTTP_REFERER, if existing."""
    if 'HTTP_REFERER' in request.META:
        sr = urlsplit(request.META['HTTP_REFERER'])
        return urlunsplit(('', '', sr.path, sr.query, sr.fragment))


########
# Views
########
class NamespaceMixin(object):
    """Common code to manage the namespace."""

    def render_to_response(self, context, **response_kwargs):
        if VERSION >= (1, 8):
            self.request.current_app = self.request.resolver_match.namespace
        else:
            response_kwargs['current_app'] = self.request.resolver_match.namespace
        return super(NamespaceMixin, self).render_to_response(context, **response_kwargs)


class FolderMixin(NamespaceMixin, object):
    """Code common to the folders."""
    http_method_names = ['get']

    @login_required_m
    def dispatch(self, *args, **kwargs):
        return super(FolderMixin, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        profilepic="/media/avatar.png"
        username=self.request.user
        obj=userprofile_extended.objects.filter(user_id=username)
        profilepic="/media/avatar.png"
        obj_count=obj.count()
        if obj_count>0:
            for i in obj:
                goal_id=i.image
                if goal_id:
                    profilepic=i.image.url

        context = super(FolderMixin, self).get_context_data(**kwargs)
        params = {}
        option = kwargs.get('option')
        if option:
            params['option'] = option
        order_by = get_order_by(self.request.GET)
        if order_by:
            params['order_by'] = order_by
        msgs = getattr(Message.objects, self.folder_name)(self.request.user, **params)
        viewname = 'postman:' + self.view_name
        current_instance = self.request.resolver_match.namespace
        context.update({
            'pm_messages': msgs,  # avoid 'messages', already used by contrib.messages
            'by_conversation': option is None,
            'by_message': option == OPTION_MESSAGES,
            'by_conversation_url': reverse(viewname, current_app=current_instance),
            'by_message_url': reverse(viewname, args=[OPTION_MESSAGES], current_app=current_instance),
            'current_url': self.request.get_full_path(),
            'gets': self.request.GET,  # useful to postman_order_by template tag
            'profilepic':profilepic,

        })
        return context


class InboxView(FolderMixin, TemplateView):
    """
    Display the list of received messages for the current user.

    Optional URLconf name-based argument:
        ``option``: display option:
            OPTION_MESSAGES to view all messages
            default to None to view only the last message for each conversation
    Optional URLconf configuration attribute:
        ``template_name``: the name of the template to use

    """
    # for FolderMixin:
    folder_name = 'inbox'
    view_name = 'inbox'
    # for TemplateView:
    template_name = 'postman/inbox.html'


class SentView(FolderMixin, TemplateView):
    """
    Display the list of sent messages for the current user.

    Optional arguments and attributes: refer to InboxView.

    """
    # for FolderMixin:
    folder_name = 'sent'
    view_name = 'sent'
    # for TemplateView:
    template_name = 'postman/sent.html'


class ArchivesView(FolderMixin, TemplateView):
    """
    Display the list of archived messages for the current user.

    Optional arguments and attributes: refer to InboxView.

    """
    # for FolderMixin:
    folder_name = 'archives'
    view_name = 'archives'
    # for TemplateView:
    template_name = 'postman/archives.html'


class TrashView(FolderMixin, TemplateView):
    """
    Display the list of deleted messages for the current user.

    Optional arguments and attributes: refer to InboxView.

    """
    # for FolderMixin:
    folder_name = 'trash'
    view_name = 'trash'
    # for TemplateView:
    template_name = 'postman/trash.html'


class ComposeMixin(NamespaceMixin, object):
    """
    Code common to the write and reply views.

    Optional attributes:
        ``success_url``: where to redirect to after a successful POST
        ``user_filter``: a filter for recipients
        ``exchange_filter``: a filter for exchanges between a sender and a recipient
        ``max``: an upper limit for the recipients number
        ``auto_moderators``: a list of auto-moderation functions

    """
    http_method_names = ['get', 'post']
    success_url = None
    user_filter = None
    exchange_filter = None
    max = None
    auto_moderators = []

    def get_form_kwargs(self):
        kwargs = super(ComposeMixin, self).get_form_kwargs()
        if self.request.method == 'POST':
            kwargs.update({
                'sender': self.request.user,
                'user_filter': self.user_filter,
                'exchange_filter': self.exchange_filter,
                'max': self.max,
                'site': get_current_site(self.request),
            })
        return kwargs

    def get_success_url(self):
        return self.request.GET.get('next') or self.success_url or _get_referer(self.request) or 'postman:inbox'

    def form_valid(self, form):
        params = {'auto_moderators': self.auto_moderators}
        if hasattr(self, 'parent'):  # only in the ReplyView case
            params['parent'] = self.parent
        is_successful = form.save(**params)
        if is_successful:
            messages.success(self.request, _("Message successfully sent."), fail_silently=True)
        else:
            messages.warning(self.request, _("Message rejected for at least one recipient."), fail_silently=True)
        return redirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        username=self.request.user
        obj=userprofile_extended.objects.filter(user_id=username)
        profilepic="/media/avatar.png"
        trainerprofilepic="/media/avatar.png"
        obj_count=obj.count()
        trainer=''
        nutritionist=''
        supplimentexpert=''
        contact=''
        trainerprofilepic="/media/avatar.png"
        nutritionistprofilepic="/media/avatar.png"
        supplimentexpertprofilepic="/media/avatar.png"
        contactprofilepic="/media/avatar.png"
        trainer_about=''
        trainer_age='Not Set' 
        trainer_gender='Not Set'
        nutritionist_about=''
        nutritionist_age='Not Set' 
        nutritionist_gender='Not Set'
        supplimentexpert_about=''
        supplimentexpert_age='Not Set' 
        supplimentexpert_gender='Not Set'
        contact_about=''
        contact_age='Not Set' 
        contact_gender='Not Set'
        User = get_user_model()
        obj=userprofile_extended.objects.filter(user_id=username)

        obj_count=obj.count()
        if obj_count>0:
            for i in obj:
                goal_id=i.image
                if goal_id:
                    profilepic=i.image.url


        print("=================")
        print(obj_count) 
        if obj_count==0:
            
            form=userprofile_extended_goalsettings_Form()
            messages.add_message(self.request,messages.SUCCESS, "Please update your workout goal. Based on your goal the system would allocate appropriate instructors to your profile.")
            print("i m here")
            template_name='user_goal_settings.html'
            context={
                     'profilepic':profilepic,
                     'username_original':username,
                    'username':str(username).title(), 
                     'trainerprofilepic':trainerprofilepic,
                    'nutritionistprofilepic':nutritionistprofilepic,
                    'supplimentexpertprofilepic':supplimentexpertprofilepic,
                    'contactprofilepic':contactprofilepic,
                    }
            print(context)
            return context
            # return render(self.request, "user_goal_settings.html",context) 
        if obj_count>0:
            for i in obj:
                goal_id=i.goal

                print(goal_id)
                print("=================")
                print(i.image)
                if goal_id==None:
                    form=userprofile_extended_goalsettings_Form()
                    messages.add_message(self.request,messages.SUCCESS, "Please update your workout goal below. Based on your goal the system would allocate appropriate instructors to your profile.")
                    context={
                             'profilepic':profilepic,
                             'username_original':username, 
                              'username':str(username).title(),
                              }
                    return context
                
                if i.image:
                    profilepic=i.image.url
                trainer=i.trainer
                nutritionist=i.nutritionist
                supplimentexpert=i.supplimentexpert
                contact=i.contact
        if (trainer):
            messages.add_message(self.request,messages.SUCCESS, "Please select your Recipient from the below list of profiles.")
            t = User.objects.get(username=trainer)
            print(t)
            trainerobj=userprofile_extended.objects.filter(user_id=t)
            
            trainerobj_count=trainerobj.count()
            if trainerobj_count>0:
                for i in trainerobj:
                    trainerprofilepic=i.image.url
                    trainer_about=i.about
                    trainer_age=i.age 
                    trainer_gender=i.gender
            
            n = User.objects.get(username=nutritionist)
            nutritionistobj=userprofile_extended.objects.filter(user_id=n)
            
            nutritionistobj_count=nutritionistobj.count()
            if nutritionistobj_count>0:
                for i in nutritionistobj:
                    nutritionistprofilepic=i.image.url
                    nutritionist_about=i.about
                    nutritionist_age=i.age 
                    nutritionist_gender=i.gender

            s=User.objects.get(username=supplimentexpert)
            supplimentexpertobj=userprofile_extended.objects.filter(user_id=s)
            
            supplimentexpertobj_count=supplimentexpertobj.count()
            if supplimentexpertobj_count>0:
                for i in supplimentexpertobj:
                    supplimentexpertprofilepic=i.image.url
                    supplimentexpert_about=i.about
                    supplimentexpert_age=i.age 
                    supplimentexpert_gender=i.gender



            c=User.objects.get(username=contact)
            contactobj=userprofile_extended.objects.filter(user_id=c)
            
            contactobj_count=contactobj.count()
            if contactobj_count>0:
                for i in contactobj:
                    contactprofilepic=i.image.url
                    contact_about=i.about
                    contact_age=i.age 
                    contact_gender=i.gender





        context = super(ComposeMixin, self).get_context_data(**kwargs)
        context.update({
            'autocompleter_app': autocompleter_app,
            'next_url': self.request.GET.get('next') or _get_referer(self.request),
            'username':str(username).title(),
            'username_original':username,
            'profilepic':profilepic,
            'trainer':trainer,
            'trainerprofilepic':trainerprofilepic,
            'nutritionist':nutritionist,
            'nutritionistprofilepic':nutritionistprofilepic,
            'supplimentexpert':'supplimentexpert',
            'supplimentexpertprofilepic':supplimentexpertprofilepic,
            'contact':contact,
            'contactprofilepic':contactprofilepic,
            'trainer_about':trainer_about,
            'trainer_age':trainer_age,
            'trainer_gender':trainer_gender,
            'nutritionist_about':nutritionist_about,
            'nutritionist_age':nutritionist_age,
            'nutritionist_gender':nutritionist_gender,
            'supplimentexpert_about':supplimentexpert_about,
            'supplimentexpert_age':supplimentexpert_age,
            'supplimentexpert_gender':supplimentexpert_gender,
            'contact_about':contact_about,
            'contact_age':contact_age,
            'contact_gender':contact_gender,

        })
        return context


class WriteView(ComposeMixin, FormView):
    """
    Display a form to compose a message.

    Optional URLconf name-based argument:
        ``recipients``: a colon-separated list of usernames
    Optional attributes:
        ``form_classes``: a 2-tuple of form classes
        ``autocomplete_channels``: a channel name or a 2-tuple of names
        ``template_name``: the name of the template to use
        + those of ComposeMixin

    """
    form_classes = (WriteForm, AnonymousWriteForm)
    autocomplete_channels = None
    template_name = 'postman/write.html'

    @csrf_protect_m
    def dispatch(self, *args, **kwargs):
        if getattr(settings, 'POSTMAN_DISALLOW_ANONYMOUS', True):
            return login_required(super(WriteView, self).dispatch)(*args, **kwargs)
        return super(WriteView, self).dispatch(*args, **kwargs)

    def get_form_class(self):
        return self.form_classes[0] if self.request.user.is_authenticated() else self.form_classes[1]

    def get_initial(self):
        initial = super(WriteView, self).get_initial()
        if self.request.method == 'GET':
            initial.update(self.request.GET.items())  # allow optional initializations by query string
            recipients = self.kwargs.get('recipients')
            if recipients:
                # order_by() is not mandatory, but: a) it doesn't hurt; b) it eases the test suite
                # and anyway the original ordering cannot be respected.
                user_model = get_user_model()
                name_user_as = getattr(settings, 'POSTMAN_NAME_USER_AS', user_model.USERNAME_FIELD)
                usernames = list(user_model.objects.values_list(name_user_as, flat=True).filter(
                    is_active=True,
                    **{'{0}__in'.format(name_user_as): [r.strip() for r in recipients.split(':') if r and not r.isspace()]}
                ).order_by(name_user_as))
                if usernames:
                    initial['recipients'] = ', '.join(map(force_text, usernames))
        return initial

    def get_form_kwargs(self):

        kwargs = super(WriteView, self).get_form_kwargs()
        if isinstance(self.autocomplete_channels, tuple) and len(self.autocomplete_channels) == 2:
            channel = self.autocomplete_channels[self.request.user.is_anonymous()]
        else:
            channel = self.autocomplete_channels
        kwargs['channel'] = channel

        return kwargs


class ReplyView(ComposeMixin, FormView):
    """
    Display a form to compose a reply.

    Optional attributes:
        ``form_class``: the form class to use
        ``formatters``: a 2-tuple of functions to prefill the subject and body fields
        ``autocomplete_channel``: a channel name
        ``template_name``: the name of the template to use
        + those of ComposeMixin

    """
    form_class = FullReplyForm
    formatters = (format_subject, format_body)
    autocomplete_channel = None
    template_name = 'postman/reply.html'

    @csrf_protect_m
    @login_required_m
    def dispatch(self, request, message_id, *args, **kwargs):
        perms = Message.objects.perms(request.user)
        self.parent = get_object_or_404(Message, perms, pk=message_id)
        return super(ReplyView, self).dispatch(request,*args, **kwargs)

    def get_initial(self):
        self.initial = self.parent.quote(*self.formatters)  # will also be partially used in get_form_kwargs()
        if self.request.method == 'GET':
            self.initial.update(self.request.GET.items())  # allow overwriting of the defaults by query string
        return self.initial

    def get_form_kwargs(self):
        kwargs = super(ReplyView, self).get_form_kwargs()
        kwargs['channel'] = self.autocomplete_channel
        if self.request.method == 'POST':
            if 'subject' not in kwargs['data']:  # case of the quick reply form
                post = kwargs['data'].copy()  # self.request.POST is immutable
                post['subject'] = self.initial['subject']
                kwargs['data'] = post
            kwargs['recipient'] = self.parent.sender or self.parent.email
        return kwargs

    def get_context_data(self, **kwargs):
        profilepic="/media/avatar.png"
        username=self.request.user
        obj=userprofile_extended.objects.filter(user_id=username)
        profilepic="/media/avatar.png"
        obj_count=obj.count()
        if obj_count>0:
            for i in obj:
                goal_id=i.image
                if goal_id:
                    profilepic=i.image.url
        context = super(ReplyView, self).get_context_data(**kwargs)
        context['recipient'] = self.parent.obfuscated_sender
        context.update({'profilepic':profilepic,})
        return context


class DisplayMixin(NamespaceMixin, object):
    """
    Code common to the by-message and by-conversation views.

    Optional attributes:
        ``form_class``: the form class to use
        ``formatters``: a 2-tuple of functions to prefill the subject and body fields
        ``template_name``: the name of the template to use

    """
    http_method_names = ['get']
    form_class = QuickReplyForm
    formatters = (format_subject, format_body if getattr(settings, 'POSTMAN_QUICKREPLY_QUOTE_BODY', False) else None)
    template_name = 'postman/view.html'

    @login_required_m
    def dispatch(self, *args, **kwargs):
        return super(DisplayMixin, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        user = request.user
        self.msgs = Message.objects.thread(user, self.filter)
        if not self.msgs:
            raise Http404
        Message.objects.set_read(user, self.filter)
        return super(DisplayMixin, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        profilepic="/media/avatar.png"
        username=self.request.user
        obj=userprofile_extended.objects.filter(user_id=username)
        profilepic="/media/avatar.png"
        obj_count=obj.count()
        if obj_count>0:
            for i in obj:
                goal_id=i.image
                if goal_id:
                    profilepic=i.image.url
        context = super(DisplayMixin, self).get_context_data(**kwargs)
        user = self.request.user
        # are all messages archived ?
        for m in self.msgs:
            if not getattr(m, ('sender' if m.sender == user else 'recipient') + '_archived'):
                archived = False
                break
        else:
            archived = True
        # look for the most recent received message (and non-deleted to comply with the future perms() control), if any
        for m in reversed(self.msgs):
            if m.recipient == user and not m.recipient_deleted_at:
                received = m
                break
        else:
            received = None
        context.update({
            'profilepic':profilepic,
            'pm_messages': self.msgs,
            'archived': archived,
            'reply_to_pk': received.pk if received else None,
            'form': self.form_class(initial=received.quote(*self.formatters)) if received else None,
            'next_url': self.request.GET.get('next') or reverse('postman:inbox', current_app=self.request.resolver_match.namespace),
        })
        return context


class MessageView(DisplayMixin, TemplateView):
    """Display one specific message."""

    def get(self, request, message_id, *args, **kwargs):
        self.filter = Q(pk=message_id)
        return super(MessageView, self).get(request, *args, **kwargs)


class ConversationView(DisplayMixin, TemplateView):
    """Display a conversation."""

    def get(self, request, thread_id, *args, **kwargs):
        self.filter = Q(thread=thread_id)
        return super(ConversationView, self).get(request, *args, **kwargs)


class UpdateMessageMixin(object):
    """
    Code common to the archive/delete/undelete actions.

    Attributes:
        ``field_bit``: a part of the name of the field to update
        ``success_msg``: the displayed text in case of success
    Optional attributes:
        ``field_value``: the value to set in the field
        ``success_url``: where to redirect to after a successful POST

    """
    http_method_names = ['post']
    field_value = None
    success_url = None

    @csrf_protect_m
    @login_required_m
    def dispatch(self, *args, **kwargs):
        return super(UpdateMessageMixin, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        next_url = _get_referer(request) or 'postman:inbox'
        pks = request.POST.getlist('pks')
        tpks = request.POST.getlist('tpks')
        if pks or tpks:
            user = request.user
            filter = Q(pk__in=pks) | Q(thread__in=tpks)
            recipient_rows = Message.objects.as_recipient(user, filter).update(**{'recipient_{0}'.format(self.field_bit): self.field_value})
            sender_rows = Message.objects.as_sender(user, filter).update(**{'sender_{0}'.format(self.field_bit): self.field_value})
            if not (recipient_rows or sender_rows):
                raise Http404  # abnormal enough, like forged ids
            messages.success(request, self.success_msg, fail_silently=True)
            return redirect(request.GET.get('next') or self.success_url or next_url)
        else:
            messages.warning(request, _("Select at least one object."), fail_silently=True)
            return redirect(next_url)


class ArchiveView(UpdateMessageMixin, View):
    """Mark messages/conversations as archived."""
    field_bit = 'archived'
    success_msg = ugettext_lazy("Messages or conversations successfully archived.")
    field_value = True


class DeleteView(UpdateMessageMixin, View):
    """Mark messages/conversations as deleted."""
    field_bit = 'deleted_at'
    success_msg = ugettext_lazy("Messages or conversations successfully deleted.")
    field_value = now()


class UndeleteView(UpdateMessageMixin, View):
    """Revert messages/conversations from marked as deleted."""
    field_bit = 'deleted_at'
    success_msg = ugettext_lazy("Messages or conversations successfully recovered.")
