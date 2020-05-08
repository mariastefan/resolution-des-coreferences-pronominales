import extraction_mot

if __name__ == '__main__':
    for e in extraction_mot.relations_entre_mots(["eau", "rivière", "profond"], True):
        print(e)
