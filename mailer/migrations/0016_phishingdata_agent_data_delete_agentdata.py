# Generated by Django 4.0.5 on 2022-07-26 02:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailer', '0015_remove_phishingdatadict_agent_data_agentdata'),
    ]

    operations = [
        migrations.AddField(
            model_name='phishingdata',
            name='agent_data',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.DeleteModel(
            name='AgentData',
        ),
    ]
