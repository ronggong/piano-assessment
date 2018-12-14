from path_data import path_annotation
from path_data import path_midi
import os
from parser.txt_parser import sv_score_annotation_parser
from midi2aud import save_midi_2_audio
from feature_cal import features_student

if __name__ == "__main__":
    temp_wav_t = "./temp/temp_wav_t.wav"
    temp_wav_s = "./temp/temp_wav_s.wav"
    plot_align = True

    folders = os.listdir(path_annotation)
    for folder in folders:
        if '.DS_Store' not in folder:
            path_student_annotation = os.path.join(path_annotation, folder)
            path_student_midi = os.path.join(path_midi, folder)
            filenames_annotation = os.listdir(path_student_annotation)
            for filename in filenames_annotation:
                if filename.endswith('.txt'):
                    filename_student_annotation = os.path.join(path_annotation, folder, filename)
                    filename_student_midi = os.path.join(path_midi, folder, filename.replace('.txt', '.mid'))
                    filename_teacher_midi = os.path.join(path_midi, folder, filename[:-8]+'(t).mid')

                    list_annotation = sv_score_annotation_parser(filename_student_annotation)

                    save_midi_2_audio(filename_teacher_midi, temp_wav_t)
                    save_midi_2_audio(filename_student_midi, temp_wav_s)

                    list_features_student = features_student(wav_t=temp_wav_t, 
                                                             wav_s=temp_wav_s, 
                                                             midi_t=filename_teacher_midi, 
                                                             annotation_txt_s=filename_student_annotation,
                                                             plot_align=plot_align)

                    print(len(list_features_student))
                    print(len(list_annotation))