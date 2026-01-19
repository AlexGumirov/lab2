from django.db import migrations, models
import django.db.models.deletion


def seed_country_sport(apps, schema_editor):
    Country = apps.get_model("leagues", "Country")
    Sport = apps.get_model("leagues", "Sport")
    League = apps.get_model("leagues", "League")

    # populate reference tables from existing League data
    for league in League.objects.all():
        country_obj, _ = Country.objects.get_or_create(name=getattr(league, "country", None) or "")
        sport_obj, _ = Sport.objects.get_or_create(name=getattr(league, "sport", None) or "")
        league.country_fk = country_obj
        league.sport_fk = sport_obj
        league.save(update_fields=["country_fk", "sport_fk"])


class Migration(migrations.Migration):
    dependencies = [
        ("leagues", "0002_rename_leagues_lea_country_5a7c36_idx_leagues_lea_country_713330_idx_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Country",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=128, unique=True)),
            ],
            options={
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="Sport",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=128, unique=True)),
            ],
            options={
                "ordering": ["name"],
            },
        ),
        migrations.AddField(
            model_name="league",
            name="country_fk",
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name="+", to="leagues.country"),
        ),
        migrations.AddField(
            model_name="league",
            name="sport_fk",
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name="+", to="leagues.sport"),
        ),
        migrations.RunPython(seed_country_sport, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="league",
            name="country_fk",
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="leagues", to="leagues.country"),
        ),
        migrations.AlterField(
            model_name="league",
            name="sport_fk",
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="leagues", to="leagues.sport"),
        ),
        migrations.RemoveField(
            model_name="league",
            name="country",
        ),
        migrations.RemoveField(
            model_name="league",
            name="sport",
        ),
        migrations.RenameField(
            model_name="league",
            old_name="country_fk",
            new_name="country",
        ),
        migrations.RenameField(
            model_name="league",
            old_name="sport_fk",
            new_name="sport",
        ),
    ]


