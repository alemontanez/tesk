# Generated by Django 4.2.7 on 2023-11-24 19:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0011_rename_states_taskstates_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='TaskStates',
            new_name='TaskCondition',
        ),
        migrations.RenameField(
            model_name='taskcondition',
            old_name='task_state',
            new_name='task_condition',
        ),
    ]
