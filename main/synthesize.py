import os
import scipy.io.wavfile as wavfile

import numpy as np
import torch
import json
from .hparams import create_hparams
from .model import Tacotron2
from .layers import TacotronSTFT
from .audio_processing import griffin_lim
from .text import text_to_sequence
from .env import AttrDict
from .meldataset import MAX_WAV_VALUE
from .models import Generator

def get_hifigan():
    conf = "main/SAVE_out/config_v1.json"
    with open(conf) as f:
        json_config = json.loads(f.read())
    h = AttrDict(json_config)
    torch.manual_seed(h.seed)
    hifigan = Generator(h).to(torch.device("cuda"))
    state_dict_g = torch.load("main/SAVE_out/Hifigan", map_location=torch.device("cuda"))
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
    state_dict = torch.load("main/SAVE_out/Amharic_last")['state_dict']
    if has_MMI(state_dict):
        raise Exception("ERROR: This notebook does not currently support MMI models.")
    model.load_state_dict(state_dict)
    _ = model.cuda().eval().half()
    return model, hparams
# count = 0
# Extra Info
def infer(text, pronounciation_dictionary, show_graphs):
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
            ###############################################################################################
            # count = 0
            if os.path.exists(f'source/voice_0.wav'):
                os.remove(f'source/voice_0.wav')
            wavfile.write(f"source/voice_0.wav", hparams.sampling_rate,audio.cpu().numpy().astype("int16")) 
            return f'source/voice_0.wav'

            ###############################################################################################
###############################################################################################
# ---------------------------------------------------------------------------------------------
hifigan,h = get_hifigan()
model,hparams = get_Tactron2()

def text2speech(text):
    
    return infer(text,False,False)