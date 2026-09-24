# Informe de compilación y empaquetado — revisión 2

Fecha: 24 de septiembre de 2026.
Resultado: **CORRECTO** en las dos pruebas independientes.

## Pruebas ejecutadas

Primera: desde los fuentes, pdfLaTeX + BibTeX + pasadas adicionales de pdfLaTeX
hasta estabilizar referencias e índices. Segunda: desde el ZIP descomprimido
en otra carpeta, únicamente con pdfLaTeX y el `main.bbl` incluido.

Ambas pruebas produjeron 33 páginas y 11 referencias bibliográficas. No hubo
errores de compilación, referencias indefinidas, glifos ausentes, cajas
desbordadas ni cajas insuficientemente llenas. El texto de ambos PDF coincide.
Los pasos y códigos de salida se registran en `BUILD_REPORT.json`.

Se conserva un aviso no bloqueante de `epstopdf`: `Shell escape feature is not
enabled.` La ejecución de programas externos se desactivó explícitamente con
`-no-shell-escape`; las figuras utilizadas son PNG y no requieren conversión EPS.

Motor: pdfTeX 3.141592653-2.6-1.40.26 (TeX Live 2025/dev/Debian).
Bibliografía: BibTeX (`bibtex.original`, alternativa local al enlace del sistema).

## Paquete de fuentes

39 archivos, sin carpeta exterior. `main.tex` y `main.bbl` están en la raíz;
se incluyen `references.bib`, 10 secciones, 4 apéndices, 13 figuras utilizadas,
4 datos complementarios, 2 textos de licencia, 1 aviso de atribución y 2 avisos
de material complementario/alcance. El ZIP no contiene el notebook ni el PDF.
Todos los miembros del ZIP tienen un hash en `BUILD_REPORT.json`.

El nombre exportado es `QI26-20_arxiv_sources_v2.zip`; corresponde a los mismos
bytes del archivo `QI26-20_arxiv_sources.zip` que generó y comprobó el script.

## Comprobación visual e integridad

Se renderizaron y compararon las 33 páginas con PyMuPDF. Solo la página 23 difiere
de la versión anterior y fue inspeccionada visualmente: las declaraciones están
completas y no presentan solapamientos ni recortes. Las otras 32 páginas son
idénticas en esa comparación de renderizado.

Se comprobaron los bytes de las diez secciones científicas, cuatro apéndices,
figuras, datos, resultados, referencias, requisitos y presentación: no cambiaron.
El notebook solo recibió el aviso de licencia y metadatos correspondientes;
se compararon sus celdas ejecutables, salidas y metadatos previos sin diferencias.
No se ejecutó nuevamente el notebook ni hardware cuántico.

## Alcance administrativo

El autor de correspondencia informa que recibió las aprobaciones de diseminación
por correo. La frase final se activó según esa indicación y el párrafo de
financiación se reemplazó literalmente por el texto que proporcionó. Las
licencias se incorporaron por su instrucción: contenido original CC BY 4.0 y
software original Apache 2.0, preservando los derechos de terceros.

Los correos no se inspeccionaron ni se incluyeron en los paquetes. No se fabricó
ninguna aprobación. No se modificó GitHub ni se depositó el trabajo en arXiv.
Seleccionar la licencia en arXiv y revisar el PDF de su servidor son operaciones
separadas de estas pruebas locales.
