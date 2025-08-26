from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum, Avg

from .models import DailyStat, WeeklyGoal, FriendRequest, SharedWeeklySummary
from .serializers import DailyStatSerializer, WeeklyGoalSerializer, FriendRequestSerializer, SharedWeeklySummarySerializer
from .permissions import IsOwnerOrReadOnly

class DailyStatViewSet(viewsets.ModelViewSet):
    serializer_class = DailyStatSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        qs = DailyStat.objects.filter(user=self.request.user)
        date_from = self.request.query_params.get("date_from")
        date_to = self.request.query_params.get("date_to")
        if date_from:
            qs = qs.filter(date__gte=date_from)
        if date_to:
            qs = qs.filter(date__lte=date_to)
        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class WeeklyGoalViewSet(viewsets.ModelViewSet):
    serializer_class = WeeklyGoalSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        return WeeklyGoal.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class FriendRequestViewSet(viewsets.ModelViewSet):
    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Return requests where the user is sender or receiver
        user = self.request.user
        return FriendRequest.objects.filter(models.Q(from_user=user) | models.Q(to_user=user))

    @action(detail=True, methods=["post"])
    def respond(self, request, pk=None):
        # accept or reject
        fr = self.get_object()
        if fr.to_user != request.user:
            return Response({"detail": "Not allowed"}, status=status.HTTP_403_FORBIDDEN)
        action = request.data.get("action")
        if action not in ("accept", "reject"):
            return Response({"detail": "action must be 'accept' or 'reject'."}, status=status.HTTP_400_BAD_REQUEST)
        fr.status = "ACCEPTED" if action == "accept" else "REJECTED"
        fr.responded_at = timezone.now()
        fr.save()
        return Response({"status": fr.status})

class SharedWeeklySummaryViewSet(viewsets.ModelViewSet):
    serializer_class = SharedWeeklySummarySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return SharedWeeklySummary.objects.filter(models.Q(owner=user) | models.Q(shared_with=user)).distinct()
    
#Views for Tracker App :Getting the weekly summary
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils.dateparse import parse_date

from .metrics import get_weekly_summary

class WeeklySummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Optional query params: start_date & end_date
        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")

        if start_date:
            start_date = parse_date(start_date)
        if end_date:
            end_date = parse_date(end_date)

        summary = get_weekly_summary(request.user, start_date, end_date)
        return Response(summary)




