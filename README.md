# Riconoscimento Farmaci Italiani 🏥💊

Un sistema di riconoscimento ottico (OCR) per identificare farmaci italiani da immagini e matchare i risultati con il dataset ufficiale del Ministero della Salute.

## 📋 Descrizione

Questo progetto utilizza tecniche di **Optical Character Recognition (OCR)** per estrarre testo da immagini di medicinali, seguito da analisi testuale e pattern matching per identificare il farmaco corrispondente nel database ufficiale italiano. Il sistema è ottimizzato per efficienza attraverso tecniche di filtraggio e pulizia dei dati OCR, e per efficacia tramite un sistema di classificazione a punti.

## ✨ Caratteristiche Principali

- **OCR avanzato**: Utilizza EasyOCR per l'estrazione del testo dalle immagini
- **Matching intelligente**: Sistema di corrispondenza fuzzy per gestire imperfezioni nell'OCR
- **Classificazione a punti**: Algoritmo di scoring per identificare il farmaco più probabile
- **Filtraggio adattivo**: Gestione automatica di diversi livelli di accuratezza
- **Dataset ufficiale**: Integrazione con il database dei farmaci del Ministero della Salute

## 🛠️ Requisiti

### Dipendenze Python
```bash
pip install pandas opencv-python easyocr fuzzywuzzy python-levenshtein
```

### File necessari
- `Utf-8DatasetFarmaci.csv` - Dataset dei farmaci italiani (formato CSV con separatore `;`)
- Immagine del farmaco da riconoscere (formato JPG/PNG)

## 🚀 Installazione

1. **Clona il repository**
   ```bash
   git clone https://github.com/username/riconoscimento-farmaci.git
   cd riconoscimento-farmaci
   ```

2. **Installa le dipendenze**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configura i percorsi**
   Modifica le variabili nel file `main.py`:
   ```python
   dataset_path = 'path/to/Utf-8DatasetFarmaci.csv'
   image_path = 'path/to/your/medicine_image.jpg'
   ```

## 💻 Utilizzo

### Esecuzione base
```bash
python src/main.py
```

### Parametri configurabili
Nel file `main.py` puoi modificare:
- `MIN_ACCURACY = 0.25` - Soglia minima di accuratezza OCR
- `GOOD_ACCURACY = 0.8` - Soglia per considerare una lettura "buona"

## 🔧 Come Funziona

### 1. Estrazione del Testo (OCR)
- Carica l'immagine e la converte in RGB
- Utilizza EasyOCR per estrarre testo e confidence scores
- Rimuove duplicati e filtra parole poco significative

### 2. Matching Preliminare
- Cerca corrispondenze nel campo "Nome" del dataset
- Applica filtri basati sulla confidence dell'OCR
- Crea una lista di candidati potenziali

### 3. Classificazione Avanzata
- Assegna punteggi basati su:
  - Corrispondenza esatta (peso x2)
  - Corrispondenza fuzzy (peso proporzionale alla confidence)
  - Presenza in altri campi del dataset
- Identifica il farmaco con il punteggio più alto

## 📊 Struttura del Dataset

Il dataset deve contenere almeno una colonna `Nome` con i nomi dei farmaci. Formato CSV con separatore `;`.

Esempio:
```csv
Nome;Principio_Attivo;Forma_Farmaceutica;Confezione
TACHIPIRINA 500MG;PARACETAMOLO;COMPRESSE;20 COMPRESSE
MOMENT 200MG;IBUPROFENE;CAPSULE;12 CAPSULE
```

## 🎯 Esempi di Output

```
Creazione del dataframe dal file...
Creato in: 0.032
Calcolo corrispondenza tabella Nomi... 
Lunghezza lista filtrata: 15
Completato in: 0.145
Classificazione...
Classificazione completata in 0.089
Cella/e trovata/e: [1247] 
Ricorrenza massima: 2.1
Nome                    TACHIPIRINA 500MG COMPRESSE
Principio_Attivo        PARACETAMOLO
Forma_Farmaceutica      COMPRESSE
Confezione             20 COMPRESSE
```

## 🔍 Algoritmo di Matching

Il sistema utilizza un approccio a più livelli:

1. **Matching esatto**: Ricerca corrispondenze precise nel nome del farmaco
2. **Matching fuzzy**: Utilizza algoritmi di similarità per gestire errori OCR
3. **Ricerca estesa**: Se non trova corrispondenze, amplia la ricerca a tutti i campi
4. **Scoring**: Assegna punteggi pesati basati su accuratezza e posizione del match

## 📈 Prestazioni

- **Velocità**: Elaborazione tipica in <1 secondo
- **Accuratezza**: Dipende dalla qualità dell'immagine e dalla chiarezza del testo
- **Robustezza**: Gestisce imperfezioni nell'OCR attraverso matching fuzzy

## 🤝 Contributi

I contributi sono benvenuti! Per contribuire:

1. Fai un fork del progetto
2. Crea un branch per la tua feature (`git checkout -b feature/AmazingFeature`)
3. Commit le tue modifiche (`git commit -m 'Add some AmazingFeature'`)
4. Push al branch (`git push origin feature/AmazingFeature`)
5. Apri una Pull Request

## 📝 Licenza

Questo progetto è rilasciato sotto licenza MIT. Vedi il file `LICENSE` per i dettagli.

## 👨‍💻 Autore

**Federico Lo Presti**
- Data: 22 novembre 2024
- Progetto: Riconoscimento Farmaci Italiani da Immagine

## 🐛 Problemi Noti

- Le performance dipendono dalla qualità dell'immagine
- Testo molto piccolo o sfocato può causare errori di riconoscimento
- Il sistema è ottimizzato per farmaci italiani

## 🔮 Sviluppi Futuri

- [ ] Supporto per più lingue
- [ ] Interfaccia grafica
- [ ] API REST
- [ ] Miglioramenti nell'accuratezza OCR
- [ ] Supporto per batch processing

## 📞 Supporto

Per problemi o domande, apri un issue su GitHub o contatta l'autore.

---

*Questo progetto è stato sviluppato per scopi educativi e di ricerca. Non sostituisce il parere medico professionale.*
