# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

class Companies(models.Model):
    company_ticker = models.CharField(primary_key=True, max_length=255)
    company_name = models.CharField(max_length=255)
    sector = models.CharField(max_length=255)
    exchange = models.CharField(max_length=255)
    website = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'companies'


class News(models.Model):
    article_id = models.AutoField(primary_key=True)
    company_ticker = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    article_url = models.CharField(max_length=255)
    url_image = models.CharField(max_length=255)
    article_description = models.CharField(max_length=10000)
    date_published = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'news'


class Stocks(models.Model):
    date = models.DateTimeField()
    company_ticker = models.CharField(primary_key=True, max_length=255)
    open = models.DecimalField(max_digits=65535, decimal_places=65535)
    high = models.DecimalField(max_digits=65535, decimal_places=65535)
    low = models.DecimalField(max_digits=65535, decimal_places=65535)
    close = models.DecimalField(max_digits=65535, decimal_places=65535)
    volume = models.DecimalField(max_digits=65535, decimal_places=65535)
    dividends = models.DecimalField(max_digits=65535, decimal_places=65535)

    class Meta:
        managed = False
        db_table = 'stocks'
        unique_together = (('company_ticker', 'date'),)


class Tweets(models.Model):
    tweet_id = models.AutoField(primary_key=True)
    company_ticker = models.CharField(max_length=255)
    tweet_url = models.CharField(max_length=255)
    tweet_content = models.CharField(max_length=300)
    date_published = models.DateTimeField()
    follower_count = models.IntegerField()
    sentiment = models.FloatField()

    class Meta:
        managed = False
        db_table = 'tweets'
