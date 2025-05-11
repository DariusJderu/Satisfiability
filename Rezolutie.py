import time, os, psutil

# ======================================================
# Citeste dintr-un fisier numit "clauze.txt" fiecare linie
# si construieste o matrice (lista de liste), fiecare sublista
# reprezentand o clauza (o lista de intregi pe care am sortat-o).
# @return: lista de clauze (lista de liste de intregi)
# ======================================================
def creare_matrice_fisier(in_file):

    mat=[]

    with open(in_file,'r') as fin:
        for linie in fin:
            valori_string=linie.strip(" \n").split(" ")
            rand_nou=sorted([int(val) for val in valori_string])
            mat.append(rand_nou)

    return mat

# ======================================================
# Verifica daca o clauza contine atat un literal, cat si opusul sau.
# @param clauza: lista de literali (intregi)
# @return: True daca clauza contine literal si opusul sau, altfel False
# ======================================================
def contine_literali_opusi(clauza):

    literali=set(clauza)

    for literal in literali:

        if -literal in literali:
            return True

    return False

# ======================================================
# Elimina clauzele triviale din formula (care contin literal si opusul sau)
# deoarece ele sunt mereu adevarate si nu influenteaza satisfiabilitatea.
# @param clauze: lista de clauze
# @return: lista de clauze filtrata
# ======================================================
def eliminare_clauze_triviale(clauze):

    return [clauza for clauza in clauze if not contine_literali_opusi(clauza)]

# ======================================================
# Incearca sa rezolve doua clauze folosind regula rezolutiei
# Aduna literalii din ambele clauze, eliminand o pereche de literali opusi.
# Daca rezultatul contine o contradictie (literal si opusul sau), se returneaza False.
# Daca clauza are un cardinal mai mare decat cardinalele celor doua clauze initiale,
# nu merita aduagat si se returneaza False, altfel clauza noua (sortata).
# @param clauza1, clauza2: doua liste de literali
# @return: clauza noua (lista sortata) sau False
# ======================================================
def adunare_clauze(clauza1, clauza2):

    rezultat=[]
    literali_adunati=False
    literal_folosit_pt_adunare=None

    for literal in clauza1:

        if -literal in clauza2 and literali_adunati==False:
            literali_adunati=True
            literal_folosit_pt_adunare=-literal
            continue

        else:
            rezultat.append(literal)

    for literal in clauza2:

        if literal not in rezultat and literal!=literal_folosit_pt_adunare:
            rezultat.append(literal)


    for i in range(0,len(rezultat)-1,1):
        for j in range(i+1,len(rezultat),1):
            if rezultat[i]==-rezultat[j]:
                return False

    if len(rezultat)<=max(len(clauza1),len(clauza2)):
        return sorted(rezultat)

    return False

# ======================================================
# Verifica daca o formula (lista de clauze) este satisfiabila
# folosind metoda rezolutiei. Se adauga clauze noi prin rezolutie
# pana cand se obtine clauza vida ([]), caz in care formula este NESAT.
# Daca nu se mai pot genera clauze noi, formula este SAT.
# @param clauze: lista de clauze
# @return: True daca formula e SAT, False daca e UNSAT
# ======================================================
def este_SAT_Rezolutie(clauze):

    while True:

        lista_noua_clauze_formate=[]

        for i in range(len(clauze)-1):
            for j in range(i+1,len(clauze)):
                new_clauza = adunare_clauze(clauze[i], clauze[j])

                if new_clauza==[]:
                    return False

                elif new_clauza!=False:
                    if new_clauza not in clauze and new_clauza not in lista_noua_clauze_formate:
                        lista_noua_clauze_formate.append(new_clauza)

        if lista_noua_clauze_formate!=[]:
            clauze.extend(lista_noua_clauze_formate)

        else:
            return True



# ======================================================
# Program principal (main)
# Citeste clauze din fisier, elimina cele triviale, aplica rezolutia
# si afiseaza daca formula este SAT sau UNSAT.
# ======================================================

# start = time.time()
#
# mat=creare_matrice_fisier(r"C:\Users\JDari\OneDrive\Desktop\Clauze\test1.cnf")
#
# mat=eliminare_clauze_triviale(mat)
#
# if este_SAT_Rezolutie(mat):
#     print("Clauzele sunt SATISFIABILE")
#
#
# else:
#     print("Clauzele sunt NESATISFIABILE")
#
#
# process = psutil.Process(os.getpid())
# memory_info = process.memory_info()
# print(f"Memorie consumată: {memory_info.rss}B")
# print(f"Memorie consumată: {memory_info.rss / 1024:.2f}KB")
# print(f"Memorie consumată: {memory_info.rss / (1024**2):.2f}MB")
# print(f"Memorie consumată: {memory_info.rss / (1024**3):.2f}GB")
#
#
# end = time.time()
# elapsed_time = (end - start)
# print(f"Timp total de execuție: {elapsed_time:.3f}")