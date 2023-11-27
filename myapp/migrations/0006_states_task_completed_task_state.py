# Generated by Django 4.2.7 on 2023-11-24 18:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_alter_task_datecompleted'),
    ]

    operations = [
        migrations.CreateModel(
            name='States',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.CharField(max_length=25)),
            ],
        ),
        migrations.AddField(
            model_name='task',
            name='completed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='task',
            name='state',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.DO_NOTHING, to='myapp.states'),
        ),
    ]
