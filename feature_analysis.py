import matplotlib.pyplot as plt 
import numpy as np
import pickle

def plot_2_rubric(feature_list_0, feature_list_1, bins, feature_name):
    plt.figure()
    plt.hist(feature_list_0, bins, alpha=0.5, label='good', density=True)
    plt.hist(feature_list_1, bins, alpha=0.5, label='bad', density=True)
    plt.legend(loc='upper right')
    plt.title(feature_name)
    plt.show()

def plot_3_rubric(feature_list_0, feature_list_1, feature_list_2, bins, feature_name):
    plt.figure()
    plt.hist(feature_list_0, bins, alpha=0.5, label='good', density=True)
    plt.hist(feature_list_1, bins, alpha=0.5, label='minor error', density=True)
    plt.hist(feature_list_2, bins, alpha=0.5, label='serious error', density=True)
    plt.legend(loc='upper right')
    plt.title(feature_name)
    plt.show()


if __name__ == "__main__":
    with open("./data/list_annotation.pkl", "rb") as f:
        list_annotation_all = pickle.load(f)
    with open("./data/list_features_student.pkl", "rb") as f:
        list_features_student = pickle.load(f)

    overall = np.array([int(list_annotation_all[ii][0]) for ii in range(len(list_annotation_all))])
    onset = np.array([int(list_annotation_all[ii][1]) for ii in range(len(list_annotation_all))])
    dur = np.array([int(list_annotation_all[ii][2]) for ii in range(len(list_annotation_all))])
    extra = np.array([int(list_annotation_all[ii][3]) for ii in range(len(list_annotation_all))])
    start = np.array([int(list_annotation_all[ii][4]) for ii in range(len(list_annotation_all))])

    # overall features
    features_overall_0 = [list_features_student[ii] for ii in range(len(overall)) if overall[ii] == 0]
    features_overall_1 = [list_features_student[ii] for ii in range(len(overall)) if overall[ii] == 1]
    features_overall_2 = [list_features_student[ii] for ii in range(len(overall)) if overall[ii] == 2]

    pitch_diff_0 = [f[0] for f in features_overall_0 if f[0]]
    pitch_diff_1 = [f[0] for f in features_overall_1 if f[0]]
    pitch_diff_2 = [f[0] for f in features_overall_2 if f[0]]
    
    beat_div_0 = [f[1] for f in features_overall_0 if f[1]]
    beat_div_1 = [f[1] for f in features_overall_1 if f[1]]
    beat_div_2 = [f[1] for f in features_overall_2 if f[1]]

    ioi_diff_0 = [f[2] for f in features_overall_0 if f[2]]
    ioi_diff_1 = [f[2] for f in features_overall_1 if f[2]]
    ioi_diff_2 = [f[2] for f in features_overall_2 if f[2]]

    dur_diff_0 = [f[3] for f in features_overall_0 if f[3]]
    dur_diff_1 = [f[3] for f in features_overall_1 if f[3]]
    dur_diff_2 = [f[3] for f in features_overall_2 if f[3]]

    missing_0 = [f[4] for f in features_overall_0]
    missing_1 = [f[4] for f in features_overall_1]
    missing_2 = [f[4] for f in features_overall_2]

    extra_0 = [f[5] for f in features_overall_0]
    extra_1 = [f[5] for f in features_overall_1]
    extra_2 = [f[5] for f in features_overall_2]

    plot_3_rubric(pitch_diff_0, pitch_diff_1, pitch_diff_2, 50, "pitch_diff_overall")
    plot_3_rubric(beat_div_0, beat_div_1, beat_div_2, 50, "beat div overall")
    plot_3_rubric(ioi_diff_0, ioi_diff_1, ioi_diff_2, 50, "ioi diff overall")
    plot_3_rubric(dur_diff_0, dur_diff_1, dur_diff_2, 50, "dur diff overall")

    # onset features
    features_onset_0 = [list_features_student[ii] for ii in range(len(onset)) if onset[ii] == 0]
    features_onset_1 = [list_features_student[ii] for ii in range(len(onset)) if onset[ii] == 1]

    beat_div_0 = [f[1] for f in features_onset_0 if f[1]]
    beat_div_1 = [f[1] for f in features_onset_1 if f[1]]

    ioi_diff_0 = [f[2] for f in features_onset_0 if f[2]]
    ioi_diff_1 = [f[2] for f in features_onset_1 if f[2]]

    dur_diff_0 = [f[3] for f in features_onset_0 if f[3]]
    dur_diff_1 = [f[3] for f in features_onset_1 if f[3]]

    plot_2_rubric(beat_div_0, beat_div_1, 50, "beat div onset")
    plot_2_rubric(ioi_diff_0, ioi_diff_1, 50, "ioi diff onset")
    plot_2_rubric(dur_diff_0, dur_diff_1, 50, "dur diff onset")

    # duration features
    features_dur_0 = [list_features_student[ii] for ii in range(len(dur)) if dur[ii] == 0]
    features_dur_1 = [list_features_student[ii] for ii in range(len(dur)) if dur[ii] == 1]

    beat_div_0 = [f[1] for f in features_dur_0 if f[1]]
    beat_div_1 = [f[1] for f in features_dur_1 if f[1]]

    ioi_diff_0 = [f[2] for f in features_dur_0 if f[2]]
    ioi_diff_1 = [f[2] for f in features_dur_1 if f[2]]

    dur_diff_0 = [f[3] for f in features_dur_0 if f[3]]
    dur_diff_1 = [f[3] for f in features_dur_1 if f[3]]

    plot_2_rubric(beat_div_0, beat_div_1, 50, "beat div onset")
    plot_2_rubric(ioi_diff_0, ioi_diff_1, 50, "ioi diff onset")
    plot_2_rubric(dur_diff_0, dur_diff_1, 50, "dur diff onset")
