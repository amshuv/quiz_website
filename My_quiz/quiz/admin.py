from django.contrib import admin
from .models import User,QuesModel,ResultModel, Player
# Register your models here.

admin.site.register(User)
admin.site.register(Player)
admin.site.register(QuesModel)
admin.site.register(ResultModel)