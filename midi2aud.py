from midi2audio import FluidSynth

def save_midi_2_audio(input_midi, output_wav):
    fs = FluidSynth()
    fs.midi_to_audio(input_midi, output_wav)