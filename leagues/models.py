from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=128, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Sport(models.Model):
    name = models.CharField(max_length=128, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class League(models.Model):
    league_id = models.CharField(max_length=32, unique=True)
    name = models.CharField(max_length=255)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="leagues")
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE, related_name="leagues")

    revenue_usd = models.DecimalField(max_digits=16, decimal_places=2, null=True, blank=True)
    avg_player_salary_usd = models.DecimalField(max_digits=16, decimal_places=2, null=True, blank=True)

    top_team = models.CharField(max_length=255, null=True, blank=True)
    total_teams = models.PositiveIntegerField(null=True, blank=True)
    founded_year = models.PositiveIntegerField(null=True, blank=True)
    viewership = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=["revenue_usd"]),
        ]

    def __str__(self) -> str:
        return f"{self.name} ({self.league_id})"


class Team(models.Model):
    name = models.CharField(max_length=255)
    league = models.ForeignKey(League, on_delete=models.CASCADE, related_name="teams")
    is_top_team = models.BooleanField(default=False)

    class Meta:
        unique_together = ("league", "name")
        indexes = [
            models.Index(fields=["league"]),
            models.Index(fields=["is_top_team"]),
        ]

    def __str__(self) -> str:
        return f"{self.name} ({self.league.name})"


