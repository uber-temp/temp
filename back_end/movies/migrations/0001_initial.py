# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Distributor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('latitude', models.DecimalField(max_digits=4, decimal_places=2, validators=[django.core.validators.MinValueValidator(-0.0), django.core.validators.MaxValueValidator(90.0)])),
                ('longitude', models.DecimalField(max_digits=5, decimal_places=2, validators=[django.core.validators.MinValueValidator(-180.0), django.core.validators.MaxValueValidator(180.0)])),
            ],
            options={
                'select_on_save': True,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('year', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1900), django.core.validators.MaxValueValidator(2015)])),
                ('fun_fact', models.CharField(max_length=500, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProductionCompany',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='movie',
            name='actors',
            field=models.ManyToManyField(related_name='acted_movies', null=True, to='movies.Person', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='movie',
            name='director',
            field=models.ForeignKey(related_name='directed_movies', to='movies.Person'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='movie',
            name='distributor',
            field=models.ForeignKey(blank=True, to='movies.Distributor', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='movie',
            name='production_company',
            field=models.ForeignKey(blank=True, to='movies.ProductionCompany', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='movie',
            name='writer',
            field=models.ForeignKey(related_name='wrote_movies', blank=True, to='movies.Person', null=True),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='movie',
            unique_together=set([('title', 'year', 'director')]),
        ),
        migrations.AddField(
            model_name='location',
            name='movie',
            field=models.ForeignKey(related_name='locations', to='movies.Movie'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='location',
            unique_together=set([('movie', 'name')]),
        ),
    ]
