"""
Nome del Progetto: Riconoscimento Farmaci Italiani da un Immagine
Autore: Federico Lo Presti
Data: 22 novembre 2024
Descrizione: Data un immagine riconosce il testo presente e effettua un matching
con le righe del dataset dei farmaci italiano, in seguito ritorna la riga del dataset candidata.
Licenza: MIT
"""

import pandas as pd
import time
import re
from fuzzywuzzy import fuzz
import cv2
import easyocr

reader = easyocr.Reader(['en'])

# Percorso del dataset da caricare. Modifica questo percorso in base alla posizione del file sul tuo sistema.
dataset_path = 'Utf-8DatasetFarmaci.csv'

# Percorso dell'immagine da elaborare. Sostituisci con il percorso corretto dell'immagine che desideri utilizzare.
image_path = 'IMG_6705.JPG'

# Range in cui viene effettuato un partial matching
MIN_ACCURACY = 0.25
GOOD_ACCURACY = 0.8


def remove_dup(lista):
    new_list = []
    for old_element in lista:
        unic_wordlist = old_element[0].split()
        for word in unic_wordlist:
            if not word.isnumeric():
                if len(word) == 1:
                    continue
            found = False
            for new_element in new_list:
                if new_element[0] == word:
                    found = True
                    break
            if not found:
                new_list.append((word, old_element[1]))
    return new_list


def separa(text):
    numbers = ''
    for char in text:
        if char.isdigit() or char == ',':
            numbers += char
        else:
            return numbers
    return numbers


def check_word(word):
    if len(word) <= 3:
        return False
    if word.isnumeric():
        return False
    return True


def contains(word, row, uncertain):
    if word.isnumeric():
        # trova il numero come numero isolato
        pattern = rf'\b{word}\b'
        return re.search(pattern, row) is not None
    elif word[0].isdigit():
        num = separa(word)
        return re.search(num, row, re.IGNORECASE) is not None
    else:
        if uncertain:
            compatibily = fuzz.partial_ratio(word, str(row))
            return compatibily == 100
        else:
            pattern = rf'\b{re.escape(word)}\b'
            return re.search(pattern, row, re.IGNORECASE) is not None


def main():
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = reader.readtext(img)

    wrdlist = [(text, confidence) for _, text, confidence in results]
    wrdlist = remove_dup(wrdlist)

    print("Creazione del dataframe dal file...")
    tempo = time.time()

    df = pd.read_csv(dataset_path, delimiter=';')

    print('Creato in:', time.time()-tempo)

    candidate_list = []

    print("Calcolo corrispondenza tabella Nomi... ")
    tempo = time.time()

    for parola in wrdlist:
        uncertain = False
        # Controllo accuratezza
        if parola[1] < MIN_ACCURACY:
            continue
        if parola[1] < GOOD_ACCURACY:
            uncertain = True
        word = parola[0]
        if not check_word(word):
            continue
        for i in range(df.shape[0]):
            row = df.iloc[i]
            if contains(word, row['Nome'], uncertain):
                candidate_list.append((i, 0))

    if not candidate_list:
        print("Parole non abbastanza precise, amplio la ricerca...")
        for parola in wrdlist:
            uncertain = False
            if parola[1] <= MIN_ACCURACY:
                continue
            if parola[1] < GOOD_ACCURACY:
                uncertain = True
            word = parola[0]
            if check_word(word):
                continue
            for i in range(df.shape[0]):
                row = df.iloc[i]
                if contains(word, str(row), uncertain):
                    candidate_list.append((i, 0))

    len_list = len(candidate_list)
    print(f"Lunghezza lista filtrata: {len_list}")
    print('Completato in: ', time.time()-tempo)

    dizionario = dict(candidate_list)

    print("Classificazione...")
    tempo = time.time()
    # Controllo ricorrenza solo nelle righe della lista
    for parola in wrdlist:
        uncertain = False
        if parola[1] < MIN_ACCURACY:
            continue
        if parola[1] < GOOD_ACCURACY:
            uncertain = True
        word = parola[0]
        for elemento in candidate_list:
            row = df.iloc[elemento[0], :-1]
            # Se il dataset non ha la colonna nome eliminare la condizione
            if contains(word, row['Nome'], uncertain):
                if uncertain:
                    compatibily = fuzz.ratio(word.upper(), row['Nome'])
                    if compatibily > 90:
                        dizionario[elemento[0]] += parola[1]
                else:
                    if word.upper() == row['Nome']:
                        dizionario[elemento[0]] += parola[1]*2
            if contains(word, str(row), uncertain):
                dizionario[elemento[0]] += parola[1]
    print('Classificazione completata in', time.time()-tempo)

    ricorrenza_max = max(dizionario.values())
    riga_max = [chiave for chiave, valore in dizionario.items() if valore == ricorrenza_max]
    print(f"Cella/e trovata/e: {riga_max} \nRicorrenza massima: {ricorrenza_max}")
    print(df.iloc[riga_max[0]])


if __name__ == "__main__":
    main()
