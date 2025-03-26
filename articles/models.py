from django import forms
from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_save, post_save
from django.contrib import admin
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from multiselectfield import MultiSelectField
from ckeditor.fields import RichTextField
import random

category_list = (
    ("tips", "Tips"),
    ("education", "Education"),
    ("technology", "Technology"),
    ("science", "Science"),
    ("world", "World"),
    ("economy", "Economy"),
    ("lifestyle", "Life Style"),
    ("football", "Football"),
    ("politics", "Politics"),
    ("sports", "Sports"),
)

class Article(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(null=True, blank=True, unique=True)
    intro = RichTextField()
    image = models.ImageField(upload_to="images/", null=True, blank= True)
    image_alt = models.CharField(max_length=200, default="image")
    body = RichTextField()
    category = MultiSelectField(max_choices=3, choices=category_list)
    topic = models.CharField(max_length=64, help_text="Pisahkan setiap kategori dengan tanda koma ' , ' dan spasi.")
    editors_pick = models.BooleanField(default=False)
    datetime_added = models.DateTimeField(auto_now_add=True)
    date_added = models.DateField(auto_now_add=True)
    datetime_updated = models.DateTimeField(auto_now=True)
    views = models.PositiveIntegerField(default=0)
    keyword = models.TextField(editable=False)
    s_id = models.IntegerField(null=True, blank=True) # editable pada s_id harus bernilai True dan s_id tidak boleh berada di 'readonly_fields' agar fungsi clean "def clean(self):" dibawah dapat mengaksesnya.
    def main_category(self):
        return str(self.category).split(", ")[0]
    def topics(self):
        return self.topic.split(", ")
    def related_articles(self):
        str_lookups = ""
        for i in range(len(self.topics())):
            str_lookups += f" | Q(topic__icontains=self.topics()[{i}])"
        lookups = eval(f"{str_lookups[3:]}")
        related_articles = Article.objects.filter(lookups).order_by('-views', '-date_added').exclude(id=self.id)
        return related_articles
    def url(self):
        return reverse('article', kwargs={'slug': self.slug})
    def save(self):
        self.slug = slugify(self.title)
        self.keyword = self.title + " " + self.intro + " " + self.body + " " + self.topic
        super(Article, self).save()

def s_id_save(sender, instance, created, *args, **kwargs): # fungsi def s_id_save() ini digunakan untuk mendapatkan s_id(show_id) dari id article setelah article disave, s_id ini akan digunakan untuk pengecualian dalam penambahan error pada fungsi def clean() ketika ada title yang sama, sehingga object article yang sedang diedit tidak termasuk kedalamnya.
    if created:
        instance.s_id = instance.id
        instance.save()
post_save.connect(s_id_save, Article)

class AdminForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = '__all__'
    def clean(self):
        data = self.cleaned_data
        s_id = data.get('s_id')
        title = data.get('title')
        try:# mencegah terjadinya error ketika terjadi ValueError pada field 'title'. (fungsi ini dilakukan karena ini merupakan form admin baru sehingga beberapa 'adderror' perlu diatur ulang).
            qs = Article.objects.filter(title__iexact=title).exclude(s_id=s_id)
            if qs.exists():
                self.add_error("title", f"Judul \"{title}\" telah digunakan.")
        except:
            pass
        return data

# Author of this template: @arjunahmad66