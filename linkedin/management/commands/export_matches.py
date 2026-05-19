import csv
import os
from datetime import datetime
from django.core.management.base import BaseCommand
from crm.models import Lead, Deal
from linkedin.enums import ProfileState

class Command(BaseCommand):
    help = "Export matched leads to a CSV file."

    def handle(self, *args, **options):
        # Query matched leads not yet exported
        leads = Lead.objects.filter(is_match=True, exported_to_csv=False)
        
        if not leads.exists():
            self.stdout.write("No new matches to export.")
            return

        os.makedirs("exports", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"exports/matches_{timestamp}.csv"

        with open(filename, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["LinkedIn URL", "Name", "Current Title", "Similarity Score", "Talking Points"])
            
            for lead in leads:
                # Find the most recent deal to get talking points (reason)
                deal = Deal.objects.filter(lead=lead).order_by("-update_date").first()
                talking_points = deal.reason if deal else ""
                
                # We don't store name/title in DB, using public_identifier as placeholder
                writer.writerow([
                    lead.linkedin_url,
                    lead.public_identifier,
                    "N/A", # Placeholder for Title
                    f"{lead.similarity_score:.4f}" if lead.similarity_score else "0.0000",
                    talking_points
                ])
                
                lead.exported_to_csv = True
                lead.save(update_fields=["exported_to_csv"])

        self.stdout.write(f"Successfully exported {leads.count()} matches to {filename}")
