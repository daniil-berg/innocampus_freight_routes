# Generated by Django 3.0.3 on 2020-02-27 15:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('cost', models.FloatField(verbose_name='Cost')),
            ],
            options={
                'verbose_name': 'Link',
                'verbose_name_plural': 'Links',
            },
        ),
        migrations.CreateModel(
            name='Map',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(blank=True, max_length=255, null=True, verbose_name='Map Title')),
                ('user', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='maps', related_query_name='map', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Map',
                'verbose_name_plural': 'Maps',
            },
        ),
        migrations.CreateModel(
            name='Node',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('pos_h', models.IntegerField(verbose_name='Horizontal Position')),
                ('pos_v', models.IntegerField(verbose_name='Vertical Position')),
                ('direct_successors', models.ManyToManyField(related_name='direct_predecessors', related_query_name='direct_predecessor', through='rail_network.Link', to='rail_network.Node', verbose_name='Nodes linked to')),
                ('map', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='nodes', related_query_name='node', to='rail_network.Map', verbose_name='Map')),
            ],
            options={
                'verbose_name': 'Node',
                'verbose_name_plural': 'Nodes',
            },
        ),
        migrations.AddField(
            model_name='link',
            name='head',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='incoming_links', related_query_name='incoming_link', to='rail_network.Node', verbose_name='"to"-Node'),
        ),
        migrations.AddField(
            model_name='link',
            name='tail',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='outgoing_links', related_query_name='outgoing_link', to='rail_network.Node', verbose_name='"from"-Node'),
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='City name')),
                ('node', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='rail_network.Node', verbose_name='Node')),
            ],
            options={
                'verbose_name': 'City',
                'verbose_name_plural': 'Cities',
            },
        ),
        migrations.AddConstraint(
            model_name='node',
            constraint=models.UniqueConstraint(fields=('map', 'pos_h', 'pos_v'), name='exclusive_position'),
        ),
    ]
