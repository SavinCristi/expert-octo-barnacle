from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0001_initial'),
    ]

    operations = [
        # Add email with a temporary empty-string default so the migration
        # can backfill any existing rows (there are none in this DB, but
        # this keeps the migration portable).  The AlterField that follows
        # immediately drops that default, matching the model definition.
        migrations.AddField(
            model_name='reservation',
            name='email',
            field=models.EmailField(default='', max_length=254),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='reservation',
            name='status',
            field=models.CharField(
                choices=[
                    ('pending',   'În Așteptare'),
                    ('confirmed', 'Confirmat'),
                    ('cancelled', 'Anulat'),
                ],
                default='pending',
                max_length=20,
            ),
        ),
    ]
