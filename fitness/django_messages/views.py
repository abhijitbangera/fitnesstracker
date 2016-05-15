from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404, render
from django.template import RequestContext
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext as _
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib import messages
from django_messages.models import Message
from django_messages.forms import ComposeForm
from django_messages.utils import format_quote, get_user_model, get_username_field
from tracker.models import userprofile_extended
from tracker.forms import userprofile_extended_goalsettings_Form,userprofile_extended_profilesettings_Form

User = get_user_model()

if "notification" in settings.INSTALLED_APPS and getattr(settings, 'DJANGO_MESSAGES_NOTIFY', True):
    from notification import models as notification
else:
    notification = None

@login_required
def inbox(request, template_name='django_messages/inbox.html'):
    """
    Displays a list of received messages for the current user.
    Optional Arguments:
        ``template_name``: name of the template to use.
    """
    profilepic="/media/avatar.png"
    username=request.user
    obj=userprofile_extended.objects.filter(user_id=request.user)
    obj_count=obj.count()
    if obj_count>0:
                for i in obj:
                    goal_id=i.image
                    if goal_id!=None:
                        profilepic=i.image.url
    message_list = Message.objects.inbox_for(request.user)
    return render_to_response(template_name, {
        'message_list': message_list,
        'profilepic':profilepic,
        'username':str(username).title(),
        'username_original':username,
    }, context_instance=RequestContext(request))

@login_required
def outbox(request, template_name='django_messages/outbox.html'):
    """
    Displays a list of sent messages by the current user.
    Optional arguments:
        ``template_name``: name of the template to use.
    """
    message_list = Message.objects.outbox_for(request.user)
    return render_to_response(template_name, {
        'message_list': message_list,
    }, context_instance=RequestContext(request))

@login_required
def trash(request, template_name='django_messages/trash.html'):
    """
    Displays a list of deleted messages.
    Optional arguments:
        ``template_name``: name of the template to use
    Hint: A Cron-Job could periodicly clean up old messages, which are deleted
    by sender and recipient.
    """
    message_list = Message.objects.trash_for(request.user)
    return render_to_response(template_name, {
        'message_list': message_list,
    }, context_instance=RequestContext(request))



@login_required
def compose(request, recipient=None, form_class=ComposeForm,
        template_name='django_messages/compose.html', success_url=None, recipient_filter=None):
    """
    Displays and handles the ``form_class`` form to compose new messages.
    Required Arguments: None
    Optional Arguments:
        ``recipient``: username of a `django.contrib.auth` User, who should
                       receive the message, optionally multiple usernames
                       could be separated by a '+'
        ``form_class``: the form-class to use
        ``template_name``: the template to use
        ``success_url``: where to redirect after successfull submission
    """
    if request.method == "POST":
        sender = request.user
        # recipient=User.objects.get(username='abhi')
        # form = form_class(request.POST, recipient_filter=recipient_filter)
        
        form = form_class(request.POST)
        
        print("********")
        print(recipient_filter)
     
        for i in form:
            print(i.name)
        print(recipient)
        # form.recipient.value=""
        # form.recipient.value='abhi'
        print("--------")
        # print(form.fields['id_recipient'])
        for i in form:
            print(i)

        if form.is_valid():
            
            # form.recipient_id=2
            form.save(sender=request.user)
            messages.info(request, _(u"Message successfully sent."))
            if success_url is None:
                success_url = reverse('messages_inbox')
            if 'next' in request.GET:
                success_url = request.GET['next']
            return HttpResponseRedirect(success_url)

    else:
        form = form_class()
        if recipient is not None:
            recipients = [u for u in User.objects.filter(**{'%s__in' % get_username_field(): [r.strip() for r in recipient.split('+')]})]
            form.fields['recipient'].initial = recipients

    #Trainer profile code ------------------------
    username=request.user
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

    obj=userprofile_extended.objects.filter(user_id=username)
    profilepic="/media/avatar.png"
    obj_count=obj.count()
    if obj_count>0:
        for i in obj:
            goal_id=i.image
            if goal_id!=None:
                profilepic=i.image.url


    print("=================")
    print(obj_count) 
    if obj_count==0:
        
        form=userprofile_extended_goalsettings_Form()
        messages.add_message(request,messages.SUCCESS, "Please update your workout goal below. Based on your goal the system would allocate appropriate instructors to your profile.")
        context={'form':form,
                 'profilepic':profilepic,
                 'username_original':username,
                'username':str(username).title(),  }
        return render(request, "user_goal_settings.html",context) 
    if obj_count>0:
        for i in obj:
            goal_id=i.goal

            print(goal_id)
            print("=================")
            print(i.image)
            if goal_id==None:
                form=userprofile_extended_goalsettings_Form()
                messages.add_message(request,messages.SUCCESS, "Please update your workout goal below. Based on your goal the system would allocate appropriate instructors to your profile.")
                context={'form':form,
                         'profilepic':profilepic,
                         'username_original':username, 
                          'username':str(username).title(),
                          }
                return render(request, "user_goal_settings.html",context)
            
            if i.image!=None:
                profilepic=i.image.url
            trainer=i.trainer
            nutritionist=i.nutritionist
            supplimentexpert=i.supplimentexpert
            contact=i.contact
    if (trainer):
        messages.add_message(request,messages.SUCCESS, "Please select your Recipient from the below list of profiles.")
        t = User.objects.get(username=trainer)
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
    #-------------------------------------------


    # print(trainer)
    return render_to_response(template_name, {
        'username':str(username).title(),
        'username_original':username,
        'form': form,
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
    }, context_instance=RequestContext(request))

