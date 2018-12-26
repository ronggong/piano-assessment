from path_data import path_annotation_aligned
from path_data import path_midi
import os
from parser.txt_parser import sv_score_annotation_parser_manual_aligned
from midi2aud import save_midi_2_audio
from feature_cal import features_student_manual_alignment
import numpy as np
import pickle

if __name__ == "__main__":

    list_features_student_all = []
    list_annotation_all = []

    folders = os.listdir(path_annotation_aligned)
    for folder in folders:
        if '.DS_Store' not in folder:
            # annotation path 标注数据-1129
            path_student_annotation = os.path.join(path_annotation_aligned, folder)
            # midi path with audio
            path_student_midi = os.path.join(path_midi, folder)
            # list annotation file names
            filenames_annotation = os.listdir(path_student_annotation)

            for filename in filenames_annotation:
                if filename.endswith('.txt'): # annotation file name ends with .txt
                    # student annotation
                    filename_student_annotation = os.path.join(path_annotation_aligned, folder, filename)
                    
                    # parse annotation and manual alignment, write an annotation parser
                    list_annotation, list_score_aligned = sv_score_annotation_parser_manual_aligned(filename_student_annotation)
                    
                    # extract student performance features
                    list_features_student = features_student_manual_alignment(list_score_aligned)

                    list_features_student_all += list_features_student
                    list_annotation_all += list_annotation

    with open("./data/list_features_student_manual_aligned.pkl", "wb") as f:
        pickle.dump(list_features_student_all, f)

    with open("./data/list_annotation_manual_aligned.pkl", "wb") as f:
        pickle.dump(list_annotation_all, f)


        