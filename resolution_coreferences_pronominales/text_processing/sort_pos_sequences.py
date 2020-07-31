import pickle
import sys
pos_sequences_out_path = 'data/pos_sequences_sorted.pkl'
pos_sequences_path = 'data/pos_sequences'
pos_sequences = []
with open(pos_sequences_path, 'r', encoding='iso-8859-1') as seq_file:
    for line in seq_file.readlines():
        if line and line != '\n':
            pos_sequence = []
            line2 = line.split('\n')[0]
            for pos in line2.split():
                pos_sequence.append(pos)
            if pos_sequence not in pos_sequences:
                pos_sequences.append(pos_sequence)

pos_sequences = sorted(pos_sequences, key=len, reverse=True)
res = {}
for i in pos_sequences:
    # print(i)
    if len(i) in res.keys():
        res[len(i)].append(' '.join(i))
    else:
        res[len(i)] = [' '.join(i)]
for key, value in res.items():
    res[key] = sorted(value, key=len, reverse=True)

try:
    seq_file = open(pos_sequences_path, 'w')
except Exception as e:
    sys.exit('Impossible de créer le fichier ' + pos_sequences_path + '\nMotif : %s' % e)

all_pos_sequences = []
for value in res.values():
    for item in value:
        seq_file.write(item + '\n')
        for a in item.split(','):
            one_pos_sequence = []
            for b in a.split():
                one_pos_sequence.append(b)
            all_pos_sequences.append(one_pos_sequence)

try:
    seq_file.close()
except Exception as e:
    print('Impossible de fermer le fichier ' + seq_file + '\nMotif : %s' % e + ' Le programme continue.')
    pass

    file = open(pos_sequences_out_path, 'wb')
except Exception as e:
    sys.exit('Impossible de créer le fichier ' + pos_sequences_out_path + '\nMotif : %s' % e)

pickle.dump(all_pos_sequences, file)
try:
    file.close()
except Exception as e:
    print('Impossible de fermer le fichier ' + file + '\nMotif : %s' % e + ' Le programme continue.')
    pass

