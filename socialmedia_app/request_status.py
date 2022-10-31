from enum import Enum

# three different states
class FriendRequestStatus(Enum):
	NO_REQUEST_SENT = 1
	THEM_SENT_TO_YOU = 2
	YOU_SENT_TO_THEM = 3