@login_required
def reply(request, message_id, form_class=ComposeForm,
        template_name='django_messages/compose.html', success_url=None,
        recipient_filter=None, quote_helper=format_quote,
        subject_template=_(u"Re: %(subject)s"),):
    """
    Prepares the ``form_class`` form for writing a reply to a given message
    (specified via ``message_id``). Uses the ``format_quote`` helper from
    ``messages.utils`` to pre-format the quote. To change the quote format
    assign a different ``quote_helper`` kwarg in your url-conf.

    """
    parent = get_object_or_404(Message, id=message_id)

    if parent.sender != request.user and parent.recipient != request.user:
        raise Http404

    if request.method == "POST":
        sender = request.user
        form = form_class(request.POST, recipient_filter=recipient_filter)
        if form.is_valid():
            form.save(sender=request.user, parent_msg=parent)
            messages.info(request, _(u"Message successfully sent."))
            if success_url is None:
                success_url = reverse('messages_inbox')
            return HttpResponseRedirect(success_url)
    else:
        form = form_class(initial={
            'body': quote_helper(parent.sender, parent.body),
            'subject': subject_template % {'subject': parent.subject},
            'recipient': [parent.sender,]
            })
    return render_to_response(template_name, {
        'form': form,
    }, context_instance=RequestContext(request))

@login_required
def delete(request, message_id, success_url=None):
    """
    Marks a message as deleted by sender or recipient. The message is not
    really removed from the database, because two users must delete a message
    before it's save to remove it completely.
    A cron-job should prune the database and remove old messages which are
    deleted by both users.
    As a side effect, this makes it easy to implement a trash with undelete.

    You can pass ?next=/foo/bar/ via the url to redirect the user to a different
    page (e.g. `/foo/bar/`) than ``success_url`` after deletion of the message.
    """
    user = request.user
    now = timezone.now()
    message = get_object_or_404(Message, id=message_id)
    deleted = False
    if success_url is None:
        success_url = reverse('messages_inbox')
    if 'next' in request.GET:
        success_url = request.GET['next']
    if message.sender == user:
        message.sender_deleted_at = now
        deleted = True
    if message.recipient == user:
        message.recipient_deleted_at = now
        deleted = True
    if deleted:
        message.save()
        messages.info(request, _(u"Message successfully deleted."))
        if notification:
            notification.send([user], "messages_deleted", {'message': message,})
        return HttpResponseRedirect(success_url)
    raise Http404

@login_required
def undelete(request, message_id, success_url=None):
    """
    Recovers a message from trash. This is achieved by removing the
    ``(sender|recipient)_deleted_at`` from the model.
    """
    user = request.user
    message = get_object_or_404(Message, id=message_id)
    undeleted = False
    if success_url is None:
        success_url = reverse('messages_inbox')
    if 'next' in request.GET:
        success_url = request.GET['next']
    if message.sender == user:
        message.sender_deleted_at = None
        undeleted = True
    if message.recipient == user:
        message.recipient_deleted_at = None
        undeleted = True
    if undeleted:
        message.save()
        messages.info(request, _(u"Message successfully recovered."))
        if notification:
            notification.send([user], "messages_recovered", {'message': message,})
        return HttpResponseRedirect(success_url)
    raise Http404

@login_required
def view(request, message_id, form_class=ComposeForm, quote_helper=format_quote,
        subject_template=_(u"Re: %(subject)s"),
        template_name='django_messages/view.html'):
    """
    Shows a single message.``message_id`` argument is required.
    The user is only allowed to see the message, if he is either
    the sender or the recipient. If the user is not allowed a 404
    is raised.
    If the user is the recipient and the message is unread
    ``read_at`` is set to the current datetime.
    If the user is the recipient a reply form will be added to the
    tenplate context, otherwise 'reply_form' will be None.
    """
    user = request.user
    now = timezone.now()
    message = get_object_or_404(Message, id=message_id)
    if (message.sender != user) and (message.recipient != user):
        raise Http404
    if message.read_at is None and message.recipient == user:
        message.read_at = now
        message.save()

    context = {'message': message, 'reply_form': None}
    if message.recipient == user:
        form = form_class(initial={
            'body': quote_helper(message.sender, message.body),
            'subject': subject_template % {'subject': message.subject},
            'recipient': [message.sender,]
            })
        context['reply_form'] = form
    return render_to_response(template_name, context,
        context_instance=RequestContext(request))
