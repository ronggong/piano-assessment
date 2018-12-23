def sv_score_parser(filename):
    """
    parse score into notes
    """
    with open(filename, "r") as file_handle:
        lines_score = file_handle.readlines()
        list_note = []
        for ls in lines_score:
            note = ls.split('\t')
            list_note.append([float(note[0]), int(note[1]), float(note[2])])
    return list_note

def sv_score_annotation_parser(filename):
    """
    parse score into note annotation
    """
    with open(filename, "r") as file_handle:
        lines_score = file_handle.readlines()
        list_annotation = []
        for ls in lines_score:
            note = ls.split('\t')
            annotation = note[4].strip().split(' ')
            if len(annotation) == 5:
                note_annotation = annotation[4].replace('\n', '')
            else:
                note_annotation = "00000"
            list_annotation.append(note_annotation)
    return list_annotation

def sv_score_annotation_parser_manual_aligned(filename):
    return 