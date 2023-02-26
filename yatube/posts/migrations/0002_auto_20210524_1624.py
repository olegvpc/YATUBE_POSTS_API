# Generated by Django 2.2.9 on 2021-05-24 16:24
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True,
                 serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='')),
                ('slug', models.SlugField(default='', unique=True)),
                ('description', models.TextField(blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='group',
            field=models.ForeignKey(blank=True, null=True,
                                    on_delete=django.db.models.deletion.
                                    SET_NULL, to='posts.Group'),
        ),
    ]
