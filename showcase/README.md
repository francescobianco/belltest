# Showcase

Questa cartella non contiene un framework condiviso.

Ogni esempio e' autonomo e definisce al suo interno:

- `Environment` globale, cioe' la realtà indipendente.
- `ENV`, istanza globale dell'ambiente.
- `Experiment`, classe replicabile.
- `Experiment.measure(setting)`, metodo noto della misura.
- il calcolo CHSH locale al file.

`ENV` non viene passato a `measure`.

La misura riceve solo:

```python
measure(setting)
```

## Classificazione

- `s_1/`: esempi con `S < 1`
- `s_2/`: esempi con `1 <= S < 2`
- `s_3/`: esempi con `2 <= S < 3`
- `s_4/`: esempi con `3 <= S <= 4`

## Comandi

```bash
python3 showcase/s_1/example.py
python3 showcase/s_2/example.py
python3 showcase/s_3/example.py
python3 showcase/s_4/example.py
```
