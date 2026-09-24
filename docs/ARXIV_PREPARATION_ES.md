# Preparación del preprint QI26-20 para arXiv — revisión 2

Actualización: 24 de septiembre de 2026. Base: `QI26-20_repositorio_corregido.zip`.

**Estado editorial:** Iván Barrientos Salas informa que recibió por correo las
aprobaciones para la diseminación del preprint. A petición suya, la frase final
de aprobación está activa en el manuscrito, se incorporó el párrafo definitivo
de financiación y se declararon CC BY 4.0 para contenidos y Apache 2.0 para código.
Los correos privados no se inspeccionaron ni se incorporaron a los archivos públicos.
No se han creado confirmaciones, firmas, fechas de aprobación ni registros de correo.

## 1. Cambios incorporados

En `paper/latex_source/main.tex` se activó, sin `%`, la siguiente frase:

```latex
All authors reviewed and approved the final manuscript and agreed to its
submission to arXiv.
```

Se conservan el orden de los seis autores, sus afiliaciones y la descripción
individual de contribuciones. El archivo principal se llama `main.tex`.

La sección `Funding and Institutional Support` contiene exactamente:

> This work was carried out as project QI26-20 within QWorld's QIntern 2026 programme, with scientific mentorship and project coordination through Qubit.mx. The support acknowledged here is in-kind academic and organizational support, consisting of the research-training framework, mentorship, and project coordination. The authors received no specific monetary grant for this study.

Se añadió una declaración visible de licencias en `Data and Code Availability`.
El enlace del repositorio sigue siendo:
https://github.com/qubitmx/qi26-20-quantum-assignment-optimization

No se modificó la declaración de conflictos de interés ni se añadió una
aseveración colectiva de ausencia de conflictos. Las ecuaciones, resultados,
figuras, referencias, celdas ejecutables y salidas del notebook se conservaron.
El notebook recibió únicamente un aviso de licencias en la primera celda
Markdown y metadatos de licencia; no fue ejecutado de nuevo.

## 2. Licencias y archivos pertinentes

Las licencias se aplican según el tipo de material, por indicación del responsable
del proyecto:

- **CC BY 4.0** para el manuscrito y el contenido original no ejecutable.
- **Apache 2.0** para el software original, incluido el código del notebook y
  `tools/build_arxiv.py`.

El alcance detallado y las exclusiones para material de terceros están en
`LICENSING.md`. Los textos legales se distribuyen sin cambios en `LICENSE`
(Apache 2.0) y `LICENSE-CONTENT` (CC BY 4.0); `NOTICE` conserva la atribución del
proyecto y de sus seis autores. Los README, el manuscrito y el notebook indican
la separación entre contenido y código. Los nombres, marcas, derechos y
licencias de terceros no se sustituyen.

En el ZIP para arXiv los textos y avisos se conservan en `anc/LICENSES/` y
`anc/LICENSING.txt` explica el alcance. **En el formulario de arXiv debes
seleccionar CC BY 4.0 para el artículo.** Incluir avisos en el ZIP no modifica la
selección de licencia en tu cuenta. Apache 2.0 corresponde al software; no
sustituye la licencia del artículo.

Fuentes oficiales de los textos y del selector de licencia:
https://creativecommons.org/licenses/by/4.0/legalcode.en
https://www.apache.org/licenses/LICENSE-2.0
https://info.arxiv.org/help/license/index.html

## 3. Dos ZIP con propósitos diferentes

El ZIP de repositorio contiene la carpeta
`qi26-20-quantum-assignment-optimization/`, incluidos los materiales científicos
originales, los avisos de licencia, las instrucciones y el PDF regenerado en
`paper/QI26_20_preprint.pdf`. Los fuentes siguen dentro de `paper/latex_source/`.

El ZIP para arXiv se abre directamente con esta estructura, sin carpeta exterior:

```text
main.tex
main.bbl
references.bib
Sections/                 # 10 archivos .tex
Appendices/               # 4 archivos .tex
Figures/                  # 13 imágenes utilizadas
anc/
  README.txt
  LICENSING.txt
  LICENSES/
    Apache-2.0.txt
    CC-BY-4.0.txt
    NOTICE.txt
  Data/                   # 4 archivos de datos originales
```

Contiene 39 archivos. No incluye el PDF compilado, el notebook, archivos
auxiliares de LaTeX, correos, aprobaciones privadas ni códigos de endorsement.
Las dos figuras no utilizadas permanecen en el repositorio, pero no en el ZIP
para arXiv. Los datos de `anc/Data/` son copias idénticas a los originales.

