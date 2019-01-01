import numpy as np
import pickle
from sklearn.model_selection import KFold
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import precision_recall_fscore_support

def get_feature_annotation_with(list_features_student, list_annotation_all, keys):
    overall = np.array([int(anno[0]) for ii in keys for anno in list_annotation_all[ii]])
    onset = np.array([int(anno[1]) for ii in keys for anno in list_annotation_all[ii]])
    dur = np.array([int(anno[2]) for ii in keys for anno in list_annotation_all[ii]])
    extra = np.array([int(anno[3]) for ii in keys for anno in list_annotation_all[ii]])
    # start = np.array([int(list_annotation_all[ii][4]) for ii in keys])
    
    # remove extra features and annotations, since extra note must be a bad note
    list_features_student_no_extra = []
    ii = 0
    for k in keys:
        for feature in list_features_student[k]:
            # print(extra[ii])
            if extra[ii] == 0:
                list_features_student_no_extra.append(feature)
            ii += 1
    overall_no_extra = overall[extra != 1]
    onset_no_extra = onset[extra != 1]
    dur_no_extra = dur[extra != 1]

    list_features_student_overall = np.array([[f[0], f[1], f[2], f[3]] for f in list_features_student_no_extra])
    list_features_student_onset_dur = np.array([[f[1], f[2], f[3]] for f in list_features_student_no_extra])

    return list_features_student_overall, list_features_student_onset_dur, overall_no_extra, onset_no_extra, dur_no_extra

def output_metrics(X_train, y_train, X_test, y_test, feature_str, fold):
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)
    clf = LogisticRegression(random_state=0, solver='lbfgs',
                            multi_class='multinomial', class_weight='balanced').fit(X_train, y_train)
    y_pred = clf.predict(X_test)

    p, r, _, support = precision_recall_fscore_support(y_test, y_pred, average=None)
    # r = recall_score(y_test, y_pred, average=None)
    # f1 = f1_score(y_test, y_pred, average=None)

    print(feature_str+" CV fold {} precision {}, recall {}, support {}".format(fold, p, r, support))

def CV_run(skf, keys_all, features_manual, annotation_manual, features_transcribed, annotation_transcribed, feature_str=None):

    for ii, (train_index, test_index) in enumerate(skf.split(keys_all)):
        keys_train, keys_test = keys_all[train_index], keys_all[test_index]
        features_train_overall, features_train_onset_dur, overall_train, onset_train, dur_train = get_feature_annotation_with(features_manual, annotation_manual, keys_train)
        features_test_overall, features_test_onset_dur, overall_test, onset_test, dur_test = get_feature_annotation_with(features_transcribed, annotation_transcribed, keys_test)
        
        output_metrics(features_train_overall, overall_train, features_test_overall, overall_test, 'overall', ii)
        output_metrics(features_train_onset_dur, onset_train, features_test_onset_dur, onset_test, 'onset', ii)
        output_metrics(features_train_onset_dur, dur_train, features_test_onset_dur, dur_test, 'dur', ii)


if __name__ == "__main__":
    with open("./data/list_annotation_manual_aligned_dict.pkl", "rb") as f:
        list_annotation_all_manual = pickle.load(f)
    with open("./data/list_features_student_manual_aligned_dict.pkl", "rb") as f:
        list_features_student_manual = pickle.load(f)

    with open("./data/list_annotation_transcribed.pkl", "rb") as f:
        list_annotation_all_transcribed = pickle.load(f)
    with open("./data/list_features_student_transcribed.pkl", "rb") as f:
        list_features_student_transcribed = pickle.load(f)

    keys_all = np.array([key for key in list_annotation_all_manual])
    
    skf = KFold(n_splits=3, shuffle=True)

    skf.get_n_splits(keys_all)

    # dur
    CV_run(skf, 
           keys_all, 
           list_features_student_manual,
           list_annotation_all_manual, 
           list_features_student_transcribed,
           list_annotation_all_transcribed)