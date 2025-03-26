from django.contrib import admin
from .models import Article, AdminForm

class ArticleDisplayAdmin(admin.ModelAdmin):
    form = AdminForm # menulis ulang form pada admin agar bisa ditambahkan error pada field form terserbut
    list_display = ['views', 'title', 'id', 'datetime_added']
    readonly_fields = ['datetime_added', 'datetime_updated', 'views']

admin.site.register(Article, ArticleDisplayAdmin) # model utama dan model displayadminnya harus berada pada satu admin.site.register()