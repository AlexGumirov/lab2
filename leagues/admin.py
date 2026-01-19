from django.contrib import admin

from .models import Country, Sport, League, Team


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Sport)
class SportAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(League)
class LeagueAdmin(admin.ModelAdmin):
    list_display = (
        "league_id",
        "name",
        "country",
        "sport",
        "revenue_usd",
        "avg_player_salary_usd",
        "total_teams",
        "founded_year",
        "viewership",
    )
    search_fields = ("league_id", "name", "country__name", "sport__name", "top_team")
    list_filter = ("country", "sport")


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ("name", "league", "is_top_team")
    search_fields = ("name", "league__name")
    list_filter = ("is_top_team", "league__sport", "league__country")


