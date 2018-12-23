from path_data import path_annotation
from path_data import path_midi
import os
from parser.txt_parser import sv_score_annotation_parser
from midi2aud import save_midi_2_audio
from feature_cal import features_student
import numpy as np
import pickle

if __name__ == "__main__":
    temp_wav_t = "./temp/temp_wav_t.wav"
    temp_wav_s = "./temp/temp_wav_s.wav"
    plot_align = True

    list_features_student_all = []
    list_annotation_all = []

    folders = os.listdir(path_annotation)
    for folder in folders:
        if '.DS_Store' not in folder:
            # annotation path 标注数据-1129
            path_student_annotation = os.path.join(path_annotation, folder)
            # midi path with audio
            path_student_midi = os.path.join(path_midi, folder)
            # list annotation file names
            filenames_annotation = os.listdir(path_student_annotation)

            for filename in filenames_annotation:
                if filename.endswith('.txt'): # annotation file name ends with .txt
                    # student annotation
                    filename_student_annotation = os.path.join(path_annotation, folder, filename)
                    # student midi file name
                    filename_student_midi = os.path.join(path_midi, folder, filename.replace('.txt', '.mid'))
                    # teacher midi file name
                    filename_teacher_midi = os.path.join(path_midi, folder, filename[:-8]+'(t).mid')

                    # parse annotation
                    list_annotation = sv_score_annotation_parser(filename_student_annotation)

                    # convert midi to wav for the alignment
                    save_midi_2_audio(filename_teacher_midi, temp_wav_t)
                    save_midi_2_audio(filename_student_midi, temp_wav_s)

                    # extract student performance features
                    list_features_student = features_student(wav_t=temp_wav_t, 
                                                             wav_s=temp_wav_s, 
                                                             midi_t=filename_teacher_midi, 
                                                             annotation_txt_s=filename_student_annotation,
                                                             plot_align=plot_align)

                    list_features_student_all += list_features_student
                    list_annotation_all += list_annotation

                    # print(len(list_features_student), len(list_annotation))

    with open("./data/list_features_student.pkl", "wb") as f:
        pickle.dump(list_features_student_all, f)

    with open("./data/list_annotation.pkl", "wb") as f:
        pickle.dump(list_annotation_all, f)


        