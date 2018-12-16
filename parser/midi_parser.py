import pretty_midi

def mid_note_parser(filename):
    """
    Parse midi note sequence ([note_start, note_pitch, note_dur], ...)
    """
    midi_note_seq = []
    midi_data = pretty_midi.PrettyMIDI(filename)
    for instrument in midi_data.instruments:
        if not instrument.is_drum:
            for note in instrument.notes:
                midi_note_seq.append([note.start, note.pitch, note.end-note.start])
    return midi_note_seq