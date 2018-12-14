from parser.txt_parser import sv_score_parser

def notes_segmenation(list_note, list_score_aligned, inter_note_threshold=2.0, segment_dur=10.0):
    """
    Segmentation the student note sequence with two criteria:
    1. current note start - previous note end > inter note time threshold
    2. current note start - first note start of the segment > segment duration
    output: [[segment_0], [segment_1], ...], segment = [[note_0], [note_1], ...], note = [start, midi, dur, note_number]
    """
    ind_student_extra_stop = 0
    list_note_entire = []
    list_note_segment = []

    for ii in range(len(list_score_aligned)):
        if not len(list_score_aligned[ii][0]):
            list_note_segment.append(list_note[ii] + [ii])
        else:
            ind_student_extra_stop = ii
            break
    if len(list_note_segment):
        list_note_entire.append(list_note_segment)

    list_note_segment = [list_note[ind_student_extra_stop]+[ind_student_extra_stop]]
    first_note_start = list_note[ind_student_extra_stop][0]

    for ii in range(ind_student_extra_stop, len(list_note)-1):
        previous_note_end = list_note[ii][0] + list_note[ii][2]
        current_note_start = list_note[ii+1][0]
        if current_note_start - previous_note_end > inter_note_threshold or current_note_start - first_note_start > segment_dur:
            list_note_entire.append(list_note_segment)
            list_note_segment = [list_note[ii+1]+[ii+1]]
            first_note_start = list_note[ii+1][0]
        else:
            list_note_segment.append(list_note[ii+1]+[ii+1])
    list_note_entire.append(list_note_segment)

    return list_note_entire
        

if __name__ == "__main__":
    student_annotation = "./test/seconds1(s).txt"
    list_note = sv_score_parser(student_annotation)
    list_note_segmented = notes_segmenation(list_note, None)
    for list_note_seg in list_note_segmented:
        print(list_note_seg)