# Showcase

Questa cartella non contiene un framework condiviso.

Ogni esempio e autonomo e definisce al suo interno:

- `context`, dict globale che rappresenta la realta disponibile alla misura.
- `Experiment`, classe replicabile.
- `Experiment.measure(setting)`, metodo noto della misura.
- il calcolo CHSH locale al file.

`context` non viene passato a `measure`.

Dentro `measure` la lettura globale e esplicita:

```python
global context
```

## Classificazione

- `s_05/`: esempi con `S < 0.5`
- `s_10/`: esempi con `0.5 <= S < 1.0`
- `s_15/`: esempi con `1.0 <= S < 1.5`
- `s_20/`: esempi con `1.5 <= S < 2.0`
- `s_25/`: esempi con `2.0 <= S < 2.5`
- `s_30/`: esempi con `2.5 <= S < 3.0`
- `s_35/`: esempi con `3.0 <= S < 3.5`
- `s_40/`: esempi con `3.5 <= S <= 4.0`

## Comandi

```bash
make demo
make s_05
make s_10
make s_15
make s_20
make s_25
make s_30
make s_35
make s_40
```
