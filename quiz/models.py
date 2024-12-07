import datetime
from datetime import timedelta
from random import choices
from time import timezone

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class RoleChoices(models.TextChoices):
        ADMIN = 'admin', 'Admin'
        USER = 'user', 'User'

    class LevelChoices(models.TextChoices):
        BEGINNER = 'beginner', 'Beginner'
        INTERMEDIATE = 'intermediate', 'Intermediate'
        ADVANCED = 'advanced', 'Advanced'

    class UserStatus(models.TextChoices):
        ACTIVE = 'active', 'Active'
        INACTIVE = 'inactive', 'Inactive'

    date_of_birth = models.DateField(null=True, blank=True)
    image = models.ImageField(upload_to='user/images/', null=True, blank=True)
    about = models.TextField(null=True, blank=True)
    role = models.CharField(max_length=100, choices=RoleChoices.choices, default=RoleChoices.USER)
    level = models.CharField(max_length=100, choices=LevelChoices.choices, default=LevelChoices.BEGINNER)
    balls = models.IntegerField(default=0)
    gifts = models.ManyToManyField('Shop')
    is_active = models.BooleanField(default=False)
    status = models.CharField(max_length=100, choices=UserStatus.choices, default=UserStatus.INACTIVE)

    @property
    def create_verification_code(self):
        code = "".join(choices("0123456789", k=4))
        UserConfirmation.objects.create(
            user=self,
            code=code,
            expire_time=datetime.datetime.now() + timedelta(minutes=5),
        )
        return code


class UserConfirmation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='code')
    code = models.IntegerField()
    expire_time = models.DateTimeField(null=True, blank=True)
    is_confirmed = models.BooleanField(default=False)

    # def save(self, *args, **kwargs):
    #     self.expire_time = datetime.datetime.now() + datetime.timedelta(minutes=5)
    #     super(UserConfirmation, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.user.username}: {self.code}'


class Shop(models.Model):
    name = models.CharField(max_length=100)
    about = models.TextField()
    amount = models.IntegerField()
    image = models.ImageField(upload_to='shop/images/', null=True, blank=True)
    is_active = models.BooleanField()
    price = models.FloatField()
    discount = models.FloatField()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.amount == 0:
            self.is_active = False
        return super().save(*args, **kwargs)

class Subjects(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Test(models.Model):
    class LevelChoices(models.TextChoices):
        BEGINNER = 'beginner', 'Beginner'
        INTERMEDIATE = 'intermediate', 'Intermediate'
        ADVANCED = 'advanced', 'Advanced'

    name = models.CharField(max_length=100)
    subject = models.ForeignKey(Subjects, on_delete=models.CASCADE, related_name='tests')
    level = models.CharField(max_length=100, choices=LevelChoices.choices, default=LevelChoices.BEGINNER)
    balls = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if self.level == self.LevelChoices.BEGINNER:
            self.balls += 10
        elif self.level == self.LevelChoices.INTERMEDIATE:
            self.level += 20
        elif self.level == self.LevelChoices.ADVANCED:
            self.level += 30
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Question(models.Model):
    about = models.TextField()
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='questions')

    def __str__(self):
        return self.about

class Option(models.Model):
    name = models.CharField(max_length=100)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    is_true = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.question.about}, option: {self.name}'

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['question', 'is_true'], name='unique_option')
        ]


