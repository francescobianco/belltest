# Spiegazione elementare: S < 2 e S > 2

Questo progetto usa il test CHSH come una misura molto semplice.

Abbiamo quattro situazioni:

```text
A0 con B0
A0 con B1
A1 con B0
A1 con B1
```

Ogni volta una funzione risponde solo con:

```text
+1 oppure -1
```

Poi misuriamo quanto le risposte sono correlate.

Alla fine calcoliamo:

```text
S = |E(A0B0) + E(A0B1) + E(A1B0) - E(A1B1)|
```

## Caso 1: funzione con S < 2

Questa e' una funzione locale con variabile nascosta.

Vuol dire:

- Alice ha la sua funzione.
- Bob ha la sua funzione.
- Entrambi vedono lo stesso numero nascosto `lambda`.
- Alice non vede la scelta di Bob.
- Bob non vede la scelta di Alice.

Esempio mentale:

```text
alice(setting, lambda) -> +1 oppure -1
bob(setting, lambda)   -> +1 oppure -1
```

Anche se Alice e Bob condividono `lambda`, restano separati.

Risultato tipico:

```text
S = 0.6
```

Quindi:

```text
S < 2
```

Interpretazione elementare:

```text
la funzione ha struttura, ma non rompe il limite classico
```

## Caso 2: funzione con S > 2

Qui il risultato non puo' essere spiegato da due funzioni locali classiche che
condividono solo una variabile nascosta.

Nel demo usiamo un campionatore quantum-like.

Esempio mentale:

```text
misura_congiunta(setting_a, setting_b) -> risposta_a, risposta_b
```

La funzione non e' piu' semplicemente:

```text
alice(setting_a, lambda)
bob(setting_b, lambda)
```

Produce invece una coppia di risposte gia' correlata.

Risultato tipico:

```text
S = 2.8
```

Quindi:

```text
S > 2
```

Interpretazione elementare:

```text
la correlazione e' troppo forte per il modello locale classico
```

## Differenza in una riga

```text
S < 2  -> compatibile con funzioni locali classiche
S > 2  -> non compatibile con sole funzioni locali classiche
```

## Attenzione

`S > 2` non significa automaticamente che abbiamo trovato vera fisica
quantistica.

In codice possiamo ottenere `S > 2` anche barando, per esempio facendo leggere a
Bob la scelta di Alice.

Per questo guardiamo anche la firma anatomica:

```text
signalling
contrast
diagnostic_label
```

Se `S > 2` ma il signalling e' alto, probabilmente c'e' leakage informativo.

Se `S > 2` ma il signalling e' basso, il comportamento assomiglia di piu' a una
correlazione quantum-like.

# auto_chsh

Nel CHSH normale abbiamo due funzioni:

```text
alice(...)
bob(...)
```

In `auto_chsh` invece vogliamo studiare una sola funzione confrontata con se
stessa.

La forma diventa:

```text
F(role, setting, context) -> +1 oppure -1
```

La stessa funzione `F` viene chiamata due volte:

```text
F("A", setting_a, context)
F("B", setting_b, context)
```

Quindi non stiamo piu' chiedendo:

```text
come interagiscono Alice e Bob?
```

Stiamo chiedendo:

```text
che anatomia interna ha questa singola funzione quando la uso in due ruoli?
```

`auto_chsh` serve proprio a questo: trasformare il test di Bell in una sonda
per una funzione ignota.

Comando:

```bash
python3 showcase/auto_chsh.py
```

Oppure:

```bash
make auto_chsh
```
