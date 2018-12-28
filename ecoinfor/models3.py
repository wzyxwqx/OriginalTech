# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class CnstockNews(models.Model):
    title = models.TextField(blank=True, null=True)
    url = models.CharField(max_length=200, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    time = models.DateTimeField(blank=True, null=True)
    source = models.CharField(max_length=80, blank=True, null=True)
    keystock = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cnstock_news'


class ConsultantShare(models.Model):
    name_text = models.CharField(max_length=20)
    intro_text = models.CharField(max_length=1000)
    company_text = models.CharField(max_length=200)
    hot_index = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'consultant_share'


class CsNews(models.Model):
    title = models.TextField(blank=True, null=True)
    url = models.CharField(max_length=200, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    time = models.DateTimeField(blank=True, null=True)
    source = models.CharField(max_length=80, blank=True, null=True)
    keystock = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cs_news'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey('UsersUser', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class JrjNews(models.Model):
    title = models.TextField(blank=True, null=True)
    url = models.CharField(max_length=200, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    time = models.DateTimeField(blank=True, null=True)
    source = models.CharField(max_length=80, blank=True, null=True)
    keyword = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'jrj_news'


class NbdNews(models.Model):
    title = models.TextField(blank=True, null=True)
    url = models.CharField(max_length=200, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    time = models.DateTimeField(blank=True, null=True)
    abstract = models.TextField(blank=True, null=True)
    source = models.CharField(max_length=80, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'nbd_news'


class News(models.Model):
    title = models.TextField(blank=True, null=True)
    url = models.CharField(max_length=200, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    time = models.DateTimeField(blank=True, null=True)
    source = models.CharField(max_length=80, blank=True, null=True)
    keywords = models.TextField(blank=True, null=True)
    topic = models.CharField(max_length=100, blank=True, null=True)
    website = models.CharField(max_length=50, blank=True, null=True)
    abstract = models.TextField(blank=True, null=True)
    keystock = models.TextField(blank=True, null=True)
    senti = models.IntegerField(blank=True, null=True)
    senti1 = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'news'


class RecomandStock(models.Model):
    time = models.DateTimeField(blank=True, null=True)
    stockcode = models.CharField(max_length=20, blank=True, null=True)
    pchange_1 = models.FloatField(blank=True, null=True)
    pchange_2 = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'recomand_stock'


class RecommendationNews(models.Model):
    title_text = models.CharField(max_length=20)
    context_text = models.CharField(max_length=1000)
    pub_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'recommendation_news'


class SentiStat(models.Model):
    time = models.DateTimeField(blank=True, null=True)
    total = models.IntegerField(blank=True, null=True)
    good = models.IntegerField(blank=True, null=True)
    bad = models.IntegerField(blank=True, null=True)
    stockcode = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'senti_stat'


class SinaNews(models.Model):
    title = models.TextField(blank=True, null=True)
    url = models.CharField(max_length=200, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    time = models.DateTimeField(blank=True, null=True)
    source = models.CharField(max_length=50, blank=True, null=True)
    keywords = models.CharField(max_length=100, blank=True, null=True)
    topic = models.CharField(max_length=100, blank=True, null=True)
    keystock = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sina_news'


class SinaNewsCopy(models.Model):
    id = models.IntegerField()
    title = models.CharField(max_length=100, blank=True, null=True)
    url = models.CharField(max_length=100, blank=True, null=True)
    content = models.CharField(max_length=5000, blank=True, null=True)
    time = models.DateTimeField(blank=True, null=True)
    source = models.CharField(max_length=50, blank=True, null=True)
    keywords = models.CharField(max_length=100, blank=True, null=True)
    topic = models.CharField(max_length=100, blank=True, null=True)
    keystock = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sina_news_copy'


class StcnNews(models.Model):
    title = models.TextField(blank=True, null=True)
    url = models.CharField(max_length=200, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    time = models.DateTimeField(blank=True, null=True)
    source = models.CharField(max_length=80, blank=True, null=True)
    keystock = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'stcn_news'


class TempNews(models.Model):
    title = models.TextField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    time = models.DateTimeField(blank=True, null=True)
    source = models.CharField(max_length=80, blank=True, null=True)
    keywords = models.TextField(blank=True, null=True)
    abstract = models.TextField(blank=True, null=True)
    keystock = models.TextField(blank=True, null=True)
    senti = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'temp_news'


class UsersUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()
    nickname = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'users_user'


class UsersUserGroups(models.Model):
    user = models.ForeignKey(UsersUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'users_user_groups'
        unique_together = (('user', 'group'),)


class UsersUserUserPermissions(models.Model):
    user = models.ForeignKey(UsersUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'users_user_user_permissions'
        unique_together = (('user', 'permission'),)
