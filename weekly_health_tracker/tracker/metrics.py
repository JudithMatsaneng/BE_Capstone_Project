#Tracker App
from datetime import timedelta
from django.utils import timezone
from .models import DailyStat, Goal

def get_weekly_summary(user, start_date=None, end_date=None):
    """
    Returns totals and averages for the user's activities over a 7-day window 
    (or a custom date range if provided).
    """
    # The default will be the last 7 days
    if not end_date:
        end_date = timezone.now().date()
    if not start_date:
        start_date = end_date - timedelta(days=6)

    stats = DailyStat.objects.filter(user=user, date__range=[start_date, end_date])

    total_steps = sum(stat.steps for stat in stats)
    total_sleep = sum(stat.sleep_hours for stat in stats)
    total_calories = sum(stat.calories for stat in stats)

    count = stats.count() or 1  

    summary = {
        "date_range": f"{start_date} to {end_date}",
        "total_steps": total_steps,
        "average_steps": total_steps // count,
        "total_sleep_hours": total_sleep,
        "average_sleep_hours": round(total_sleep / count, 1),
        "total_calories": total_calories,
        "average_calories": total_calories // count,
    }

    # A comparison with goals set for the week if they exist. 
    goals = Goal.objects.filter(user=user).last()
    if goals:
        summary["goals"] = {
            "target_steps": goals.target_steps,
            "progress_steps": f"{total_steps}/{goals.target_steps}",
            "target_sleep": goals.target_sleep_hours,
            "progress_sleep": f"{total_sleep}/{goals.target_sleep_hours}",
            "target_calories": goals.target_calories,
            "progress_calories": f"{total_calories}/{goals.target_calories}",
        }

    return summary



