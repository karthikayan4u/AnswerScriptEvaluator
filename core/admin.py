from core.models import Answers, Questions, Scores
from django.contrib import admin

class UserAdmin(admin.ModelAdmin):
    search_fields = [
        'user__username']

# Register your models here.
admin.site.register(Questions)
admin.site.register(Answers, UserAdmin)
admin.site.register(Scores, UserAdmin)
