# Generated by Django 2.2.6 on 2021-06-28 18:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_auto_20210601_0714'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='group',
            options={'verbose_name': 'Группа по интересам', 'verbose_name_plural': 'Группы по интересам'},
        ),
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ('-pub_date',), 'verbose_name': 'Пост пользователя', 'verbose_name_plural': 'Посты пользователей'},
        ),
    ]
