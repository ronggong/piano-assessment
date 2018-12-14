import librosa
from parser.midi_parser import mid_note_parser
from parser.txt_parser import sv_score_parser
from align import alignment
from segmentation import notes_segmenation
from tempo_estimation import indices_segment_start_end
from tempo_estimation import streching_student_notes

def pitch_difference(p_t, p_s):
    """
    absolute pitch difference
    p_t: teacher pitch in midi note
    p_s: student pitch in midi note
    """
    return abs(p_t - p_s)

def duration_difference(d_t, d_s):
    """
    absolute duration difference
    d_t: teacher note duration in s
    d_s: student note duration in s
    """
    return abs(d_t - d_s)

def ioi(onset, onset_previous):
    """
    Inter-onset interval
    onset: note onset in s
    onset_previous: previous note onset in s
    """
    return onset - onset_previous

def ioi_difference(ioi_t, ioi_s):
    """
    Inter-onset interval difference
    ioi_t: teacher ioi
    ioi_s: student ioi
    """
    return abs(ioi_t - ioi_s)

def beat_diviation(onset_s, onset_first_s, tempo_s):
    """
    The deviation of student note onset from the beat grid
    """
    bd =  (onset_s - onset_first_s) % (float(60)/tempo_s)
    bd = bd if bd <= 0.5 else 1-bd
    return bd

def all_features(list_score_seg, tempo_s):
    """
    Calculate features of each student note
    output: list of [pitch difference, beat deviation, ioi difference, duration difference, missing note, extra note]
    """
    # onset_first_t = 0.
    onset_first_s = 0.
    onset_previous_t = 0.
    onset_previous_s = 0.
    ind_onset_first_t = 0
    ind_onset_first_s = 0
    list_features = []

    for ii in range(len(list_score_seg)):
        if len(list_score_seg[ii][0]):
            # onset_first_t = list_score_seg[ii][0][0]
            onset_previous_t = list_score_seg[ii][0][0]
            ind_onset_first_t = ii
            break
    for ii in range(len(list_score_seg)):
        if len(list_score_seg[ii][1]):
            onset_first_s = list_score_seg[ii][1][0]
            onset_previous_s = list_score_seg[ii][1][0]
            ind_onset_first_s = ii
            break

    for ii in range(len(list_score_seg)):
        if len(list_score_seg[ii][0]) and len(list_score_seg[ii][1]):
            extra = False
            missing = False
            ioi_diff = ioi_difference(list_score_seg[ii][0][0] - onset_previous_t, list_score_seg[ii][1][0] - onset_previous_s)
            pitch_diff = pitch_difference(list_score_seg[ii][0][1], list_score_seg[ii][1][1])
            dur_diff = duration_difference(list_score_seg[ii][0][2], list_score_seg[ii][1][2])
            beat_div = beat_diviation(list_score_seg[ii][1][0], onset_first_s, tempo_s)
            onset_previous_t = list_score_seg[ii][0][0] 
            onset_previous_s = list_score_seg[ii][1][0]
        if not len(list_score_seg[ii][0]):
            extra = True
            missing = False
            ioi_diff = None
            pitch_diff = None
            dur_diff = None
            beat_div = None
            onset_previous_s = list_score_seg[ii][1][0]
        if not len(list_score_seg[ii][1]):
            extra = False
            missing = True
            ioi_diff = None
            pitch_diff = None
            dur_diff = None
            beat_div = None
            onset_previous_t = list_score_seg[ii][0][0]
        
        if ii == ind_onset_first_t or ii == ind_onset_first_s:
            ioi_diff = None
        if ii == ind_onset_first_s:
            beat_div = None

        list_features.append([pitch_diff, beat_div, ioi_diff, dur_diff, missing, extra])

    return list_features

def features_student(wav_t, wav_s, midi_t, annotation_txt_s, plot_align=False):
    y_t, sr_t = librosa.load(wav_t, sr=None)
    y_s, sr_s = librosa.load(wav_s, sr=None)

    # load score of sonic visualizer
    score_t = mid_note_parser(midi_t)
    score_s = sv_score_parser(annotation_txt_s)
    
    list_score_aligned = alignment(y_t, y_s, sr_t, sr_s, score_t, score_s, plot=plot_align)

    score_s_segmented = notes_segmenation(score_s, list_score_aligned)

    segment_start_end = indices_segment_start_end(list_score_aligned, score_s_segmented)

    list_score_aligned_seg, _, list_tempo_s = streching_student_notes(list_score_aligned, segment_start_end)

    list_features = []
    for ii in range(len(list_score_aligned_seg)):
        list_features_seg = all_features(list_score_aligned_seg[ii], list_tempo_s[ii])
        list_features += list_features_seg
    
    list_features_student = []
    for ii in range(len(list_score_aligned)):
        if len(list_score_aligned[ii][1]):
            list_features_student.append(list_features[ii])
    return list_features_student

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
    
    list_features = []
    for ii in range(len(list_score_aligned_seg)):
        list_features_seg = all_features(list_score_aligned_seg[ii], list_tempo_s[ii])
        list_features += list_features_seg
    
    list_features_student = []
    for ii in range(len(list_score_aligned)):
        if len(list_score_aligned[ii][1]):
            list_features_student.append(list_features[ii])
