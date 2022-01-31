from django.contrib import admin
from .models import NewStories, ShowStories, AskStories, JobStories

# Register your models here.

class NewsCategoryAdmin(admin.ModelAdmin):
    list_display = ('id_news', 'title', 'time')
    list_display_links = ('id_news', 'title')
    search_fields = ('title',)

admin.site.register(AskStories, NewsCategoryAdmin)
admin.site.register(NewStories, NewsCategoryAdmin)
admin.site.register(ShowStories, NewsCategoryAdmin)
admin.site.register(JobStories, NewsCategoryAdmin)