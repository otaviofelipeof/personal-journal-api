from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import JournalEntry
from .permissions import IsOwner
from .serializers import JournalEntrySerializer


class JournalEntryViewSet(viewsets.ModelViewSet):

    serializer_class = JournalEntrySerializer
    permission_classes = [IsOwner]

    def get_queryset(self):

        user = self.request.user

        if user.groups.filter(name='Editor').exists():
            return JournalEntry.objects.all()

        return JournalEntry.objects.filter(
            author=user
        )

    def perform_create(self, serializer):

        serializer.save(
            author=self.request.user
        )

    @action(
        detail=False,
        methods=['get'],
        permission_classes=[AllowAny],
        url_path='public'
    )
    def public_entries(self, request):

        entries = JournalEntry.objects.filter(
            is_public=True
        )

        serializer = self.get_serializer(
            entries,
            many=True
        )

        return Response(serializer.data)