El paquete entregado se denomina `QI26-20_arxiv_sources_v2.zip`. El script genera
el mismo tipo de paquete con el nombre genérico `QI26-20_arxiv_sources.zip`.

## 4. Recompilar y reempaquetar

Requisitos: Python 3.9 o posterior, pdfLaTeX y BibTeX.
Desde la raíz del repositorio, en PowerShell:

```powershell
py -3 tools/build_arxiv.py
if ($LASTEXITCODE -ne 0) { throw 'La compilación o la verificación falló.' }
```

En Linux/macOS:

```bash
python3 tools/build_arxiv.py
```

El script regenera `main.bbl` desde `references.bib`, compila hasta estabilizar
índices y referencias, actualiza `paper/QI26_20_preprint.pdf`, crea un ZIP mínimo
con avisos de licencia y datos complementarios, y lo descomprime en otra carpeta
para compilar exclusivamente desde los archivos entregados. La segunda prueba
utiliza el `.bbl` incluido y no ejecuta BibTeX. Los resultados, hashes y logs
se escriben en `build/arxiv/`.

La excepción `!paper/latex_source/main.bbl` permanece en `.gitignore`.
Para cambiar una referencia, edita `references.bib`, no `main.bbl`.
El script no ejecuta el notebook, no solicita hardware, no usa credenciales y
no publica archivos. No subas `build/` completo a GitHub ni a arXiv.

Después de cualquier modificación al manuscrito o a sus avisos de licencia,
regenera el ZIP; no reutilices el archivo anterior. Una recompilación puede
cambiar el hash del PDF por metadatos aunque el contenido visible no cambie.

## 5. Confirmaciones privadas: conservar las que ya recibiste

Guarda los correos auténticos y una copia identificada del material autorizado
**fuera del repositorio público y fuera del ZIP para arXiv**. Por ejemplo:

```text
%USERPROFILE%\Documents\QI26-20_PRIVATE_RELEASE\2026-09-24_revision2\
  QI26_20_preprint.pdf
  QI26-20_arxiv_sources_v2.zip
  REGISTRO_APROBACIONES.md
  evidence/
```

`evidence/` es la ubicación recomendada para las respuestas reales de los autores.
No se genera esa carpeta en esta entrega ni se incluyen respuestas simuladas.
Conserva los remitentes, fechas y relación con la versión autorizada. La frase
impresa en el PDF no reemplaza la correspondencia privada. Asegura que los
alcances de la autorización sean coherentes con el depósito y las licencias
indicadas, sin convertir una aprobación limitada en una autorización distinta.

Los hashes actualizados están en `paper/verification/SHA256SUMS.txt`.
El código de endorsement pertenece a otro trámite; no lo incorpores a ningún
archivo del repositorio ni a los fuentes públicos.

## 6. Incorporación a GitHub y depósito

Los ZIP contienen cambios locales; esta entrega no creó commits ni modificó
GitHub. Extrae el ZIP completo, compara los archivos con tu rama actual y conserva
cualquier trabajo posterior de los colaboradores. Los cambios respecto al ZIP
anterior están listados en `paper/verification/CHANGES.md`.

En un clon limpio, una secuencia posible es:

```powershell
git status --short
# Resuelve o respalda los cambios locales antes de continuar.
git switch -c prepare-arxiv-20260924-r2
# Copia los archivos revisados desde el ZIP a este clon.
git diff --check
git diff --stat
git add LICENSE LICENSE-CONTENT LICENSING.md NOTICE
git add README.md QI26_20_QUBO_QAOA_GM_QAOA_Benchmark.ipynb
git add paper/README.md paper/latex_source/README.md
git add paper/latex_source/main.tex paper/latex_source/main.bbl
git add paper/QI26_20_preprint.pdf paper/verification
git add docs/ARXIV_PREPARATION_ES.md tools/build_arxiv.py
git diff --cached --stat
git commit -m "Finalize preprint declarations and content/code licenses"
git push -u origin prepare-arxiv-20260924-r2
```

Si tu clon todavía no contiene la revisión técnica anterior, incorpora también
los archivos nuevos/modificados de esa revisión, incluidas la excepción de
`.gitignore` y la corrección del apéndice D. No uses `git push --force` ni añadas
correos, firmas, tokens, claves o la carpeta privada.

Al completar el depósito, carga únicamente el ZIP para arXiv, selecciona
`main.tex` y pdfLaTeX cuando corresponda, elige **CC BY 4.0** e inspecciona el PDF
que genere arXiv. La compilación local no es una decisión de moderación ni
sustituye la revisión de ese PDF.
