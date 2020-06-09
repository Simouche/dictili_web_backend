# Generated by Django 3.0.2 on 2020-05-14 20:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AudioFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted', models.BooleanField(default=False)),
                ('file_location', models.FileField(upload_to='C:\\Users\\Simou\\Desktop\\PFE\\web_backend\\dictili\\uploads\\generated\\audio')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Word',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted', models.BooleanField(default=False)),
                ('word', models.CharField(max_length=255, unique=True)),
                ('context', models.ManyToManyField(blank=True, related_name='_word_context_+', to='document_generation.Word')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted', models.BooleanField(default=False)),
                ('type', models.CharField(choices=[('p', 'Prescription'), ('r', 'Report')], max_length=3)),
                ('text', models.CharField(max_length=2048)),
                ('text_file', models.FileField(upload_to='reports')),
                ('audio_file', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to='document_generation.AudioFile')),
                ('words', models.ManyToManyField(to='document_generation.Word')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
