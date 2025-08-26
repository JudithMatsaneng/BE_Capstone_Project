from django.db import models
from django.contrib.auth.models import User

class DailyStat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="daily_stats")
    date = models.DateField()
    steps = models.PositiveIntegerField(default=0)
    sleep_hours = models.DecimalField(max_digits=4, decimal_places=2, default=0)  
    calories_consumed = models.PositiveIntegerField(default=0)
    diet = models.TextField(blank=True, null=True)
    exercises = models.TextField(blank=True, null=True) 

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("user", "date")
        ordering = ["-date"]

    def __str__(self):
        return f"{self.user.username} — {self.date}"

class WeeklyGoal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="weekly_goals")
    week_start = models.DateField(help_text="The week starting date (e.g., Monday)")
    target_steps = models.PositiveIntegerField(default=0)
    target_sleep_hours = models.PositiveIntegerField(default=0)  
    target_calories = models.PositiveIntegerField(default=0)     
    notes = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("user", "week_start")
        ordering = ["-week_start"]

    def __str__(self):
        return f"{self.user.username} goal week {self.week_start}"

class FriendRequest(models.Model):
    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("ACCEPTED", "Accepted"),
        ("REJECTED", "Rejected"),
    ]
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_friend_requests")
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_friend_requests")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="PENDING")
    created_at = models.DateTimeField(auto_now_add=True)
    responded_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        unique_together = ("from_user", "to_user")

    def __str__(self):
        return f"{self.from_user} -> {self.to_user} ({self.status})"

class SharedWeeklySummary(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="shared_summaries")
    week_start = models.DateField()
    shared_with = models.ManyToManyField(User, related_name="summaries_shared_to_me", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("owner", "week_start")

    def __str__(self):
        return f"{self.owner.username} shared week {self.week_start}"

