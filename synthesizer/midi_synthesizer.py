import pretty_midi

def notes2midi(list_notes, output_midi):
    # Create a PrettyMIDI object
    midi_obj = pretty_midi.PrettyMIDI()
    # Create an Instrument instance for a piano instrument
    piano_program = pretty_midi.instrument_name_to_program('Acoustic Grand Piano')
    piano = pretty_midi.Instrument(program=piano_program)
    # Iterate over note names, which will be converted to note number later
    for note in list_notes:
        # Create a Note instance for this note, starting at 0s and ending at .5s
        note = pretty_midi.Note(velocity=100, pitch=note[1], start=note[0], end=note[0]+note[2])
        # Add it to our piano instrument
        piano.notes.append(note)
    # Add the piano instrument to the PrettyMIDI object
    midi_obj.instruments.append(piano)
    # Write out the MIDI data
    midi_obj.write(output_midi)