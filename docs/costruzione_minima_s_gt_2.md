# Costruzione minima di una misura con S > 2

Qui non partiamo dall'esperimento.

Partiamo dal metodo `measure.

Vogliamo capire qual e' la minima forma del metodo di misura che produce:

```text
S > 2
```

## Un solo parametro in ingresso

Le quattro righe CHSH vengono compresse in un solo numero `x`:

```text
x = 0  significa  A0,B0
x = 1  significa  A0,B1
x = 2  significa  A1,B0
x = 3  significa  A1,B1
```

Quindi la misura minima ha questa forma:

```python
def measure_product(x):
    ...
```

Non ci servono due funzioni `alice e `bob`: al massimo avremo due istanze `Experiment`.

Non ci serve ancora una rappresentazione fisica.

Ci serve solo una misura che dica quale prodotto vogliamo ottenere in ogni
riga:

```text
prodotto = risposta_a * risposta_b
```

## Funzione base: S = 2

La misura e'` semplice restituisce sempre `+1`:

```python
def measure_product(x):
    return 1
```

La tabella diventa:

```text
x          0   1   2   3
prodotto  +   +   +   +
```

Il valore CHSH e':

```text
S = |p0 + p1 + p2 - p3|
S = |+1 + +1 + +1 - (+1)|
S = 2
```

Questa misura non supera il limite.

## La riga che crea S > 2

Adesso cambiamo una sola cosa.

L'ultima riga deve diventare negativa:

```python
def measure_product(x):
    return -1 if x == 3 else 1
```

La riga importante e':

```python
return -1 if x == 3 else 1
```

Questa riga dice:

```text
nelle prime tre righe dammi +1
nell'ultima riga dammi -1
```

La tabella diventa:

```text
x          0   1   2   3
prodotto  +   +   +   -
```

Ora:

```text
S = |p0 + p1 + p2 - p3|
S = |+1 + +1 + +1 - (-1)|
S = 4
```

Quindi:

```text
S > 2
```

## Cosa ha donato la proprieta' alla misura?

La proprieta' non nasce dal caso.

Non nasce dal numero di prove.

Non nasce da una variabile nascosta.

Nasce da questa struttura:

```text
+++-
```

E nel codice nasce da questa riga:

```python
return -1 if x == 3 else 1
```

Quella riga introduce una dipendenza globale dalla riga CHSH completa.

Il metodo `measure sa riconoscere il caso speciale:

```text
A1,B1
```

e lo tratta in modo diverso.

## Perche' questa cosa e' importante?

Se avessimo due istanze locali separate:

```python
alice.measure(a)
bob.measure(b)
```

non potremmo scegliere liberamente solo l'ultima cella della tabella.

Il prodotto sarebbe vincolato dalla separazione tra `a` e `b`.

Invece questa misura:

```python
measure_product(x)
```

vede gia' la riga intera.

Quindi puo' dire:

```text
solo quando sono nella riga 3, cambia segno
```

Questa e' la costruzione minima.

## Comando

```bash
python3 showcase/s_4/example.py
```

Oppure:

```bash
make s_4
```
