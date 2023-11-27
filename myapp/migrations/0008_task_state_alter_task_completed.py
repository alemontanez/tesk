# Generated by Django 4.2.7 on 2023-11-24 18:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0007_remove_task_state'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='state',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='myapp.states'),
        ),
        migrations.AlterField(
            model_name='task',
            name='completed',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
