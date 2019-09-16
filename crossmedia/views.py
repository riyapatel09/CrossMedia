from django.contrib.auth import authenticate
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse

from .models import SiteGroup, Profile, FriendList, Post, LikePost, FriendRequestList, ParentChild
#from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, ProfileForm, PostForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as registration_login
from datetime import datetime
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from crossmedia.tokens import account_activation_token
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.models import User
from django.shortcuts import render
from .forms import RegisterFormStepOne, RegisterFormStepTwo
from datetime import date
import dateutil.parser
from django.shortcuts import render_to_response
# Create your views here.

# @login_required
# def home(request):
#     context = {
#         'sitegroups' : SiteGroup.objects.all()
#     }
#     return render(request, 'crossmedia/welcome.html', context)

def login(request):
    return render(request, 'crossmedia/login.html')

def register(request):
    if request.method == 'POST':
        us_form = UserRegisterForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES or None)

        if us_form.is_valid() and profile_form.is_valid():
            user = us_form.save()
            user.refresh_from_db()
            user.profile.image = profile_form.cleaned_data.get('image')
            u_bd = request.session['user_bd']
            store_user_birthdate = datetime.strptime(u_bd, '%Y-%m-%d')
            d = dateutil.parser.parse(u_bd).date()
            #print(d)
            user.profile.birth_date = d
            user.profile.is_parent = True
            #user_age = int((datetime.now().date() - user.profile.birth_date).days / 365.25)
            user.save()
            user.profile.save()
            username = us_form.cleaned_data.get('username')
            raw_password = us_form.cleaned_data.get('password1')
            l_user = authenticate(username=user.username, password=raw_password)
            registration_login(request, l_user)
            messages.success(request, f'Account created for {username}!')
            return redirect('home')

            # user = us_form.save(commit=False)
            # user.is_active = False
            # user.save()
            # current_site = get_current_site(request)
            # subject = 'Activate Your Child Crossmedia Account'
            # message = render_to_string('account_activation_email.html', {
            #     'user': user,
            #     'domain': current_site.domain,
            #     'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            #     'token': account_activation_token.make_token(user),--
            # })
            # parent_user = User.objects.get(pk=44)
            # parent_user.email_user(subject, message)
            # return redirect('account_activation_sent')
    else:
        us_form = UserRegisterForm()
        profile_form = ProfileForm()
    return render(request, 'crossmedia/register.html', {'form' : us_form, 'profile_form' : profile_form})

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your account has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form' : u_form,
        'p_form' : p_form
    }
    return render(request, 'crossmedia/profile.html', context)
#messages.debug
#messages.info
#messages.success
#messages.warning
#messages.error

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64).decode() )
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        registration_login(request, user)
        return redirect('home')
    else:
        return render(request, 'account_activation_invalid.html')

def account_activation_sent(request):
    return render(request, 'account_activation_sent.html')

def account_activation_email(request):
    return render(request, 'account_activation_email.html')

def register_form_step_one(request):
    if request.method == 'POST':
        step_one_form = RegisterFormStepOne(request.POST)

        if step_one_form.is_valid():
            u_birthdate = step_one_form.cleaned_data.get('user_birthdate')
            today = date.today()
            u_age = today.year - u_birthdate.year - ((today.month, today.day) < (u_birthdate.month, u_birthdate.day))
            if u_age >= 18:
                send_user_birthdate = str(u_birthdate)
                request.session['user_bd'] = send_user_birthdate
                return redirect('register')
            else:
                send_user_birthdate = str(u_birthdate)
                request.session['user_bd'] = send_user_birthdate
                return redirect('register_step_two')

    else:
        step_one_form = RegisterFormStepOne()

    return render(request, 'crossmedia/register_step_one_form.html', {'step_one_form' : step_one_form})

