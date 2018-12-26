import numpy as np
import pickle
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import precision_score, recall_score, f1_score


def CV_run(skf, list_features, annotation_no_extra, feature_str=None):
    skf.get_n_splits(list_features, annotation_no_extra)

    for ii, (train_index, test_index) in enumerate(skf.split(list_features, annotation_no_extra)):
        X_train, X_test = list_features[train_index], list_features[test_index]
        y_train, y_test = annotation_no_extra[train_index], annotation_no_extra[test_index]

        scaler = StandardScaler()
        X_train = scaler.fit_transform(X_train)
        X_test = scaler.transform(X_test)
        clf = LogisticRegression(random_state=0, solver='lbfgs',
                                 multi_class='multinomial', class_weight='balanced').fit(X_train, y_train)
        y_pred = clf.predict(X_test)

        p = precision_score(y_test, y_pred, average='weighted')
        r = recall_score(y_test, y_pred, average='weighted')
        f1 = f1_score(y_test, y_pred, average='weighted')

        print(feature_str+" CV {} precision {}, recall {}, f1 {}".format(ii, p, r, f1))

if __name__ == "__main__":
    with open("./data/list_annotation_manual_aligned.pkl", "rb") as f:
        list_annotation_all = pickle.load(f)
    with open("./data/list_features_student_manual_aligned.pkl", "rb") as f:
        list_features_student = pickle.load(f)

    overall = np.array([int(list_annotation_all[ii][0]) for ii in range(len(list_annotation_all))])
    onset = np.array([int(list_annotation_all[ii][1]) for ii in range(len(list_annotation_all))])
    dur = np.array([int(list_annotation_all[ii][2]) for ii in range(len(list_annotation_all))])
    extra = np.array([int(list_annotation_all[ii][3]) for ii in range(len(list_annotation_all))])
    start = np.array([int(list_annotation_all[ii][4]) for ii in range(len(list_annotation_all))])

    # remove extra features and annotations, since extra note must be a bad note
    list_features_student_no_extra = [list_features_student[ii] for ii in range(len(list_features_student)) if extra[ii] == 0]
    overall_no_extra = overall[extra != 1]
    onset_no_extra = onset[extra != 1]
    dur_no_extra = dur[extra != 1]

    # features for overall, onset, dur
    list_features_student_overall = np.array([[f[0], f[1], f[2], f[3]] for f in list_features_student_no_extra])
    list_features_student_onset_dur = np.array([[f[1], f[2], f[3]] for f in list_features_student_no_extra])

    skf = StratifiedKFold(n_splits=3, shuffle=True)

    # overall
    CV_run(skf, list_features_student_overall, overall_no_extra, 'overall')

    # onset
    CV_run(skf, list_features_student_onset_dur, onset_no_extra, 'onset')

    # dur
    CV_run(skf, list_features_student_onset_dur, dur_no_extra, 'duration')