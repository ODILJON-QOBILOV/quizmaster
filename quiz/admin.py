from django.contrib import admin

from quiz.models import Question, User, Test, Option, Shop, Subjects, UserConfirmation

# Register your models here.

admin.site.register(Question)
admin.site.register(Test)
admin.site.register(Option)
admin.site.register(Shop)
admin.site.register(Subjects)
admin.site.register(User)
admin.site.register(UserConfirmation)