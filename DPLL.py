from Rezolutie import creare_matrice_fisier, eliminare_clauze_triviale
from DP import regula_1_aplicabila, regula_2_aplicabila, propagarea_unitatii, literal_pur, exista_clauze
from collections import Counter
import copy, time, psutil, os

# ======================================================
# Alege literalul cu cele mai multe apariții absolute
# (ignorând semnul). Acest literal va fi folosit la split.
# @param clauze: lista de clauze (listă de liste de intregi)
# @return: literalul (fără semn) cu frecvența maximă
# ======================================================
def gasire_literal_splitare(clauze):

    frecventa_literali=Counter()

    for clauze in clauze:

        for literal in clauze:

            frecventa_literali[abs(literal)] += 1

    return frecventa_literali.most_common(1)[0][0]


# ======================================================
# Algoritm DPLL (Davis–Putnam–Logemann–Loveland)
# Aplică:
#  - propagare unitate (Regula 1)
#  - eliminare literal pur (Regula 2)
#  - split (alegere literal și recursivitate)
# @param clauze: formula sub formă de listă de clauze
# @return: True dacă formula este satisfiabilă, altfel False
# ======================================================
def este_SAT_DPLL(clauze):

    while exista_clauze(clauze):

        while regula_1_aplicabila(clauze):

            clauze=propagarea_unitatii(clauze)


        if not exista_clauze(clauze):
            return True

        if [] in clauze:
            return False


        while regula_2_aplicabila(clauze):

            literal_cautat=regula_2_aplicabila(clauze)
            clauze=literal_pur(clauze,literal_cautat)


        if not exista_clauze(clauze):
            return True


        literal_splitare=gasire_literal_splitare(clauze)

        clauze1=copy.deepcopy(clauze)
        clauze1.append([literal_splitare])

        clauze2=copy.deepcopy(clauze)
        clauze2.append([-literal_splitare])

        return este_SAT_DPLL(clauze1) or este_SAT_DPLL(clauze2)


    return True



# ======================================================
# Program principal
# 1. Citește clauzele din fișierul clauze.txt
# 2. Elimină clauzele triviale
# 3. Aplică algoritmul DPLL
# 4. Afișează rezultatul
# ======================================================

start = time.time()

mat=creare_matrice_fisier(r"C:\Users\JDari\OneDrive\Desktop\Clauze\test1.cnf")

mat=eliminare_clauze_triviale(mat)

if este_SAT_DPLL(mat):
    print("Clauzele sunt SATISFIABILE")

else:
    print("Clauzele sunt NESATISFIABILE")


process = psutil.Process(os.getpid())
memory_info = process.memory_info()
print(f"Memorie consumată: {memory_info.rss}B")
print(f"Memorie consumată: {memory_info.rss / 1024:.2f}KB")
print(f"Memorie consumată: {memory_info.rss / (1024**2):.2f}MB")
print(f"Memorie consumată: {memory_info.rss / (1024**3):.2f}GB")


end = time.time()
elapsed_time = (end - start)
print(f"Timp total de execuție: {elapsed_time:.3f}")
