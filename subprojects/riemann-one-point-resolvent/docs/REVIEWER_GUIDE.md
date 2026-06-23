# Reviewer guide

Review the project in five independent passes.

## 1. Claim audit

Check that every headline is labeled verified, documented, open or numerical. Search for hidden assumptions equivalent to RH.

## 2. Mathematical audit

Check the \(\xi/\Xi\) conventions, the map \(-z^2\), connectivity after removing discrete zeros, local logarithmic-derivative poles, the Hausdorff theorem hypotheses, dominated holomorphic integration and the integer-cutoff sum–integral bound.

## 3. Formal audit

Run the pinned build and oracle. Confirm that finite theorem names match the documentation and that no project axiom or placeholder enters the imported root module. Treat the source scanner as a supplementary guard, not as kernel evidence.

## 4. Monorepo interface audit

Compare the interface contract and shared release/audit scripts byte-for-byte. Verify that construction obligations are not silently assumed by the criterion layer and that criterion results are not duplicated with divergent definitions.

## 5. Reproducibility audit

Run `make audit`, inspect every manifest change, check VERSION/CFF/CodeMeta/Python-package coherence, and reproduce the criterion ZIP twice. Confirm the active root workflow publishes this site beneath `/criterion/` and attests the criterion source archive independently.
