# Generated by Django 2.1.3 on 2018-12-18 08:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(error_messages={'required': 'Add a title for your article.'}, max_length=255)),
                ('description', models.TextField(error_messages={'required': 'Add a description for your article.'})),
                ('body', models.TextField(error_messages={'required': 'Add a body for your article.'})),
                ('user_rating', models.CharField(default='0', max_length=10)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('image_url', models.CharField(max_length=255, null=True)),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('favourites_count', models.IntegerField(default=0)),
            ],
            options={
                'ordering': ['-created_on', 'author'],
                'get_latest_by': 'created_on',
            },
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rated_on', models.DateTimeField(auto_now_add=True)),
                ('score', models.DecimalField(decimal_places=2, max_digits=5)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scores', to='article.Article')),
            ],
            options={
                'ordering': ['-score'],
            },
        ),
    ]
