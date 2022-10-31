from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.conf import settings
from django.utils import timezone

# custom user model manager to build functions that is commonly used
# customer user model to create a new user


class MyAccountManager(BaseUserManager):
    def create_user(self, user_email, username, age, country, height, password=None):
        # email is a required field
        if not user_email:
            raise ValueError("Email address is a compulsory field.")
        # username is a required field
        if not username:
            raise ValueError("Username is a compulsory field.")

        # if both conditions are present, create user
        user = self.model(
            # normalize and make it lowercase
            user_email=self.normalize_email(user_email),
            username=username,
            age=age,
            country=country,
            height=height,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    # customer user model to create a superuser
    def create_superuser(self, user_email, username, password):
        user = self.create_user(
            user_email=self.normalize_email(user_email),
            username=username,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


# custom user model

def get_profile_image_filepath(self, filename):
    return 'profile_images/' + str(self.pk) + '/profile_image.png'


def get_default_profile_image():
    return "icon/penguin.png"

# include login fields


class Account(AbstractBaseUser):

    user_email = models.EmailField(
        verbose_name="email", max_length=60, unique=True)
    username = models.CharField(max_length=30, unique=True)
    date_joined = models.DateTimeField(
        verbose_name='date joined', auto_now_add=True)
    last_login_date = models.DateTimeField(
        verbose_name='last login', auto_now=True)
    # override following four parameters
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    profile_image = models.ImageField(max_length=255, upload_to=get_profile_image_filepath,
                                      null=True, blank=True, default=get_default_profile_image)
    hide_email = models.BooleanField(default=True)

    # login with email instead of default username
    USERNAME_FIELD = "user_email"

    # username required to create account
    REQUIRED_FIELDS = ["username"]

    objects = MyAccountManager()

    # return username when individual fields are not returned
    def str(self):
        return self.username

    def get_profile_image_filename(self):
        return str(self.profile_image)[str(self.profile_image).index(f"profile_images/{self.pk}/"):]

    # if user is admin, given permission
    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


class FriendList(models.Model):
    # one friendlist per user
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user")
    friends = models.ManyToManyField(
        settings.AUTH_USER_MODEL, blank=True, related_name="friends")

    # returns the username
    def str(self):
        return self.user.username

    def add_friend(self, account):

        # if user account is not part of friendlist, add friend
        if not account in self.friends.all():
            self.friends.add(account)
            self.save()

    # def remove_friend(self, account):
    #   """
    #   Remove a friend.
    #   """
    #   if account in self.friends.all():
    #     self.friends.remove(account)


# def unfriend(self, removee):
    #   """
    #   Initiate the action of unfriending someone.
    #   """
    #   remover_friends_list = self # person terminating the friendship

    #   # Remove friend from remover friend list
    #   remover_friends_list.remove_friend(removee)

    #   # Remove friend from removee friend list
    #   friends_list = FriendList.objects.get(user=removee)
    #   friends_list.remove_friend(remover_friends_list.user)

    def is_mutual_friend(self, friend):
        # check if the user is a friend
        if friend in self.friends.all():
            return True
        return False

# model for each post


class Post(models.Model):
    user = models.ForeignKey(
        Account, on_delete=models.DO_NOTHING, related_name='posts')
    date_Post = models.DateTimeField(default=timezone.now)
    text = models.CharField(max_length=500)
    image = models.ImageField(upload_to='post_image', blank=True, null=True)
    post_Id = models.AutoField(primary_key=True)


class FriendRequest(models.Model):
    """
    A friend request consists of two main parts:
      1. SENDER
        - Person sending/initiating the friend request
      2. RECIVER
        - Person receiving the friend friend
    """

    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="receiver")
    # checks if friend request is active
    is_active = models.BooleanField(blank=False, null=False, default=True)
    # time entry when friend request was sent
    timestamp = models.DateTimeField(auto_now_add=True)

    # returns the username
    def str(self):
        return self.sender.username

    def accept(self):

        # accept friend request and update friendlist for sender and receiver
        receiver_friend_list = FriendList.objects.get(user=self.receiver)
        if receiver_friend_list:
            receiver_friend_list.add_friend(self.sender)
            sender_friend_list = FriendList.objects.get(user=self.sender)
            if sender_friend_list:
                sender_friend_list.add_friend(self.receiver)
                self.is_active = False
                self.save()

    # def decline(self):
    #   """
    #   Decline a friend request.
    #   Is it "declined" by setting the is_active field to False
    #   """
    #   self.is_active = False
    #   self.save()

    # def cancel(self):
    #   """
    #   Cancel a friend request.
    #   Is it "cancelled" by setting the is_active field to False.
    #   This is only different with respect to "declining" through the notification that is generated.
    #   """
    #   self.is_active = False
    #   self.save()
