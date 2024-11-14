from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Task
from .serializers import TaskSerializer

class TaskListCreateView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Only return tasks for the logged-in user
        if self.request.user.is_staff:
            return Task.objects.all()  # Admin users see all tasks
        return Task.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Set the logged-in user as the owner of the task
        serializer.save(user=self.request.user)

class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        task = self.get_object()
        if task.user != request.user and not request.user.is_staff:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        task = self.get_object()
        if task.user != request.user:
            return Response({"detail": "You do not have permission to edit this task."}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        task = self.get_object()
        if task.user != request.user:
            return Response({"detail": "You do not have permission to delete this task."}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)
