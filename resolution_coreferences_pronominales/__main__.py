import resolution_coreferences_pronominales_extraction_mot

if __name__ == '__main__':
    relations_mot = resolution_coreferences_pronominales_extraction_mot.relations_mot('amfour', 'all', 0)
    if(relations_mot is None):
        print("oui")
    else:
        for rid in relations_mot.keys():
            print(rid + " : " + str(relations_mot[rid]))
