from rest_framework import serializers
from base.models import Texttospeech

class TexttospeechSerializer(serializers.ModelSerializer):
    class Meta:
        model = Texttospeech
        fields = '__all__'