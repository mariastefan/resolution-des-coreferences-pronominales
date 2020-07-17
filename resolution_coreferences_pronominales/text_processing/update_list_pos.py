def update():
    pos_list = []
    with open('pos_sequences', 'r') as seq_file:
        for line in seq_file.readlines():
            for pos in line.split():
                if pos not in pos_list:
                    pos_list.append(pos)
    print(pos_list)
    with open('list_pos', 'w') as f:
        f.write('\n'.join(pos_list))