def register_form_step_two(request):
    if request.method == 'POST':
        step_two_form = RegisterFormStepTwo(request.POST)

        if step_two_form.is_valid():
            u_parent_email = step_two_form.cleaned_data.get('parent_email')
            try:
                parent_user = User.objects.get(email=u_parent_email)
                if parent_user.profile.is_parent == True:
                    request.session['send_user_parent_email'] = u_parent_email
                    return redirect('register_step_three')
                else:
                    messages.warning(request, f'Entered email is not a registered parent email!')
                    step_two_form = RegisterFormStepTwo()

            except User.DoesNotExist:
                messages.warning(request, f'Parent do not have account with given email!')
                step_two_form = RegisterFormStepTwo()

    else:
        step_two_form = RegisterFormStepTwo()

    return render(request, 'crossmedia/register_step_two_form.html', {'step_two_form' : step_two_form})

def register_form_step_three(request):
    if request.method == 'POST':
        us_form = UserRegisterForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES or None)

        if us_form.is_valid() and profile_form.is_valid():
            user = us_form.save(commit=False)
            user.is_active = False
            u_bd = request.session['user_bd']
            store_user_birthdate = datetime.strptime(u_bd, '%Y-%m-%d')
            d = dateutil.parser.parse(u_bd).date()
            u_parent_email = request.session['send_user_parent_email']
            print(u_parent_email)
            user.save()
            user.profile.birth_date = d
            user.profile.is_parent = False
            user.profile.save()
            current_site = get_current_site(request)
            subject = 'Activate Your Child Crossmedia Account'
            message = render_to_string('account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            #parent_user = User.objects.get(pk=44)
            parent_user = User.objects.get(email=u_parent_email)
            parent_user.email_user(subject, message)
            obj_p_c = ParentChild(parent=parent_user,child=user)
            obj_p_c.save()
            return redirect('account_activation_sent')
    else:
        us_form = UserRegisterForm()
        profile_form = ProfileForm()
    return render(request, 'crossmedia/register_step_three_form.html', {'form' : us_form, 'profile_form' : profile_form})

@login_required
def friendlist(request):
    # user = authenticate(username='asdd', password='testuser12')
    # user = request.user
    current_user = request.user
    #if current_user:
    if current_user.is_active:
        #registration_login(request, current_user)
        # current_user = request.user
        friendlist = FriendList.objects.filter(user=current_user)
        return render(request, 'crossmedia/friendlist.html', {'friendlist': friendlist})
    else:
        return HttpResponse('Your account is disabled.')
   # else:
       # return HttpResponse('Invalid login details.')

def friend_profile(request, id=None):
        instance = get_object_or_404(User, id=id)
        # share_string = quote_plus(instance.content)
        context = {'instance': instance}
        return render(request, 'crossmedia/friend_profile.html', context)

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            messages.success(request, f'Postcreated!')
            return redirect("home")
        else:
            #print("errkasjdhfkjhvkba")
            messages.warning(request, f'Post not created!')
    else:
        form = PostForm()
        context = {'form': form}
    return render(request, 'crossmedia/post_form.html', context)

@login_required
def post_update(request, id=None):
    instance = get_object_or_404(Post, id=id)
    form = PostForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return redirect("my-posts")
    context = {'instance': instance, 'form':form}
    return render(request, 'crossmedia/post_update.html', context)

@login_required
def home(request):
    post_list_of_friends = []
    #user = authenticate(username='Riya', password='Parthpatel16*')
    #if user:
    #if user.is_active:
            #login(request, user)
    current_user = request.user
    friendlist = FriendList.objects.filter(user=current_user)
    for f in friendlist:
        post = Post.objects.filter(user=f.friend).order_by('-timestamp')
        for p in post:
            post_list_of_friends.append(p)

    current_user_posts = Post.objects.filter(user=current_user)
    for c_u_post in current_user_posts:
        post_list_of_friends.append(c_u_post)
    print(post_list_of_friends)
    post_list_of_friends.sort(key=lambda x:x.timestamp, reverse=True)
    print(post_list_of_friends)
    #list_of_posts = Post.objects.all()
    #context = {'list_of_posts': post_list_of_friends}
    return render(request, 'crossmedia/welcome.html', {'post_list_of_friends': post_list_of_friends})

@login_required()
def post_detail(request, id=None):
    current_user = request.user
    #instance = get_object_or_404(Post, id=id)
    current_user_posts = Post.objects.filter(user=current_user).order_by('-timestamp')
    #share_string = quote_plus(instance.content)
    #context = {'title': instance.title, 'instance': instance, 'share_string':share_string}
    return render(request, 'crossmedia/my_posts.html', {'my_posts':current_user_posts})

def post_delete(request, id=None):
    instance = get_object_or_404(Post, id=id)
    instance.delete()
    return redirect("my-posts")

def post_like(request, id=None):
    new_like, created = LikePost.objects.get_or_create(user=request.user, post_id=id)
    if not created:
        liked = "true"
        # return render(request, 'crossmedia/welcome.html', {'liked': liked})
        # return HttpResponse("the user already liked this picture before")
        # the user already liked this picture before
    else:
        # oll korrekt
        p = Post.objects.get(pk=id)
        number_of_likes = p.likepost_set.all().count()
        print(number_of_likes)
        # return render(request, 'crossmedia/welcome.html', {'number_of_likes': number_of_likes})
    return redirect("home")

@login_required()
def people_you_may_know(request):
    #user = authenticate(username='riya12', password='testuser12')
    current_user = request.user
    friend_list = FriendList.objects.filter(user=current_user).values('friend__id')
    friend_requests_sent_list = FriendRequestList.objects.filter(requested_user=current_user).values('user__id')
    fl = FriendRequestList.objects.filter(user=current_user).values('requested_user__id')
    remaining_user = User.objects.exclude(id__in=friend_list).exclude(id=current_user.id).exclude(id__in=friend_requests_sent_list).exclude(id__in=fl)

    #friend_requests_sent_list = FriendRequestList.objects.filter(requested_user=current_user)
    #print(friend_requests_sent_list)
    return render(request, 'crossmedia/people_list.html', {'remaining_user': remaining_user})

@login_required()
def send_request(request, id=None):
    current_user = request.user
    request_sent_user = User.objects.get(id=id)
    sent_request_obj = FriendRequestList(user=current_user,requested_user=request_sent_user)
    sent_request_obj.save()
    #print(current_user)
    #print(request_sent_user)
    is_sent = True
    friend_list = FriendList.objects.filter(user=current_user).values('friend__id')
    remaining_user = User.objects.exclude(id__in=friend_list).exclude(id=current_user.id)
    return render(request, 'crossmedia/people_list.html', {'remaining_user': remaining_user, 'is_sent' : is_sent, 'request_sent_user' :request_sent_user })

@login_required()
def friend_requests(request):
    current_user = request.user
    received_requests_obj = FriendRequestList.objects.filter(requested_user=current_user)
    print(received_requests_obj)
    return render(request, 'crossmedia/friend_requests.html', {'received_requests': received_requests_obj})

@login_required()
def accept_friend_request(request, id=None):
    current_user = request.user
    requesting_user = User.objects.get(id=id)
    obj1 = FriendList(user=current_user, friend=requesting_user)
    obj1.save()
    obj2 = FriendList(user=requesting_user, friend=current_user)
    obj2.save()
    FriendRequestList.objects.filter(requested_user=current_user, user=requesting_user).delete()
    # return redirect('friend-requests')
    received_requests_obj = FriendRequestList.objects.filter(requested_user=current_user)
    return render(request, 'crossmedia/friend_requests.html', {'received_requests': received_requests_obj})

@login_required
def children_list(request):
    current_user = request.user
    if current_user.is_active:
        childrenlist = ParentChild.objects.filter(parent=current_user)
        return render(request, 'crossmedia/children_accounts.html', {'childrenlist': childrenlist})
    else:
        return HttpResponse('Your account is disabled.')