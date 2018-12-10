# import essentia.standard as ess
import matplotlib.pyplot as plt
import librosa
from parser.midi_parser import mid_note_parser
from parser.txt_parser import sv_score_parser
from segmentation import notes_segmenation
from align import alignment
import pretty_midi

# audio_t = ess.MonoLoader(filename="./test/seconds(t).wav")()
# audio_s = ess.MonoLoader(filename="./test/seconds1(s).wav")()
# audio_t /= max(audio_t)
# audio_s /= max(audio_s)

# RHYTHM = ess.RhythmExtractor2013(method="degara")

# bpm_t, ticks_t, _, _, bpmIntervals_t = RHYTHM(audio_t)
# bpm_s, ticks_s, _, _, bpmIntervals_s = RHYTHM(audio_s)

# f, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
# ax1.plot(bpmIntervals_t)
# ax2.plot(bpmIntervals_s)
# plt.show()

def get_tempo_segment(seg):
    piano_seg = pretty_midi.PrettyMIDI()
    piano_program = pretty_midi.instrument_name_to_program('Acoustic Grand Piano')
    piano = pretty_midi.Instrument(program=piano_program)
    for note in seg:
        note_midi = pretty_midi.Note(
        velocity=100, pitch=note[1], start=note[0], end=note[0]+note[2])
        piano.notes.append(note_midi)
    piano_seg.instruments.append(piano)
    return piano_seg.estimate_tempo()


if __name__ == "__main__":
    y_t, sr_t = librosa.load("./test/seconds(t).wav", sr=None)
    y_s, sr_s = librosa.load("./test/seconds1(s).wav", sr=None)

    # load score of sonic visualizer
    score_t = mid_note_parser("./test/seconds(t).mid")
    score_s = sv_score_parser("./test/seconds1(s).txt")
    
    list_score_aligned = alignment(y_t, y_s, sr_t, sr_s, score_t, score_s)

    score_s_segmented = notes_segmenation(score_s)

    segment_start_end = []
    for note_seq_s in score_s_segmented:
        num_t_start, num_t_end = 0, 0
        num_s_start = note_seq_s[0][3]
        num_s_end = note_seq_s[-1][3]
        for ii, note_t_s in enumerate(list_score_aligned):
            if len(note_t_s[1]):
                if note_t_s[1][3] == num_s_start:
                    num_t_start = ii
                if note_t_s[1][3] == num_s_end:
                    num_t_end = ii
        segment_start_end.append([num_t_start, num_t_end])
    
    for num_seg in segment_start_end:
        seg_t = [note_t_s[0] for note_t_s in list_score_aligned[num_seg[0]: num_seg[1]+1] if len(note_t_s[0])]
        seg_s = [note_t_s[1] for note_t_s in list_score_aligned[num_seg[0]: num_seg[1]+1] if len(note_t_s[1])]
        tempo_t = get_tempo_segment(seg_t)
        tempo_s = get_tempo_segment(seg_s)
        print(tempo_t, tempo_s)

        seg_s = [[note_s[0]*tempo_s/tempo_t, note_s[1], note_s[2]*tempo_s/tempo_t] for note_s in seg_s]
        tempo_s = get_tempo_segment(seg_s)
        print(tempo_t, tempo_s)