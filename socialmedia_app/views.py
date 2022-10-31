from django.views import View
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.conf import settings

from .models import Account, FriendRequest, FriendList, Post
from .forms import RegistrationForm, NewPostForm
from .utility import get_friend_request_or_false
from .request_status import FriendRequestStatus

import json 

def index(request):
    return render(request, 'chat_index.html', {})

def room(request, room_name):
    return render(request, 'chat_room.html', {
        'room_name': room_name
    })

# def index(request):
#     return render(request, 'chat/index.html', {})

# def room(request, room_name):
#     return render(request, 'chat/room.html', {
#         'room_name': room_name
#     })



	








class home_screen_post(View):

# get user input as post
	def get(self, request, *args, **kwargs):
		posts = Post.objects.all()
		form = NewPostForm()

		context = {
		'post_list': posts,
		'form': form,
		}

		return render(request, 'home.html', context)

	def post(self, request, *args, **kwargs):
		logged_in_user = request.user
		posts = Post.objects.all()
		form = NewPostForm(request.POST, request.FILES)

		if form.is_valid():
			new_post = form.save(commit=False)
			new_post.user =logged_in_user
			new_post.save()

		context = {
			'post_list': posts,
			'form': form,
		}

		return render(request, 'home.html', context)


def register_view(request, *args, **kwargs):
	user = request.user
	if user.is_authenticated: 
		return HttpResponse("You are already authenticated as " + str(user.user_email))

	context = {}
	if request.POST:
		form = RegistrationForm(request.POST)
		if form.is_valid():
			form.save()
	# email = form.cleaned_data.get('user_email').lower()
	# raw_password = form.cleaned_data.get('password1')
	# account = authenticate(email=email, password=raw_password)
	# login(request, account)
	# destination = kwargs.get("next")
	# if destination:
	# 	return redirect(destination)
			return redirect('home')
		else:
			context={
				'form' : form
			}

	else:
		form = RegistrationForm()
		context={
			'form' : form
		}
	return render(request, 'register.html', context)







def account_view(request, *args, **kwargs):
	"""
	- Logic here is kind of tricky
		is_self (boolean)
			is_friend (boolean)
				1: NO_REQUEST_SENT
				2: THEM_SENT_TO_YOU
				3: YOU_SENT_TO_THEM
	"""
	context = {}
	user_id = kwargs.get("user_id")
	try:
		account = Account.objects.get(pk=user_id)
	except:
		return HttpResponse("Something went wrong.")
	if account:
		context['id'] = account.id
		context['username'] = account.username
		context['email'] = account.user_email
		context['profile_image'] = account.profile_image.url
		context['hide_email'] = account.hide_email

		try:
			# retrieve friendlist of another user
			friend_list = FriendList.objects.get(user=account)
		except Exception as e:
		# except FriendList.DoesNotExist():
			# create friendlist for user if it does not exist
			friend_list = FriendList(user=account)
			friend_list.save()
		# accessing friends field from the model and using all() to retrieve query set
		friends = friend_list.friends.all()
		# friends of the other user profile we are viewing
		context['friends'] = friends

		# Define template variables
		is_self = True
		is_friend = False
		request_sent = FriendRequestStatus.NO_REQUEST_SENT.value
		friend_requests = None
		user = request.user

		# viewing another user account
		if user.is_authenticated and user != account:
			is_self = False

			# search thru their friendlist and search for our id
			if friends.filter(pk=user.id):
				is_friend = True
			else:
				# friend request sent from them to you
				is_friend = False
				
				# CASE1: Request has been sent from THEM to YOU: FriendRequestStatus.THEM_SENT_TO_YOU
				if get_friend_request_or_false(sender=account, receiver=user) != False:
					# get value of friend request
					request_sent = FriendRequestStatus.THEM_SENT_TO_YOU.value
					context['pending_friend_request_id'] = get_friend_request_or_false(sender=account, receiver=user).id
				# CASE2: Request has been sent from YOU to THEM: FriendRequestStatus.YOU_SENT_TO_THEM
				elif get_friend_request_or_false(sender=user, receiver=account) != False:
					# get value of friend request
					request_sent = FriendRequestStatus.YOU_SENT_TO_THEM.value
				# CASE3: No request sent from YOU or THEM: FriendRequestStatus.NO_REQUEST_SENT
				else:
					request_sent = FriendRequestStatus.NO_REQUEST_SENT.value
		
		# if youre not logged in
		elif not user.is_authenticated:
			is_self = False
		# youre looking at your own profile
		else:
			try:
				# get all active friend request for the user we are viewing
				friend_requests = FriendRequest.objects.filter(receiver=user, is_active=True)
			except:
				pass


		# Set the template variables to the values
		context['is_self'] = is_self
		context['is_friend'] = is_friend
		context['request_sent'] = request_sent
		context['friend_requests'] = friend_requests
		context['BASE_URL'] = settings.BASE_URL
		return render(request, "account.html", context)






def search_user(request, *args, **kwargs):
	context = {}
	if request.method == "GET":
		search_query = request.GET.get("q")
		print(search_query)
		if len(search_query) > 0:
			search_results = Account.objects.filter(user_email__icontains=search_query).filter(username__icontains=search_query).distinct()
			user = request.user
			accounts = [] # [(account1, True), (account2, False), ...]
			for account in search_results:
				accounts.append((account, False)) # you have no friends yet
			context['accounts'] = accounts
				
	return render(request, "search_result.html", context)























def send_friend_request(request, *args, **kwargs):
	user = request.user
	payload = {}
	if request.method == "POST" and user.is_authenticated:
		user_id = request.POST.get("receiver_user_id")
		if user_id:
			receiver = Account.objects.get(pk=user_id)
			try:
				# Get any friend requests (active and not-active)
				friend_requests = FriendRequest.objects.filter(sender=user, receiver=receiver)
				# find if any of them are active (pending)
				try:
					for request in friend_requests:
						if request.is_active:
							raise Exception("You already sent them a friend request.")
					# If none are active create a new friend request
					friend_request = FriendRequest(sender=user, receiver=receiver)
					friend_request.save()
					payload['response'] = "Friend request sent."
				except Exception as e:
					payload['response'] = str(e)
			except FriendRequest.DoesNotExist:
				# There are no friend requests so create one.
				friend_request = FriendRequest(sender=user, receiver=receiver)
				friend_request.save()
				payload['response'] = "Friend request sent."

			if payload['response'] == None:
				payload['response'] = "Something went wrong."
		else:
			payload['response'] = "Unable to sent a friend request."
	else:
		payload['response'] = "You must be authenticated to send a friend request."
	return HttpResponse(json.dumps(payload), content_type="application/json")



