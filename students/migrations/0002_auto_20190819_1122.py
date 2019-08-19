# Generated by Django 2.1 on 2019-08-19 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='student_class_designation',
            field=models.CharField(max_length=1, null=True, verbose_name='Class Designation'),
        ),
        migrations.AddField(
            model_name='student',
            name='student_grade',
            field=models.IntegerField(null=True, verbose_name='Grade'),
        ),
        migrations.AlterField(
            model_name='sport',
            name='achievement',
            field=models.CharField(max_length=100, verbose_name='Students Achievement'),
        ),
        migrations.AlterField(
            model_name='sport',
            name='sport_played',
            field=models.CharField(max_length=100, verbose_name='Sport Name'),
        ),
        migrations.AlterField(
            model_name='sport',
            name='year_participated',
            field=models.IntegerField(verbose_name='Year Participated'),
        ),
        migrations.AlterField(
            model_name='student',
            name='student_admno',
            field=models.IntegerField(primary_key=True, serialize=False, verbose_name='Admin Number'),
        ),
        migrations.AlterField(
            model_name='student',
            name='student_classcode',
            field=models.CharField(max_length=10, verbose_name='Class Code'),
        ),
        migrations.AlterField(
            model_name='student',
            name='student_firstname',
            field=models.CharField(max_length=50, verbose_name='First Name'),
        ),
        migrations.AlterField(
            model_name='student',
            name='student_fullname',
            field=models.CharField(max_length=200, verbose_name='Full Name'),
        ),
        migrations.AlterField(
            model_name='student',
            name='student_gender',
            field=models.CharField(max_length=10, verbose_name='Gender'),
        ),
        migrations.AlterField(
            model_name='student',
            name='student_lastname',
            field=models.CharField(max_length=50, verbose_name='Last Name'),
        ),
        migrations.AlterField(
            model_name='student',
            name='student_middlename',
            field=models.CharField(blank=True, max_length=50, verbose_name='Middle Name'),
        ),
    ]
