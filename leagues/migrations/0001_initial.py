from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="League",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("league_id", models.CharField(max_length=32, unique=True)),
                ("name", models.CharField(max_length=255)),
                ("country", models.CharField(max_length=128)),
                ("sport", models.CharField(max_length=128)),
                ("revenue_usd", models.DecimalField(blank=True, decimal_places=2, max_digits=16, null=True)),
                ("avg_player_salary_usd", models.DecimalField(blank=True, decimal_places=2, max_digits=16, null=True)),
                ("top_team", models.CharField(blank=True, max_length=255, null=True)),
                ("total_teams", models.PositiveIntegerField(blank=True, null=True)),
                ("founded_year", models.PositiveIntegerField(blank=True, null=True)),
                ("viewership", models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
            ],
            options={
                "indexes": [
                    models.Index(fields=["country"], name="leagues_lea_country_5a7c36_idx"),
                    models.Index(fields=["sport"], name="leagues_lea_sport_2a2c10_idx"),
                    models.Index(fields=["revenue_usd"], name="leagues_lea_revenu_2e8c39_idx"),
                ],
            },
        )
    ]


