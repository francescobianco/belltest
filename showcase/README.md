# Bell showcase

This folder contains executable CHSH experiments that classify response
functions by their observable information anatomy.

Run the scripts from the repository root:

```bash
python3 showcase/classification_table.py
python3 showcase/unknown_function_probe.py
python3 showcase/coupling_sweep.py
```

## Interpretation

The CHSH score is used here as a diagnostic instrument:

- `S <= 2`: compatible with local hidden-variable structure.
- `2 < S <= 2*sqrt(2)`: quantum-range correlation strength.
- `S > 2*sqrt(2)`: post-quantum sampler, explicit leakage, or another
  non-local/non-standard mechanism.

The extra anatomy fields make the result more useful for a black-box function:

- `signalling`: whether one side's marginal output changes when the remote
  setting changes.
- `correlation_curvature`: the CHSH-oriented second difference of the four
  correlations.
- `correlation_contrast`: the spread between the strongest and weakest
  measured correlations.
- `diagnostic_label`: a compact qualitative classification of the observed
  structure.

This is not a detector of real quantum mechanics by itself.  It is a way to
turn Bell-style measurements into a table of functional signatures.
