from django.db.models import fields
from rest_framework import serializers

from .models import UserNote

class NoteSerializer(serializers.ModelSerializer):
  class Meta:
    model = UserNote
    fields = '__all__'

  def create(self, validated_data):
    note = UserNote.objects.create(**validated_data)
    note.save()
    return note 
