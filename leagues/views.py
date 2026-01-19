from django.db.models import Avg, Count, Max, Min, Sum, Q
from django.shortcuts import render

from .models import League, Team


def dashboard(request):
    qs = League.objects.all()

    stats_counts = {
        "Лиг": qs.count(),
        "Стран": qs.values("country__name").distinct().count(),
        "Видов спорта": qs.values("sport__name").distinct().count(),
        "Команд": Team.objects.count(),
    }

    overall_stats = qs.aggregate(
        total_revenue=Sum("revenue_usd"),
        avg_revenue=Avg("revenue_usd"),
        max_revenue=Max("revenue_usd"),
        min_revenue=Min("revenue_usd"),
        avg_salary=Avg("avg_player_salary_usd"),
        max_salary=Max("avg_player_salary_usd"),
        min_salary=Min("avg_player_salary_usd"),
        avg_viewership=Avg("viewership"),
    )

    overall_rows = [
        {"Метрика": "Суммарная выручка (USD)", "Значение": overall_stats.get("total_revenue")},
        {"Метрика": "Средняя выручка (USD)", "Значение": overall_stats.get("avg_revenue")},
        {"Метрика": "Макс. выручка (USD)", "Значение": overall_stats.get("max_revenue")},
        {"Метрика": "Мин. выручка (USD)", "Значение": overall_stats.get("min_revenue")},
        {"Метрика": "Средняя зарплата игрока (USD)", "Значение": overall_stats.get("avg_salary")},
        {"Метрика": "Макс. зарплата игрока (USD)", "Значение": overall_stats.get("max_salary")},
        {"Метрика": "Мин. зарплата игрока (USD)", "Значение": overall_stats.get("min_salary")},
        {"Метрика": "Средняя аудитория (Viewership)", "Значение": overall_stats.get("avg_viewership")},
    ]

    top_by_revenue_rows = [
        {
            "League ID": l.league_id,
            "League Name": l.name,
            "Country": l.country.name,
            "Sport": l.sport.name,
            "Revenue (USD)": l.revenue_usd,
            "Top Team": l.top_team,
        }
        for l in qs.order_by("-revenue_usd")[:20]
    ]

    top_by_salary_rows = [
        {
            "League ID": l.league_id,
            "League Name": l.name,
            "Country": l.country.name,
            "Sport": l.sport.name,
            "Average Player Salary (USD)": l.avg_player_salary_usd,
            "Top Team": l.top_team,
        }
        for l in qs.order_by("-avg_player_salary_usd")[:20]
    ]

    country_agg = list(
        qs.values("country__name")
        .annotate(
            leagues=Count("id"),
            total_revenue=Sum("revenue_usd"),
            avg_revenue=Avg("revenue_usd"),
            avg_salary=Avg("avg_player_salary_usd"),
            avg_viewership=Avg("viewership"),
        )
        .order_by("-total_revenue")[:20]
    )
    top_countries_rows = [
        {
            "Country": c["country__name"],
            "Лиг": c["leagues"],
            "Суммарная выручка (USD)": c["total_revenue"],
            "Средняя выручка (USD)": c["avg_revenue"],
            "Средняя зарплата (USD)": c["avg_salary"],
            "Средняя аудитория": c["avg_viewership"],
        }
        for c in country_agg
    ]

    sport_agg = list(
        qs.values("sport__name")
        .annotate(
            leagues=Count("id"),
            total_revenue=Sum("revenue_usd"),
            avg_salary=Avg("avg_player_salary_usd"),
            avg_viewership=Avg("viewership"),
        )
        .order_by("-total_revenue")[:20]
    )
    top_sports_rows = [
        {
            "Sport": s["sport__name"],
            "Лиг": s["leagues"],
            "Суммарная выручка (USD)": s["total_revenue"],
            "Средняя зарплата (USD)": s["avg_salary"],
            "Средняя аудитория": s["avg_viewership"],
        }
        for s in sport_agg
    ]

    teams_by_sport = list(
        Team.objects.values("league__sport__name")
        .annotate(teams=Count("id"), top_teams=Count("id", filter=Q(is_top_team=True)))
        .order_by("-teams")
    )

    context = {
        "stats_counts": stats_counts,
        "overall_rows": overall_rows,
        "top_by_revenue_rows": top_by_revenue_rows,
        "top_by_salary_rows": top_by_salary_rows,
        "top_countries_rows": top_countries_rows,
        "top_sports_rows": top_sports_rows,
        "teams_rows": [
            {
                "Team": t.name,
                "League": t.league.name,
                "Country": t.league.country.name,
                "Sport": t.league.sport.name,
                "Is Top Team": t.is_top_team,
            }
            for t in Team.objects.select_related("league", "league__country", "league__sport").all()[:200]
        ],
        "teams_by_sport_rows": [
            {"Sport": r["league__sport__name"], "Teams": r["teams"], "Top Teams": r["top_teams"]} for r in teams_by_sport
        ],
    }
    return render(request, "leagues/dashboard.jinja2", context)


