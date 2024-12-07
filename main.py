
from copy import copy
from collections import deque

'''
6 azioni possibili:
1)c3 in c8 
2)c5 in c8
3)c8 in c5
4)c3 in c5
5)c8 in c3
6)c5 in c3
'''
def compiAzione(stato_ingresso, scelta):
    stato=copy(stato_ingresso)
    if scelta=="0":
        trasferisci(stato, 3, 8)
    elif scelta == "1":
        trasferisci(stato, 5, 8)
    elif scelta == "2":
        trasferisci(stato, 8, 5)
    elif scelta == "3":
        trasferisci(stato, 3, 5)
    elif scelta == "4":
        trasferisci(stato, 8, 3)
    elif scelta =="5":
        trasferisci(stato, 5, 3)
    else:
        pass
    return stato

def trasferisci(stato, da_contenitore, a_contenitore):
    trasferibile = min(stato[da_contenitore], a_contenitore - stato[a_contenitore])
    stato[da_contenitore] -= trasferibile
    stato[a_contenitore] += trasferibile

def obiettivoRaggiunto(stato):
    if(stato[8]==4 or stato[5]==4):
        return True
    return False


def game():
    stato= {8:8, 5:0, 3:0}
    print("Obiettivo: dividere esattamente 4 litri di acqua in uno dei contenitori")
    print(stato)
    while(not obiettivoRaggiunto(stato)):
        print("Scegli azione: ")
        print("0)Da c3 a c8")
        print("1)Da c5 a c8")
        print("2)Da c8 a c5")
        print("3)Da c3 a c5")
        print("4)Da c8 a c3")
        print("5)Da c5 a c3")
        scelta = input()
        stato=compiAzione(stato, scelta)
        print(stato)
    print("OBIETTIVO RAGGIUNTO...COMPLIMENTI!")


def ricercaInProfondita(stato, stati_visitati,profondita):
    stati_visitati.add(tuple(sorted(stato.items())))
    profondita+=1
    if(obiettivoRaggiunto(stato)):
        return True
    for mossa in range(6):
        nuovo_stato=compiAzione(stato, str(mossa))
        if(tuple(sorted(nuovo_stato.items())) not in stati_visitati):
            print("PROFONDITA': "+ str(profondita)+" MOSSA: " + str(mossa))
            print(nuovo_stato)
            if(ricercaInProfondita(nuovo_stato, stati_visitati,profondita)):
                return True
    return False

def eseguiRicercaInProfondita():
    stati_visitati=set()
    stato= {8:8, 5:0, 3:0}
    print("Obiettivo: dividere esattamente 4 litri di acqua in uno dei contenitori")
    print(stato)
    if(ricercaInProfondita(stato, stati_visitati, 0)):
      print("OBIETTIVO RAGGIUNTO")
    else:
      print("FALLIMENTO")


def ricercaAProfonditaLimitata(stato, stati_visitati,sequenza_stati_risolutiva,profondita, limite_di_profondita):
    stati_visitati.add(tuple(sorted(stato.items())))
    profondita+=1
    if(obiettivoRaggiunto(stato)):
        return True
    for mossa in range(6):
        nuovo_stato=compiAzione(stato, str(mossa))
        if(tuple(sorted(nuovo_stato.items())) not in stati_visitati and profondita<=limite_di_profondita):
            print(f"PROFONDITÀ: {profondita} | MOSSA: {mossa} | STATO: {nuovo_stato}")
            sequenza_stati_risolutiva.append((mossa, tuple(sorted(nuovo_stato.items()))))
            if(ricercaAProfonditaLimitata(nuovo_stato,stati_visitati,sequenza_stati_risolutiva,profondita, limite_di_profondita)):
                return True
            sequenza_stati_risolutiva.pop()
    return False



def eseguiRicercaAdApprofondimentoIterativo():
    for limite_profondita in range(1,20):
        stati_visitati = set()
        sequenza_stati_risolutiva = deque()
        stato = {8: 8, 5: 0, 3: 0}
        print("Obiettivo: dividere esattamente 4 litri di acqua in uno dei contenitori")
        print(stato)
        print("LIMITE PROFONDITA' "+str(limite_profondita))
        if(ricercaAProfonditaLimitata(stato, stati_visitati,sequenza_stati_risolutiva, 0, limite_profondita)):
            print("OBIETTIVO RAGGIUNTO")
            print("Sequenza completa di mosse:")
            for i, (mossa, stato) in enumerate(sequenza_stati_risolutiva, 1):
                print(f"Passo {i}: Mossa {mossa}, Stato {dict(stato)}")
            break
        else:
            print(f"RICERCA A PROFONDITÀ {limite_profondita} FALLITA")

def ricercaInAmpiezza(stato_iniziale, sequenza_stati_risolutiva):
    stati_visitati=set()
    coda_stati=deque()
    stati_visitati.add(tuple(sorted(stato_iniziale.items())))
    coda_stati.append((tuple(sorted(stato_iniziale.items())),[]))
    while coda_stati:
      stato, percorso = coda_stati.popleft()
      if(obiettivoRaggiunto(dict(stato))):
        sequenza_stati_risolutiva.extend(percorso)
        return True
      for mossa in range(6):
        nuovo_stato = compiAzione(dict(stato), str(mossa))
        if(tuple(nuovo_stato) not in stati_visitati):
            stati_visitati.add(tuple(sorted(nuovo_stato.items())))
            coda_stati.append((tuple(sorted(nuovo_stato.items())),  percorso + [(mossa, (tuple(sorted(nuovo_stato.items()))))]))
    return False

def eseguiRicercaInAmpiezza():
    sequenza_stati_risolutiva = deque()
    stato = {8:8, 5:0, 3:0}
    print("Obiettivo: dividere esattamente 4 litri di acqua in uno dei contenitori")
    print(stato)
    if (ricercaInAmpiezza(stato, sequenza_stati_risolutiva)):
        print("OBIETTIVO RAGGIUNTO")
        for passo, (mossa, stato) in enumerate(sequenza_stati_risolutiva, 1):
            print(f"Passo {passo}: Mossa {mossa}, Stato {dict(stato)}")
    else:
        print("FALLIMENTO")

esposizione_del_problema="""
Ecco una versione del problema della damigiana:

Hai tre contenitori con le seguenti capacità:
1)Una damigiana da 8 litri (c8)  (completamente piena).
2)Un contenitore da 5 litri (c5) (vuoto).
3)Un contenitore da 3 litri (c3) (vuoto).

Obiettivo:
Dividere esattamente 4 litri di acqua in uno dei contenitori.

Puoi trasferire acqua da un contenitore all’altro, ma senza utilizzare strumenti di misurazione diversi dai contenitori stessi.
"""
print(esposizione_del_problema)
print("Scegli tra:")
print("0)Prova a risolverlo tu")
print("1)Esegui ricerca in profondità")
print("2)Esegui ricerca ad approfondimento iterativo")
print("3)Esegui ricerca in ampiezza")
scelta=input()
if(scelta=="0"):
    game()
elif(scelta=="1"):
    eseguiRicercaInProfondita()
elif(scelta=="2"):
    eseguiRicercaAdApprofondimentoIterativo()
elif(scelta=="3"):
    eseguiRicercaInAmpiezza()
else:
    pass