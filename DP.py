from Rezolutie import creare_matrice_fisier, eliminare_clauze_triviale, adunare_clauze
import copy, time, psutil, os

# ======================================================
# Verifică dacă în formulă există o clauză unitară (cu un singur literal).
# Dacă da, se poate aplica propagarea unității.
# @param clauze: lista de clauze (listă de liste de intregi)
# @return: True dacă există clauză unitară, altfel False
# ======================================================
def regula_1_aplicabila(clauze):

    for clauza in clauze:

        if len(clauza) == 1:
            return True

    return False


# ======================================================
# Caută un literal care este "pur" – adică apare doar cu un singur semn
# (doar pozitiv sau doar negativ). Un astfel de literal poate fi setat
# ca adevărat, iar clauzele care îl conțin pot fi eliminate.
# @param clauze: lista de clauze
# @return: literalul pur (int) dacă există, altfel False
# ======================================================
def regula_2_aplicabila(clauze):

    aparitii = {}

    for clauza in clauze:

        for literal in clauza:

            if literal not in aparitii:
                aparitii[literal] = True

    for literal in aparitii:
        if -literal not in aparitii:
            return literal

    return False


# ======================================================
# Verifică dacă mai există clauze.
# @param clauze: lista de clauze
# @return: False dacă lista e goală, altfel True
# ======================================================
def exista_clauze(clauze):

    if clauze == []:
        return False

    return True


# ======================================================
# Aplică propagarea unității: găsește un literal dintr-o clauză unitară,
# îl presupune adevărat, și:
# - elimină clauzele în care apare
# - elimină negația lui din celelalte clauze
# @param clauze: lista de clauze
# @return: lista de clauze actualizată
# ======================================================
def propagarea_unitatii(clauze):

    literal_cautat=None

    for clauza in clauze:

        if len(clauza) == 1:
            literal_cautat = clauza[0]
            break

    new_clauze = []

    for clauza in clauze:

        if literal_cautat in clauza:
            continue

        else:
            clauza_noua=[literal for literal in clauza if literal!=-literal_cautat]
            new_clauze.append(clauza_noua)


    return new_clauze


# ======================================================
# Elimină toate clauzele care conțin literalul dat (presupus adevărat).
# Se folosește la aplicarea regulii literalului pur.
# @param clauze: lista de clauze
# @param literal_cautat: literalul pur care va fi eliminat
# @return: lista de clauze actualizată
# ======================================================
def literal_pur(clauze, literal_cautat):

    new_clauze = []

    for clauza in clauze:

        if literal_cautat in clauza:
            continue

        else:
            new_clauze.append(clauza)


    return new_clauze


# ======================================================
# Aplică rezoluția pe toate perechile de clauze posibile.
# Dacă se generează clauza vidă => formula este nesatisfiabilă (False).
# Dacă nu se pot genera clauze noi, întoarce True.
# Altfel, adaugă clauzele noi la formulă și continuă.
# @param clauze: lista de clauze
# @return: clauzele extinse, sau True (SAT), sau False (UNSAT)
# ======================================================
def aplicare_rezolutie(clauze):

    lista_noua_clauze_formate = []

    for i in range(len(clauze) - 1):
        for j in range(i + 1, len(clauze)):

            new_clauza = adunare_clauze(clauze[i], clauze[j])

            if new_clauza == []:
                return False

            elif new_clauza != False:
                if new_clauza not in clauze and new_clauza not in lista_noua_clauze_formate:
                    lista_noua_clauze_formate.append(new_clauza)


    if lista_noua_clauze_formate != []:
        clauze.extend(lista_noua_clauze_formate)
        return clauze

    else:
        return True


# ======================================================
# Algoritm principal David–Putnam (DP) pentru satisfiabilitate.
# Aplică:
# - propagarea unității (Regula 1)
# - eliminarea literalilor puri (Regula 2)
# - rezoluție între clauze (Regula 3)
# @param clauze: lista de clauze
# @return: True dacă formula este satisfiabilă, altfel False
# ======================================================
def este_SAT_DP(clauze):

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


        clauze=aplicare_rezolutie(clauze)

        if clauze == True:
            return True

        elif clauze == False:
            return False


    return True



# ======================================================
# Program principal (main)
# Citește clauze din fișier, elimină cele triviale,
# aplică metoda David–Putnam și afișează rezultatul.
# ======================================================

start = time.time()

mat=creare_matrice_fisier(r"C:\Users\JDari\OneDrive\Desktop\Clauze\test1.cnf")

mat=eliminare_clauze_triviale(mat)

if este_SAT_DP(mat):
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
