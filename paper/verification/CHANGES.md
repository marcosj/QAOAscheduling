# Cambios de la revisión 2

Base: `QI26-20_repositorio_corregido.zip`. Actualización: 24 de septiembre de 2026.
No se eliminó ningún archivo de esa instantánea ni se modificó GitHub.

## Correcciones solicitadas

La aprobación final de autores está activa en `main.tex`. El párrafo de
financiación reproduce exactamente el texto suministrado por Iván. El manuscrito,
README, notebook, avisos y paquete de fuentes señalan CC BY 4.0 para contenido
original y Apache 2.0 para software original. Los textos legales completos se
conservan en `LICENSE` y `LICENSE-CONTENT`, con alcance y atribuciones por separado.

## Archivos modificados respecto al ZIP anterior

- `QI26_20_QUBO_QAOA_GM_QAOA_Benchmark.ipynb`
- `README.md`
- `docs/ARXIV_PREPARATION_ES.md`
- `paper/QI26_20_preprint.pdf`
- `paper/README.md`
- `paper/latex_source/README.md`
- `paper/latex_source/main.tex`
- `paper/verification/BUILD_REPORT.json`
- `paper/verification/BUILD_REPORT_ES.md`
- `paper/verification/SHA256SUMS.txt`
- `paper/verification/logs_clean_zip_final_latex_log.txt`
- `paper/verification/logs_from_bib_final_latex_log.txt`
- `tools/build_arxiv.py`

`main.bbl` se regeneró con BibTeX; sus bytes coinciden con la versión anterior,
pues no cambiaron las citas ni `references.bib`.

## Archivos nuevos

- `LICENSE`
- `LICENSE-CONTENT`
- `LICENSING.md`
- `NOTICE`

## Integridad científica y correspondencia

Las diez secciones, los cuatro apéndices, todas las figuras, datos, resultados,
referencias, requisitos y presentación se conservaron sin cambios. Las celdas de
código, salidas, orden de celdas y metadatos previos del notebook no cambiaron;
solo se añadieron un aviso de licencia al texto inicial y metadatos de licencia.

El PDF se regeneró y se comparó visualmente con el anterior: únicamente la página
23 cambió. Ambas compilaciones produjeron 33 páginas y 11 referencias.
No se ejecutó el notebook ni hardware cuántico. No se incluyen correos,
firmas, aprobaciones privadas ni el código de endorsement.
