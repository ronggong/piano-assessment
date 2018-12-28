from path_data import path_transcribed
from path_data import path_midi
import os
from parser.txt_parser import sv_score_annotation_parser
from parser.txt_parser import sv_score_parser
from synthesizer.midi_synthesizer import notes2midi
from midi2aud import save_midi_2_audio
from feature_cal import features_student
import numpy as np
import pickle

if __name__ == "__main__":
    temp_wav_t = "./temp/temp_wav_t.wav"
    temp_wav_s = "./temp/temp_wav_s.wav"
    temp_midi_s = "./temp/temp_midi_s.wav"
    plot_align = False

    list_features_student_all = {}
    list_annotation_all = []

    folders = os.listdir(path_transcribed)
    for folder in folders:
        # if folder != '采集数据：快乐钢琴，王恩言，学琴五个月':
        #     continue
        if '.DS_Store' not in folder:
            # transcribed path
            path_student_transcribed = os.path.join(path_transcribed, folder)
            # midi path with audio
            path_student_midi = os.path.join(path_midi, folder)
            # list annotation file names
            filenames_transcribed = os.listdir(path_student_transcribed)

            for filename in filenames_transcribed:
                # if filename != 'row1(s).mp3.midi.txt':
                #     continue
                if filename.endswith('.mp3.midi.txt'):
                    base_filename = filename.replace('.mp3.midi.txt', '')
                    # student transcription
                    filename_student_transcribed = os.path.join(path_transcribed, folder, filename)
                    list_score_student_transcribed = sv_score_parser(filename_student_transcribed)

                    notes2midi(list_score_student_transcribed, temp_midi_s)

                    # teacher midi file name
                    filename_teacher_midi = os.path.join(path_midi, folder, base_filename[:-4]+'(t).mid')

                    # # parse annotation
                    # list_annotation = sv_score_annotation_parser(filename_student_transcribed)

                    # convert midi to wav for the alignment
                    save_midi_2_audio(filename_teacher_midi, temp_wav_t)
                    save_midi_2_audio(temp_midi_s, temp_wav_s)

                    print(folder, filename)

                    # extract student performance features
                    list_features_student = features_student(wav_t=temp_wav_t, 
                                                             wav_s=temp_wav_s, 
                                                             midi_t=filename_teacher_midi, 
                                                             annotation_txt_s=filename_student_transcribed,
                                                             plot_align=plot_align)

                    list_features_student_all[folder+'-'+base_filename] = list_features_student
                    # list_annotation_all += list_annotation

                    # print(len(list_features_student), len(list_annotation))

    with open("./data/list_features_student_transcribed.pkl", "wb") as f:
        pickle.dump(list_features_student_all, f)

    # with open("./data/list_annotation.pkl", "wb") as f:
    #     pickle.dump(list_annotation_all, f)


        