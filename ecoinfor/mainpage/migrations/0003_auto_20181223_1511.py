# Generated by Django 2.1.2 on 2018-12-23 07:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainpage', '0002_delete_share'),
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(blank=True, null=True)),
                ('url', models.CharField(blank=True, max_length=200, null=True)),
                ('content', models.TextField(blank=True, null=True)),
                ('time', models.DateTimeField(blank=True, null=True)),
                ('source', models.CharField(blank=True, max_length=80, null=True)),
                ('keywords', models.TextField(blank=True, null=True)),
                ('topic', models.CharField(blank=True, max_length=100, null=True)),
                ('website', models.CharField(blank=True, max_length=50, null=True)),
                ('abstract', models.TextField(blank=True, null=True)),
                ('keystock', models.TextField(blank=True, null=True)),
                ('senti', models.IntegerField(blank=True, null=True)),
                ('senti1', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'news',
                'managed': False,
            },
        ),
        migrations.DeleteModel(
            name='Market',
        ),
        migrations.DeleteModel(
            name='Message',
        ),
    ]
