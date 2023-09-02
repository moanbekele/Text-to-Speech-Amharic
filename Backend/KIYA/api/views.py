from rest_framework.response import Response
from rest_framework.decorators import api_view
from base.models import Texttospeech
from .serializers import TexttospeechSerializer
from django.templatetags.static import static
from django.http import JsonResponse



@api_view(['GET'])
def getData(request):
    tts = Texttospeech.objects.all()
    serializer = TexttospeechSerializer(tts, many=True)
    return Response(serializer.data)

# @api_view(['POST'])
# def addTTS(request):
#     serializer = TexttospeechSerializer(data=request.data)
#     if serializer.is_valid():
#         print(serializer.validated_data[]['audio'] )
#         serializer.save()
#     return Response(serializer.validated_data)

@api_view(['POST'])
def addTTS(request):
    ############################################################################################################

    text_value = request.data.get('text')  # Get the value of the 'text' field from the request data
    audio_location = "source/voice.wav"  # Location of the audio file
    
    ############################################################################################################
    #serializer = TexttospeechSerializer(data=request.data)
    serializer = ''

    # Generate the URL of the audio file
    audio_url = static(audio_location)
    
    return JsonResponse({'audio_url': audio_url}, status=201)


    