import csv
from decimal import Decimal, InvalidOperation

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from leagues.models import Country, Sport, League, Team


class Command(BaseCommand):
    help = "Import top_expensive_leagues CSV into League model"

    def add_arguments(self, parser):
        parser.add_argument("--path", required=True, help="Path to CSV file")
        parser.add_argument("--limit", type=int, default=0, help="Limit rows (0 = no limit)")

    @transaction.atomic
    def handle(self, *args, **opts):
        path = opts["path"]
        limit = opts["limit"]

        try:
            f = open(path, "r", encoding="utf-8", newline="")
        except FileNotFoundError:
            raise CommandError(f"CSV not found: {path}")

        reader = csv.DictReader(f)
        if not reader.fieldnames:
            raise CommandError("CSV has no header row")

        processed = 0
        created = 0
        updated = 0
        skipped = 0

        def to_int(v):
            try:
                if v is None:
                    return None
                s = str(v).strip()
                if s == "":
                    return None
                return int(Decimal(s))
            except Exception:
                return None

        def to_decimal(v):
            try:
                if v is None:
                    return None
                s = str(v).strip()
                if s == "":
                    return None
                return Decimal(s)
            except (InvalidOperation, ValueError):
                return None

        for row in reader:
            processed += 1
            if limit and processed > limit:
                break

            league_id = (row.get("League ID") or "").strip()
            name = (row.get("League Name") or "").strip()
            country_name = (row.get("Country") or "").strip()
            sport_name = (row.get("Sport") or "").strip()

            if not league_id or not name:
                skipped += 1
                continue

            revenue = to_decimal(row.get("Revenue (USD)"))
            avg_salary = to_decimal(row.get("Average Player Salary (USD)"))
            top_team = (row.get("Top Team") or "").strip() or None
            total_teams = to_int(row.get("Total Teams"))
            founded_year = to_int(row.get("Founded Year"))
            viewership = to_decimal(row.get("Viewership"))

            country_obj, _ = Country.objects.get_or_create(name=country_name or "Unknown")
            sport_obj, _ = Sport.objects.get_or_create(name=sport_name or "Unknown")

            obj, was_created = League.objects.update_or_create(
                league_id=league_id,
                defaults={
                    "name": name,
                    "country": country_obj,
                    "sport": sport_obj,
                    "revenue_usd": revenue,
                    "avg_player_salary_usd": avg_salary,
                    "top_team": top_team,
                    "total_teams": total_teams,
                    "founded_year": founded_year,
                    "viewership": viewership,
                },
            )

            # create/update top team as related entity for 3rd level
            if top_team:
                Team.objects.update_or_create(
                    league=obj,
                    name=top_team,
                    defaults={"is_top_team": True},
                )

            if was_created:
                created += 1
            else:
                updated += 1

            if processed % 1000 == 0:
                self.stdout.write(f"Processed {processed} rows...")

        f.close()

        self.stdout.write(self.style.SUCCESS("Import finished."))
        self.stdout.write(f"Rows processed: {processed}")
        self.stdout.write(f"Created: {created}, Updated: {updated}, Skipped: {skipped}")


