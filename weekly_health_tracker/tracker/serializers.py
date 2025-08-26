from rest_framework import serializers
from .models import DailyStat, WeeklyGoal, FriendRequest, SharedWeeklySummary
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email")

class DailyStatSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = DailyStat
        fields = ("id", "user", "date", "steps", "sleep_hours", "calories_consumed", "diet", "exercises", "created_at", "updated_at")
        read_only_fields = ("id", "user", "created_at", "updated_at")

    def validate(self, attrs):
        # basic guards
        if attrs.get("steps", 0) < 0:
            raise serializers.ValidationError({"steps": "Cannot be negative."})
        if attrs.get("sleep_hours", 0) < 0:
            raise serializers.ValidationError({"sleep_hours": "Cannot be negative."})
        if attrs.get("calories_consumed", 0) < 0:
            raise serializers.ValidationError({"calories_consumed": "Cannot be negative."})
        return attrs

class WeeklyGoalSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")
    class Meta:
        model = WeeklyGoal
        fields = ("id", "user", "week_start", "target_steps", "target_sleep_hours", "target_calories", "notes", "created_at", "updated_at")
        read_only_fields = ("id", "user", "created_at", "updated_at")

class FriendRequestSerializer(serializers.ModelSerializer):
    from_user = serializers.ReadOnlyField(source="from_user.username")
    to_user_username = serializers.CharField(write_only=True, required=True)  

    class Meta:
        model = FriendRequest
        fields = ("id", "from_user", "to_user_username", "status", "created_at", "responded_at")
        read_only_fields = ("id", "from_user", "status", "created_at", "responded_at")

    def create(self, validated_data):
        to_username = validated_data.pop("to_user_username")
        to_user = User.objects.get(username=to_username)
        request_obj = FriendRequest.objects.create(from_user=self.context["request"].user, to_user=to_user)
        return request_obj

class SharedWeeklySummarySerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")
    shared_with_usernames = serializers.ListField(child=serializers.CharField(), write_only=True, required=False)

    class Meta:
        model = SharedWeeklySummary
        fields = ("id", "owner", "week_start", "shared_with_usernames", "created_at")
        read_only_fields = ("id", "owner", "created_at")

    def create(self, validated_data):
        usernames = validated_data.pop("shared_with_usernames", [])
        owner = self.context["request"].user
        s = SharedWeeklySummary.objects.create(owner=owner, **validated_data)
        for u in usernames:
            try:
                user_obj = User.objects.get(username=u)
                s.shared_with.add(user_obj)
            except User.DoesNotExist:
                continue
        return s

