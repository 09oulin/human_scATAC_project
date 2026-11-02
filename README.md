# human_scATAC_project — Human Consensus Motif Atlas

A standalone static website for 461 human consensus motifs, 131 cell subtypes and reconciled instance statistics. Search, category and pattern filters, sorting, sequence logos, motif details, subtype distributions and TSV downloads work entirely in the browser.

## Deploy to GitHub Pages

1. Put this project's contents in a GitHub repository, with `.github/`, `dist/`, `validate.py` and this README at the repository root. Include the hidden `.github` folder.
2. In the repository, open **Settings → Pages → Build and deployment → Source**, and select **GitHub Actions**.
3. When you are ready to publish the website publicly, run **Actions → Deploy motif atlas to GitHub Pages → Run workflow**. Deployment is manual so pushing to this private repository does not publish the data.
4. The deployment job reports the actual website URL. A typical project Pages URL is `https://OWNER.github.io/REPOSITORY/`.

The workflow uploads only `dist/`. It does not require Node, third-party Python packages, Sites, an API key, or the original 104 MB HTML. All asset paths are relative, so repository subpaths work. GitHub Pages availability depends on your repository visibility and plan; see https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages .

## Local preview and validation

Open `dist/index.html` directly, or run `python3 -m http.server 8765 --directory dist` and visit http://localhost:8765 . Run `python3 validate.py` to verify assets, identifiers and total counts.

## Rebuild with updated inputs

The original input snapshots remain in the local `source/` directory and are intentionally excluded from Git. Put the final motif HTML, `motif_summary.tsv`, `motif_counts_by_subtype.tsv` and `celltype_summary.tsv` there, then run `python3 build.py` followed by `python3 validate.py`. Commit the updated `dist/` assets to publish the update. The builder validates complete ID joins and subtype sums before emitting files.

Source paths:

- `/home/oulin/chrombpnet/chrombpnet_use_snakefile/Hs_MotifCompendium/output/threshold_90_recforce_95/html/motif_table_0927_final.html`
- `/home/oulin/chrombpnet/chrombpnet_use_snakefile/qc_metrics/human/summarize_reconciled`

## Data interpretation

Motif names join on `annotation3 = motif_name`; all 461 names match. The supplied total of 111,612,517 sums instances across subtype records and is not a deduplicated count of genomic loci. Original motif class (`posneg`) and instance record class (`pattern_class`) are retained separately. Consensus construction seqlets are distinct from reconciled genomic instances. No genome build is inferred from filenames.

Forward/reverse logos and reference scores are taken from the original table. Missing consensus strings are preserved as supplied. Reference scores are not TOMTOM q-values. See the webpage's Data & downloads tab for provenance and downloadable summaries.

## Planned repository

Owner: `09oulin`; repository: `human_scATAC_project`; visibility: private. Repository privacy does not make a personal GitHub Pages website private. Keep Pages disabled until public website publication is intended.

PNG logos are deduplicated into sixteen `dist/logos-*.js` assets. Original individual PNGs can be regenerated locally and are excluded from Git; the deployed website uses the packed assets without external services.
