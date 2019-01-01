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

def sv_score_transcribed_parser(filename):
    """
    parse transcribed score with annotation into notes
    """
    with open(filename, "r") as file_handle:
        lines_score = file_handle.readlines()
        list_note = []
        list_annotation = []
        for ls in lines_score:
            note = ls.split('\t')
            print(note)
            if len(note) == 3:
                list_annotation.append("00000")
            else:
                list_annotation.append(note[3].replace('\n', ''))
            list_note.append([float(note[0]), int(note[1]), float(note[2].replace('\n', ''))])
    return list_note, list_annotation

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
    """
    parse score into with manual annotation
    """
    with open(filename, "r") as file_handle:
        lines_score = file_handle.readlines()
        list_annotation = []
        list_note_aligned = []
        ctr_teacher, ctr_student = 0, 0
        for ls in lines_score:
            note = ls.split('\t')
            annotation = note[4].strip().split(' ')
            if len(annotation) == 5:
                note_annotation = annotation[4].replace('\n', '')
            else:
                note_annotation = "00000"
            list_annotation.append(note_annotation)

            if len(note) == 10:
                list_note_aligned.append([[float(note[5]), float(note[6]), float(note[7]), ctr_teacher], 
                                         [float(note[0]), float(note[1]), float(note[2]), ctr_student]])
                ctr_teacher += 1
                ctr_student += 1
            elif len(note) == 5:
                list_note_aligned.append([[], [float(note[0]), float(note[1]), float(note[2]), ctr_student]])
                ctr_student += 1
            else:
                raise ValueError("Not a valid note list length {}".format(len(note)))
    return list_annotation, list_note_aligned

def sv_score_annotation_parser_manual_aligned(filename):
    """
    parse manual annotation
    """
    list_annotation = []
    list_score_aligned = []
    with open(filename, "r") as file_handle:
        lines = file_handle.readlines()
        tidx = 0
        for sidx, line in enumerate(lines):
            label, teacher_data, student_data = parse_manual_line(line)
            list_annotation.append(label)
            if teacher_data:
                list_score_aligned.append([teacher_data + [tidx], student_data + [sidx]])
                tidx += 1
            else:
                list_score_aligned.append([[], student_data + [sidx]])
    return list_annotation, list_score_aligned

def parse_manual_line(line):
    """
    helper function for parsing manual aligned files
    """
    line = line.split('\t')
    # get the student data
    student_data = [float(line[0]), int(line[1]), float(line[2])]
    # get the teacher data
    if len(line) > 5:
        teacher_data = [float(line[5]), int(line[6]), float(line[7])]
    else:
        teacher_data = []
    # get the annotation label
    ant_data = line[4].split()
    if len(ant_data[-1]) == 5 and set(ant_data[-1]).issubset({'0', '1', '2'}):
        label = ant_data[-1]
    else:
        label = "0" * 5
    return label, teacher_data, student_data
