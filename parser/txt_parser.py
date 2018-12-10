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