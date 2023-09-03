# ======================== Rest API Dependency ===================================#
from rest_framework.response import Response
from rest_framework.decorators import api_view
from base.models import Texttospeech
from ..serializers import TexttospeechSerializer

# ======================== Syntesize Dependency ===================================#
import os
import scipy.io.wavfile as wavfile

import numpy as np
import torch
import json
from .hparams import create_hparams
from .model import Tacotron2
from .text import text_to_sequence
from .layers import TacotronSTFT
from .audio_processing import griffin_lim
from . import *
from .env import AttrDict
from .meldataset import MAX_WAV_VALUE
from .models import Generator


# ===========================================================================================
# ------------------  Syntesize Initialization ----------------------------------------------
# =========================================================================================== 

def get_hifigan():
    conf = "D:/fiinal/MOAN/Backend/KIYA/api/main/SAVE_out/config_v1.json"
    with open(conf) as f:
        json_config = json.loads(f.read())
    h = AttrDict(json_config)
    torch.manual_seed(h.seed)
    hifigan = Generator(h).to(torch.device("cuda"))
    state_dict_g = torch.load("D:/fiinal/MOAN/Backend/KIYA/api/main/SAVE_out/Hifigan", map_location=torch.device("cuda"))
    hifigan.load_state_dict(state_dict_g["generator"])
    hifigan.eval()
    hifigan.remove_weight_norm()
    return hifigan, h

def has_MMI(STATE_DICT):
    return any(True for x in STATE_DICT.keys() if "mi." in x)

def get_Tactron2():
 # Load Tacotron2 and Config
    hparams = create_hparams()
    hparams.sampling_rate = 22050
    hparams.max_decoder_steps = 3000 # Max Duration
    hparams.gate_threshold = 0.25 # Model must be 25% sure the clip is over before ending generation
    model = Tacotron2(hparams)
    state_dict = torch.load("D:/fiinal/MOAN/Backend/KIYA/api/main/SAVE_out/Amharic_last")['state_dict']
    if has_MMI(state_dict):
        raise Exception("ERROR: This notebook does not currently support MMI models.")
    model.load_state_dict(state_dict)
    _ = model.cuda().eval().half()
    return model, hparams

# Extra Info
def infer(text, pronounciation_dictionary, show_graphs, file_name):
    for i in [x for x in text.split("\n") if len(x)]:
        if not pronounciation_dictionary:
            if i[-1] != ";": i=i+";" 
        else: i = ARPA(i)
        with torch.no_grad(): # save VRAM by not including gradients
            sequence = np.array(text_to_sequence(i, ['english_cleaners']))[None, :]
            sequence = torch.autograd.Variable(torch.from_numpy(sequence)).cuda().long()
            mel_outputs, mel_outputs_postnet, _, alignments = model.inference(sequence)
            if show_graphs:
                plot_data((mel_outputs_postnet.float().data.cpu().numpy()[0],
                        alignments.float().data.cpu().numpy()[0].T))
            y_g_hat = hifigan(mel_outputs_postnet.float())
            audio = y_g_hat.squeeze()
            audio = audio * MAX_WAV_VALUE
            print("")

            # ---------------------------------------------------------------------------------------------
            wavfile.write(file_name, hparams.sampling_rate,audio.cpu().numpy().astype("int16")) 
            # ---------------------------------------------------------------------------------------------


hifigan,h = get_hifigan()
model,hparams = get_Tactron2()



# ===========================================================================================
# ------------------  API Requests ----------------------------------------------------------
# ===========================================================================================

@api_view(['GET'])
def getData(request):
    """GET all recorded tts requests from database. 
    """
    tts = Texttospeech.objects.all()
    serializer = TexttospeechSerializer(tts, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def addTTS(request):
    """Fetch the text  from the json api request and
    syntesize with the file name saved from the variable below.
    """
    text = request.data.get('text')  # Get the value of the 'text' field from the request data | ይህህን ስራ ለመጨረስ ከ ወር በላይ ፈጅቶብኛል አሁን ደሞ ጓደኛዬ ያግዘኛል በጣም ደስ ብሎኛል
    file_name = "D:/fiinal/MOAN/Backend/KIYA/api/main/wav_file_save/the_new_one.wav"  # Location of the audio file
    infer(text,False,False,file_name) # fetch the text and file name from the api request and syntesize 

    serializer = TexttospeechSerializer(data=request.data) # Serialize data

    if serializer.is_valid():
        """Check if data is valid then save data in database
        """
        serializer.save(audio=file_name)  # Assign the 'audio' value to the serializer
        return Response(serializer.data, status=201) # If all good return a success status 201
    return Response(serializer.errors, status=400) # If post request fail return status 400
