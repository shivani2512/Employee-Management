# Generated by Django 2.2.1 on 2019-06-19 19:13

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emp', '0010_auto_20190619_1839'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='Image',
            field=models.ImageField(blank=True, upload_to='profile_pic'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='Joining_date',
            field=models.DateField(default=datetime.date(2019, 6, 20)),
        ),
    ]
