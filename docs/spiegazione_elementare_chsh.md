# Spiegazione elementare: S < 2 e S > 2

Questo progetto usa il test CHSH come una misura molto semplice.

Abbiamo quattro situazioni:

```text
A0 con B0
A0 con B1
A1 con B0
A1 con B1
```

Ogni volta il metodo measure risponde solo con:

```text
+1 oppure -1
```

Poi misuriamo quanto le risposte sono correlate.

Alla fine calcoliamo:

```text
S = |E(A0B0) + E(A0B1) + E(A1B0) - E(A1B1)|
```

## Caso 1: misura con S < 2

Questa e' una misura locale con variabile nascosta.

Vuol dire:

- `alice` e una istanza di `Experiment`.
- `bob` e una istanza di `Experiment`.
- Entrambi vedono lo stesso numero nascosto `lambda`.
- `alice.measure` non vede la scelta remota.
- `bob.measure` non vede la scelta remota.

Esempio mentale:

```text
alice.measure(setting, context) -> +1 oppure -1
bob.measure(setting, context)   -> +1 oppure -1
```

Anche se le due istanze condividono `lambda`, i loro metodi `measure` restano locali.

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
la misura ha struttura, ma non rompe il limite classico
```

## Caso 2: misura con S > 2

Qui il risultato non puo' essere spiegato da due istanze locali classiche di `Experiment` che
condividono solo una variabile nascosta.

Nel demo usiamo un campionatore quantum-like.

Esempio mentale:

```text
misura_congiunta(setting_a, setting_b) -> risposta_a, risposta_b
```

La misura non e piu semplicemente:

```text
alice.measure(setting_a, context)
bob.measure(setting_b, context)
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
S < 2  -> compatibile con istanze locali classiche di `Experiment`
S > 2  -> non compatibile con sole istanze locali classiche di `Experiment`
```

## Attenzione

`S > 2` non significa automaticamente che abbiamo trovato vera fisica
quantistica.

In codice possiamo ottenere `S > 2` anche barando, per esempio facendo leggere a
`bob.measure` la scelta di `alice`.

Per questo guardiamo anche la firma anatomica:

```text
signalling
contrast
diagnostic_label
```

Se `S > 2` ma il signalling e' alto, probabilmente c'e' leakage informativo.

Se `S > 2` ma il signalling e' basso, il comportamento assomiglia di e'' a una
correlazione quantum-like.

# auto_chsh

Nel CHSH normale abbiamo due istanze replicabili:

```text
alice.measure(...)
bob.measure(...)
```

In `auto_chsh` invece vogliamo studiare un solo metodo `measure confrontato con se stesso.

La forma diventa:

```text
F(role, setting, context) -> +1 oppure -1
```

Lo stesso metodo `measure viene chiamato su due istanze:

```text
alice.measure(setting_a, context)
bob.measure(setting_b, context)
```

Quindi non stiamo e'' chiedendo:

```text
che cosa succede quando replichiamo lo stesso esperimento in due istanze?
```

Stiamo chiedendo:

```text
che anatomia interna ha il metodo measure quando lo replico in due istanze?
```

`auto_chsh` serve proprio a questo: trasformare il test di Bell in una sonda
per una misura ignota.

Comando:

```bash
python3 showcase/auto_chsh.py
```

Oppure:

```bash
make auto_chsh
```
