import ast  # Pour parser un str en une list : ast.literal_eval()
import sys
import os

sys.path.append(".")
from resolution_coreferences_pronominales.coreferences import analyses_texte
import time

if __name__ == '__main__':
    start = time.time()
    phrases_test = open(os.path.dirname(os.path.dirname(__file__)) + "/data/phrases_test", "r")
    numero_ligne = 0
    incorrect = 0
    correct = 0
    phrase = ""
    for ligne in phrases_test:
        if numero_ligne % 2 == 0:
            phrase = ligne
        else:
            corefs_justes = ast.literal_eval(ligne)
            corefs_a_tester = analyses_texte.coreferences_phrase(phrase, True)
            if corefs_justes == corefs_a_tester:
                print(phrase.rstrip() + " : 100%")  # pour enlever le \n
                correct += len(corefs_justes)
            else:
                print(phrase.rstrip() + " : PAS TOTALEMENT JUSTE")
                if len(corefs_a_tester) == len(corefs_justes):
                    for ind in range(len(corefs_justes)):
                        if corefs_justes[ind][1].lower() != corefs_a_tester[ind][1].lower():
                            print("La coréférence trouvée pour le pronom numéro " + str(ind + 1) + " est " +
                                  str(corefs_a_tester[ind]) + " alors qu'elle devrait etre " + str(corefs_justes[ind]) + '\n')
                            incorrect += 1
                        else:
                            correct += 1
                elif len(corefs_a_tester) != 0 and len(corefs_justes) != 0 and len(corefs_a_tester) != len(corefs_justes):
                    print("Toutes les coréférences n'ont pas été trouvées, seulement :", corefs_a_tester)
                elif len(corefs_a_tester) == 0:
                    print('Aucune coréférence trouvée' + '\n')
                    incorrect == len(corefs_justes)
                else:  # len(corefs_a_tester) < len(corefs_justes)
                    for ind_j in range(len(corefs_justes)):
                        for ind_t in range(len(corefs_a_tester)):
                            if corefs_justes[ind_j][0].lower() == corefs_a_tester[ind_t][0].lower():
                                if corefs_justes[ind_j][1].lower() != corefs_a_tester[ind_t][1].lower():
                                    print("La coréférence trouvée pour le pronom numéro " + str(ind + 1) + " est " +
                                          str(corefs_a_tester[ind]) + " alors qu'elle devrait etre " + str(
                                        corefs_justes[ind]) + '\n')
                                    incorrect += 1
                                    break
                                else:
                                    correct += 1
                                    break
                            else:
                                print()
                                incorrect += 1

        numero_ligne += 1
    phrases_test.close()
    precision = (correct - incorrect) / correct
    print("\n" + str(precision * 100) + '% des coréférences sont justes.')
    historique_precision = open("historique_precision.txt", "r+")
    last_line = historique_precision.readlines()
    if last_line:
        last_line = last_line[-1]
        if precision < float(last_line):
            # historique_precision.write("\n" + str(precision))
            print('\033[93m' + "ATTENTION ! La précision a baissé. Avant elle était de " + str(float(last_line) * 100) +
                  "%, maintenant elle est de " + str(precision * 100) +
                  "% ! \nPas d'inscription de la nouvelle "
                  "valeur dans historique_precision.txt, vérifiez "
                  "d'abord pourquoi la précision a baissé et "
                  "ajoutez manuellement la précision au fichier "
                  "si utile.")

        elif precision > float(last_line):
            print("Bravo ! La précision a augmenté ! Avant elle était de " + str(float(last_line) * 100) +
                  "%, maintenant elle est de " + str(precision) + "% !")
            historique_precision.write("\n" + str(precision))
        else:
            print("La précision n'a pas changé.")
    else:
        historique_precision.write("\n" + str(precision))
    historique_precision.close()
    print(time.time() - start)