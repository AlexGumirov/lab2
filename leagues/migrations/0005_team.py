from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("leagues", "0004_remove_league_leagues_lea_country_713330_idx_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Team",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=255)),
                ("is_top_team", models.BooleanField(default=False)),
                ("league", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="teams", to="leagues.league")),
            ],
            options={
                "unique_together": {("league", "name")},
            },
        ),
        migrations.AddIndex(
            model_name="team",
            index=models.Index(fields=["league"], name="leagues_tea_league_6bea60_idx"),
        ),
        migrations.AddIndex(
            model_name="team",
            index=models.Index(fields=["is_top_team"], name="leagues_tea_is_top__cad8c2_idx"),
        ),
    ]


