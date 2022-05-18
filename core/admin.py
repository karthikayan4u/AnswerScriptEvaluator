from core.models import Answer, Question, Score
from django.contrib import admin

class UserAdmin(admin.ModelAdmin):
    search_fields = [
        'user__username']

# Register your models here.
admin.site.register(Question)
admin.site.register(Answer, UserAdmin)
admin.site.register(Score, UserAdmin)
admin.site.site_url = "http://127.0.0.1:8000/"
