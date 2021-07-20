# Generated by Django 2.2.16 on 2020-09-16 14:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('environments', '0014_auto_20200917_1032'),
    ]

    operations = [
        # Separate DB and state as we're just moving traits into their own app.
        # To do this, we're simply reusing the old table.
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.AlterUniqueTogether(
                    name='trait',
                    unique_together=None,
                ),
                migrations.RemoveField(
                    model_name='trait',
                    name='identity',
                ),
                migrations.DeleteModel(
                    name='Trait',
                ),
            ],
            # don't do anything with the db as we're just reusing the existing table
            database_operations=[]
        ),
        # historical traits aren't used for anything so can be removed
        # as part of this refactor
        migrations.DeleteModel(
            name='HistoricalTrait',
        ),
    ]
