from django.contrib import admin

from .models import Video, Comment, User, Task, CommentTask

admin.site.register(Video)
admin.site.register(Comment)
admin.site.register(CommentTask)
admin.site.register(User)
admin.site.register(Task)

