from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser, Group

class User(AbstractUser):
    is_player = models.BooleanField(default=False)
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    custom_user_groups = models.ManyToManyField(Group, related_name='custom_users')
class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    email_id = models.EmailField

class QuesModel(models.Model):
    LEVEL_CHOICES = (
        ('Level 1', 'Level 1'),
        ('Level 2', 'Level 2'),
    )
    question = models.CharField(max_length=200, null=True)
    op1 = models.CharField(max_length=200, null=True)
    op2 = models.CharField(max_length=200, null=True)
    op3 = models.CharField(max_length=200, null=True)
    op4 = models.CharField(max_length=200, null=True)
    ans = models.CharField(max_length=200, null=True)
    level = models.CharField(max_length=10, choices=LEVEL_CHOICES,default='level1')

    def __str__(self):
        return self.question

class ResultModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True)
    score = models.IntegerField(null=True)
    percentage = models.IntegerField(null=True)
    correct_answers = models.IntegerField(null=True)
    incorrect_answers = models.IntegerField(null=True)
    total_question = models.IntegerField(null=True)
    date = models.DateField(auto_now_add=True,null=True)
    level = models.CharField(max_length=10, null=True)

    def __str__(self):
        if isinstance(self.user, User):
            return f"{self.user.username}"
