# Modello corretto: Experiment.measure

Il concetto centrale non e' una funzione chiamata `alice`.

Il concetto centrale non e' una funzione chiamata `bob`.

Il concetto centrale e':

```python
class Experiment:
    def measure(self, setting, context):
        ...
```

Per noi l'esperimento e' replicabile.

Questo significa che la misura ha una forma nota e ripetibile:

```text
measure(setting, context) -> +1 oppure -1
```

## Alice e Bob non sono funzioni

Nel codice, `alice` e `bob` possono esistere solo come nomi di due istanze:

```python
alice = Experiment("alice", measure_rule)
bob = Experiment("bob", measure_rule)
```

Il metodo pubblico resta sempre:

```python
measure(...)
```

Quindi non diciamo:

```text
chiamata diretta di due osservatori come funzioni
```

Diciamo:

```python
alice.measure(...)
bob.measure(...)
```

Questa differenza e' importante.

Nel primo caso sembra che Alice e Bob siano due funzioni speciali.

Nel secondo caso sono due repliche dello stesso tipo di oggetto sperimentale.

## La misura e' il metodo noto

Una prova CHSH interroga la stessa forma di misura in quattro righe:

```text
setting_a=0, setting_b=0
setting_a=0, setting_b=1
setting_a=1, setting_b=0
setting_a=1, setting_b=1
```

Ogni riga chiama:

```python
outcome_a = alice.measure(setting_a, context)
outcome_b = bob.measure(setting_b, context)
```

Poi guarda il prodotto:

```python
product = outcome_a * outcome_b
```

La tabella dei prodotti produce `S`.

## Perche' questa struttura e' migliore

Il modello diventa costruttivo:

- `Experiment` rappresenta la replicabilita' della misura.
- `measure` e' il metodo pubblico noto.
- `alice` e `bob` sono solo due istanze.
- La differenza tra `S <= 2` e `S > 2` dipende da cosa il metodo `measure`
  puo' vedere nel `context`.

La domanda corretta diventa:

```text
quale informazione entra in measure?
```

Non:

```text
che cosa fanno due funzioni diverse?
```

## Riga che dona S > 2

Nel caso costruttivo minimo, comprimiamo le quattro righe CHSH in `x`:

```text
x = 0 -> 00
x = 1 -> 01
x = 2 -> 10
x = 3 -> 11
```

La misura che rompe il limite e':

```python
def measure_product(x):
    return -1 if x == 3 else 1
```

La riga decisiva e':

```python
return -1 if x == 3 else 1
```

Quella riga dice alla misura di riconoscere la riga intera `11`.

Quindi `measure` non e' piu' una misura locale cieca rispetto all'altra
impostazione: sta usando informazione globale sulla riga CHSH.
