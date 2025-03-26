# Generated by Django 3.2.20 on 2023-08-11 23:39

import ckeditor.fields
from django.db import migrations, models
import multiselectfield.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('slug', models.SlugField(blank=True, null=True, unique=True)),
                ('intro', ckeditor.fields.RichTextField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('image_alt', models.CharField(default='image', max_length=200)),
                ('body', ckeditor.fields.RichTextField()),
                ('category', multiselectfield.db.fields.MultiSelectField(choices=[('tips', 'Tips'), ('education', 'Education'), ('technology', 'Technology'), ('science', 'Science'), ('world', 'World'), ('economy', 'Economy'), ('lifestyle', 'Life Style'), ('football', 'Football'), ('politics', 'Politics'), ('sports', 'Sports')], max_length=82)),
                ('topic', models.CharField(help_text="Pisahkan setiap kategori dengan tanda koma ' , ' dan spasi.", max_length=64)),
                ('editors_pick', models.BooleanField(default=False)),
                ('datetime_added', models.DateTimeField(auto_now_add=True)),
                ('date_added', models.DateField(auto_now_add=True)),
                ('datetime_updated', models.DateTimeField(auto_now=True)),
                ('views', models.PositiveIntegerField(default=0)),
                ('keyword', models.TextField(editable=False)),
                ('s_id', models.IntegerField(blank=True, null=True)),
            ],
        ),
    ]
