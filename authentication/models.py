from ckeditor.fields import RichTextField
from django.contrib.auth.models import AbstractUser, UserManager
from django.db.models import ImageField, DateTimeField, TextChoices, BooleanField, SET_NULL
from django.db.models import Model, ForeignKey, CASCADE, ManyToManyField
from django.db.models.fields import CharField, EmailField, PositiveIntegerField


class User(AbstractUser):
    class RoleType(TextChoices):
        ADMIN = "admin", "Admin"
        USER = 'user', 'User'

    avatar = ImageField(upload_to='avatars/%Y/%m/%d/', null=True, blank=True)
    email = EmailField(max_length=255, unique=True)
    bio = RichTextField(null=True, blank=True)
    role = CharField(max_length=25, choices=RoleType.choices, default=RoleType.USER)
    city = ForeignKey('authentication.City', related_name='users', on_delete=SET_NULL, null=True, blank=True)
    reputation = PositiveIntegerField(default=0)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.username

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class City(Model):
    name = CharField(max_length=60)


class Follow(Model):
    class Meta:
        unique_together = ("follower", "following")

    follower = ForeignKey('authentication.User', related_name='following_set', on_delete=CASCADE)
    following = ForeignKey('authentication.User', related_name='followers_set', on_delete=CASCADE)
    created_at = DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.follower.username} -> {self.following.username}"


class Badge(Model):
    name = CharField(max_length=255, unique=True)
    description = RichTextField(null=True, blank=True)
    icon = ImageField(upload_to='badges/%Y/%m/%d/', null=True, blank=True)
    users = ManyToManyField(User, related_name='badges', blank=True)

    def __str__(self):
        return self.name


class Notifications(Model):
    class NotificationType(TextChoices):
        LIKED = 'liked', 'liked'
        FOLLOWED = 'followed', 'followed'
        COMMENTED = 'commented', 'commented'
        SAVED = 'saved', 'Saved'

    recipient = ForeignKey('authentication.User', on_delete=CASCADE, related_name="notifications")
    sender = ForeignKey('authentication.User', on_delete=CASCADE, related_name="notification")
    type = CharField(max_length=20, choices=NotificationType.choices)
    message = RichTextField()
    created_at = DateTimeField(auto_now_add=True)
    is_read = BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.recipient.username}"


class Sessions(Model):
    user = ForeignKey('authentication.User', on_delete=CASCADE, related_name='sessions')
    ip_address = CharField(max_length=200)
    device_name = CharField(max_length=200)
    last_login = DateTimeField(auto_now=True)
    expires_at = DateTimeField(auto_now_add=True)