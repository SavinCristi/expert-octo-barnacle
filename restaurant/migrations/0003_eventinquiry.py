from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0002_reservation_email_reservation_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventInquiry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True,
                                           serialize=False, verbose_name='ID')),
                ('name',             models.CharField(max_length=200)),
                ('phone',            models.CharField(max_length=20)),
                ('email',            models.EmailField(max_length=254)),
                ('desired_date',     models.DateField()),
                ('event_type', models.CharField(
                    choices=[
                        ('wedding',   'Nuntă'),
                        ('corporate', 'Corporate'),
                        ('party',     'Petrecere Privată'),
                        ('other',     'Altceva'),
                    ],
                    max_length=20,
                )),
                ('estimated_guests', models.PositiveSmallIntegerField()),
                ('message',          models.TextField(blank=True)),
                ('status', models.CharField(
                    choices=[
                        ('new',       'Nou'),
                        ('contacted', 'Contactat'),
                        ('closed',    'Închis'),
                    ],
                    default='new',
                    max_length=20,
                )),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now,
                                                    editable=False)),
            ],
            options={
                'verbose_name':        'Event Inquiry',
                'verbose_name_plural': 'Event Inquiries',
                'ordering':            ['-created_at'],
            },
        ),
    ]
