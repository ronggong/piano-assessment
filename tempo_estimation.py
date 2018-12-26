# import essentia.standard as ess
import matplotlib.pyplot as plt
import librosa
from parser.midi_parser import mid_note_parser
from parser.txt_parser import sv_score_parser
from segmentation import notes_segmenation
from align import alignment
import pretty_midi
import copy


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

def indices_segment_start_end(list_score_aligned, score_s_segmented):
    """
    Input:
        list_score_aligned: [[note_teacher_0, note_student_0], [note_teacher_1, note_student_1], ...]
        score_s_segmented: student score segmented, [[note_0, note_1,...], [note_n, note_n+1], ...]
    Output:
        segment start and end indices of list_score_aligned: [[segment_start_ind, segment_end_ind], [...], ...]
    """
    last_end_num = 0
    segment_start_end = [] # segment start and end indices
    for note_seq_s in score_s_segmented:
        # print(note_seq_s)
        num_t_start, num_t_end = 0, 0
        num_s_start = note_seq_s[0][3]
        num_s_end = note_seq_s[-1][3]
        for ii, note_t_s in enumerate(list_score_aligned):
            if len(note_t_s[1]):
                if note_t_s[1][3] == num_s_start:
                    num_t_start = ii
                if note_t_s[1][3] == num_s_end:
                    num_t_end = ii
        # print(num_t_start)
        # # force the end of the last index of the segment end = the current segment start number - 1
        # force the beginning of the current index of the segment = the index of the last segment end
        if num_t_start > last_end_num + 1 and len(segment_start_end):
            num_t_start_orig = num_t_start # this index, list_score_aligned list has note
            # segment_start_end[-1][1] = num_t_start - 1
            num_t_start = last_end_num + 1
        elif not len(segment_start_end) and num_t_start > 0:
            num_t_start = 0
            num_t_start_orig = 0
        else:
            num_t_start_orig = last_end_num + 1
        last_end_num = num_t_end
        # print(num_t_start)
        # print(list_score_aligned[num_t_start_orig], list_score_aligned[num_t_end])
        # print(segment_start_end)
        # TODO implement the minimum note restriction for teacher's segment
        # print(len(list_score_aligned), num_t_start_orig, last_end_num)
        if len(segment_start_end) and list_score_aligned[num_t_end][1][3] - list_score_aligned[num_t_start_orig][1][3] < 2:
            segment_start_end[-1][1] = num_t_end
        else:
            segment_start_end.append([num_t_start, num_t_end])
        # print(num_t_start)
    if segment_start_end[-1][1] < len(list_score_aligned)-1:
        segment_start_end[-1][1] = len(list_score_aligned)-1
    return segment_start_end
    
def streching_student_notes(list_score_aligned, segment_start_end):
    """
    Streching the student note onset and duration according to the tempo
    Input:
        list_score_aligned: [[note_teacher_0, note_student_0], [note_teacher_1, note_student_1], ...]
        segment_start_end: [[segment_start_ind, segment_end_ind], [...], ...]
    Output:
        time strenched list_score_aligned: [seg_0, seg_1, ... ]
    """
    list_score_aligned_seg = []
    list_score_aligned_copy = copy.deepcopy(list_score_aligned)
    list_tempo_t = []
    list_tempo_s = []
    # print(segment_start_end)
    for num_seg in segment_start_end:
        # print(num_seg)
        # print(list_score_aligned[num_seg[0]: num_seg[1]+1])
        seg_t = [note_t_s[0] for note_t_s in list_score_aligned[num_seg[0]: num_seg[1]+1] if len(note_t_s[0])]
        seg_s = [note_t_s[1] for note_t_s in list_score_aligned[num_seg[0]: num_seg[1]+1] if len(note_t_s[1])]
        
        if len(seg_t):
            tempo_t = get_tempo_segment(seg_t)
        else:
            tempo_t = None
        if len(seg_s) and tempo_t:
            tempo_s = get_tempo_segment(seg_s)
        else:
            tempo_s = None

        list_score_seg = []
        for ii in range(num_seg[0], num_seg[1]+1):
            if len(list_score_aligned[ii][1]) and tempo_t:
                list_score_aligned_copy[ii][1][0] = list_score_aligned[ii][1][0]*tempo_s/tempo_t
                list_score_aligned_copy[ii][1][2] = list_score_aligned[ii][1][2]*tempo_s/tempo_t
            list_score_seg.append(list_score_aligned_copy[ii])
        list_score_aligned_seg.append(list_score_seg)

        # print("before strech {}, {}".format(tempo_t, tempo_s))
        if tempo_s:
            seg_s = [[note_s[0]*tempo_s/tempo_t, note_s[1], note_s[2]*tempo_s/tempo_t] for note_s in seg_s]
            tempo_s = get_tempo_segment(seg_s)
            list_tempo_t.append(tempo_t)
            list_tempo_s.append(tempo_s)
            # print("after strech {}, {}".format(tempo_t, tempo_s))
        else:
            list_tempo_t.append(None)
            list_tempo_s.append(None)

    return list_score_aligned_seg, list_tempo_t, list_tempo_s


if __name__ == "__main__":
    y_t, sr_t = librosa.load("./test/seconds(t).wav", sr=None)
    y_s, sr_s = librosa.load("./test/seconds1(s).wav", sr=None)

    # load score of sonic visualizer
    score_t = mid_note_parser("./test/seconds(t).mid")
    score_s = sv_score_parser("./test/seconds1(s).txt")
    
    list_score_aligned = alignment(y_t, y_s, sr_t, sr_s, score_t, score_s)

    score_s_segmented = notes_segmenation(score_s, list_score_aligned)

    segment_start_end = indices_segment_start_end(list_score_aligned, score_s_segmented)

    list_score_aligned_seg, list_tempo_t, list_tempo_s = streching_student_notes(list_score_aligned, segment_start_end)

    for seg in list_score_aligned_seg:
        print(seg)
    
    print(list_tempo_t)
    print(list_tempo_s)
