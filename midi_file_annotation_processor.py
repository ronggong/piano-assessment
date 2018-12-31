import os
from collections import defaultdict

base_dir = "./data"
midi_txt_dir = os.path.join(base_dir, "测试数据转谱")
ground_truth_dir = os.path.join(base_dir, "标注数据-1129")
processed_dir = os.path.join(base_dir, "processed")

if not os.path.exists(processed_dir):
    os.mkdir(processed_dir)

def get_graph(lines):
    """
    get the graph created based on the txt file
    the key is the pitches, the value is a list for each pitch
    format of the entry in the list: (line number, onset, annotation if exists)
    """
    graph = defaultdict(list)
    for i, line in enumerate(lines):
        line = line.split('\t')
        # get the annotation if exists
        annotation = line[-1].split()[-1]
        if len(annotation) == 5 and set(annotation).issubset({'0', '1', '2'}):
            data = (i, float(line[0]), annotation)
        else:
            data = (i, float(line[0]))
        graph[int(line[1])].append(data)
    return graph

def add_annotation(line, annotation):
    """
    add the annotation for a line from the ground truth to the midi created file
    """
    line = line.strip()
    line += '\t{}\n'.format(annotation)
    return line

def process(dname, fname):
    """
    given the directory name and file name
    process the file
    """
    # ground truth file directory
    dir1 = os.path.join(ground_truth_dir, dname)
    # midi based file directory
    dir2 = os.path.join(midi_txt_dir, dname)
    # processed file directory
    dir3 = os.path.join(processed_dir, dname)
    
    # create the processed file directory if not exist
    if not os.path.exists(dir3):
        os.mkdir(dir3)

    # ground truth file
    fn1 = os.path.join(dir1, fname + '.txt')
    # midi based file
    fn2 = os.path.join(dir2, fname + '.mp3.midi.txt')
    # processed file
    fn3 = os.path.join(dir3, fname + '.mp3.midi.txt')

    l1, l2 = [], []
    with open(fn1) as f1:
        l1 = f1.readlines()
    with open(fn2) as f2:
        l2 = f2.readlines()

    g1 = get_graph(l1)
    g2 = get_graph(l2)
    threshold = 0.1

    for k in g1:
        len1 = len(g1[k])
        len2 = len(g2[k])
        # add the label to the corresponding line directly if the lengths match
        if len1 == len2:
            for i in range(len1):
                if len(g1[k][i]) == 3:
                    idx = g2[k][i][0]
                    l2[idx] = add_annotation(l2[idx], g1[k][i][2])
            continue
        # if lengths don't match, match the lines based on the onset
        i1, i2 = 0, 0
        while (i1 < len1 and i2 < len2):
            if abs(g2[k][i2][1] - g1[k][i1][1]) > threshold:
                if len1 > len2:
                    i1 += 1
                else:
                    i2 += 1
            if len(g1[k][i1]) == 3:
                idx = g2[k][i2][0]
                l2[idx] = add_annotation(l2[idx], g1[k][i1][2])
            i1 += 1
            i2 += 1

    # store the processed file
    with open(fn3, 'w') as f:
        for l in l2:
            f.write(l)

# process each file
for dir_name in os.listdir(ground_truth_dir):
    if dir_name == '.DS_Store':
        continue
    for file_name in os.listdir(os.path.join(ground_truth_dir, dir_name)):
        if file_name.endswith('(s).txt'):
            process(dir_name, file_name[:-4])