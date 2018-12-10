from midi2audio import FluidSynth

fs = FluidSynth()
input_midi = "./seconds(t).mid"
output_wav = "./seconds(t).wav"
fs.midi_to_audio(input_midi, output_wav)

input_midi = "./seconds1(s).mid"
output_wav = "./seconds1(s).wav"
fs.midi_to_audio(input_midi, output_wav)