
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.utils.text import slugify


from users.manager import UserManager


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, max_length=260, error_messages={'unique': 'Email already exist'})
    is_customer = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        db_table = 'users_user'
        verbose_name = 'user'
        verbose_name_plural = 'users'
        ordering = ['-id']

    def __str__(self):
        return self.email
    


class Manager(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.email
    
class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    

    def __str__(self):
        return self.user.email
    
class TrackedLink(models.Model):
    CATEGORY_CHOICES = [
        ('portfolio', 'Portfolio'),
        ('linkedin', 'LinkedIn'),
        ('github', 'GitHub'),
        ('youtube', 'YouTube'),
        ('other', 'Other'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    url = models.URLField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    other_category_name = models.CharField(max_length=100, blank=True, null=True)
    custom_slug = models.SlugField(max_length=50, unique=True, blank=True, null=True)
    click_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.custom_slug:
            self.custom_slug = slugify(self.custom_slug)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.url} ({self.category})"
    
class TrackedClick(models.Model):
    link = models.ForeignKey(TrackedLink, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
