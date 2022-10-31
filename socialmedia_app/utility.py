from socialmedia_app.models import FriendRequest

# determine if two users are friends (active friend request)
def get_friend_request_or_false(sender, receiver):
	try:
		return FriendRequest.objects.get(sender=sender, receiver=receiver, is_active=True)
	except FriendRequest.DoesNotExist:
		return False