#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 the QI26-20 authors and contributors.
"""Build and independently test the QI26-20 arXiv source archive.

Requires Python >= 3.9, pdfLaTeX and BibTeX (TeX Live or MiKTeX).
Run from any directory: python tools/build_arxiv.py
No research notebook, hardware job, network request or upload is executed.
The build verifies files and typesetting, not private author correspondence.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'paper' / 'latex_source'
DATA_NAMES = ['derived_metrics.json', 'full_hardware_distributions.csv',
              'gm_qaoa_top20.csv', 'standard_qaoa_top20.csv']
RELEASE_CHECKS = [
    'Retain the existing author-approval emails privately; do not include them in GitHub or arXiv.',
    'Keep the deposited version consistent with the author approvals and disclosed competing interests.',
    'Select CC BY 4.0 for the manuscript in the arXiv submission form; original software uses Apache-2.0.',
    'Review the PDF produced by arXiv; local success is not an arXiv acceptance decision.',
]
LICENSE_INPUTS = {
    'anc/LICENSES/Apache-2.0.txt': ROOT / 'LICENSE',
    'anc/LICENSES/CC-BY-4.0.txt': ROOT / 'LICENSE-CONTENT',
    'anc/LICENSES/NOTICE.txt': ROOT / 'NOTICE',
}



def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def executable(*names: str) -> str:
    for name in names:
        found = shutil.which(name)
        if found:
            return found
    raise RuntimeError('Missing executable: ' + ' or '.join(names))


def run(command: list[str], cwd: Path, log: Path, steps: list[dict]) -> str:
    # Disable shell escape explicitly in pdfLaTeX commands. No shell=True.
    proc = subprocess.run(command, cwd=cwd, stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT, text=True, errors='replace',
                          timeout=120)
    log.parent.mkdir(parents=True, exist_ok=True)
    log.write_text(proc.stdout, encoding='utf-8')
    steps.append({'command': [Path(command[0]).name] + command[1:],
                  'exit_code': proc.returncode, 'log': log.name})
    if proc.returncode:
        raise RuntimeError(f'Command failed: {command}\nSee {log}\n{proc.stdout[-2000:]}')
    return proc.stdout


def stripped_tex(path: Path) -> str:
    return re.sub(r'(?<!\\)%[^\n]*', '', path.read_text(encoding='utf-8'))


def contained(source: Path, name: str) -> Path:
    if not name or Path(name).is_absolute() or '..' in Path(name).parts:
        raise ValueError(f'Unsafe or unsupported source path: {name!r}')
    resolved = (source / name).resolve()
    if not resolved.is_relative_to(source.resolve()) or not resolved.is_file():
        raise FileNotFoundError(f'Missing source dependency: {name}')
    return resolved


def dependencies() -> list[Path]:
    """Resolve this project's literal input/figure paths; fail on missing files."""
    found: set[Path] = set()
    pending = [SOURCE / 'main.tex']
    while pending:
        p = pending.pop().resolve()
        if p in found:
            continue
        found.add(p)
        for name in re.findall(r'\\(?:input|include)\s*\{([^}]+)\}', stripped_tex(p)):
            if not Path(name).suffix:
                name += '.tex'
            pending.append(contained(SOURCE, name))
    texfiles = list(found)
    for p in texfiles:
        for name in re.findall(r'\\includegraphics(?:\[[^\]]*\])?\s*\{([^}]+)\}', stripped_tex(p)):
            # The manuscript declares \\graphicspath{{Figures/}}.
            choices = [SOURCE / name, SOURCE / 'Figures' / name]
            image = next((c for c in choices if c.is_file()), None)
            if image is None:
                raise FileNotFoundError(f'Missing graphic: {name}')
            found.add(contained(SOURCE, image.relative_to(SOURCE).as_posix()))
    found.add(contained(SOURCE, 'references.bib'))
    return sorted(found, key=lambda p: p.relative_to(SOURCE).as_posix())


def compile_pdf(folder: Path, logs: Path, pdflatex: str, bibtex: str | None) -> dict:
    steps: list[dict] = []
    command = [pdflatex, '-no-shell-escape', '-interaction=nonstopmode',
               '-halt-on-error', '-file-line-error', '-recorder', 'main.tex']
    run(command, folder, logs / 'pdflatex_pass1.txt', steps)
    if bibtex:
        run([bibtex, 'main'], folder, logs / 'bibtex.txt', steps)
        if re.search(r'Warning--|error message', (folder/'main.blg').read_text(errors='replace'), re.I):
            raise RuntimeError('BibTeX warnings/errors require inspection: ' + str(folder/'main.blg'))
    stabilized = False
    previous = None
    for n in range(2, 7):
        run(command, folder, logs / f'pdflatex_pass{n}.txt', steps)
        state = tuple((folder/f'main.{ext}').read_bytes() if (folder/f'main.{ext}').exists() else b''
                      for ext in ('aux', 'toc', 'lof', 'lot', 'out'))
        if previous == state:
            stabilized = True
            break
        previous = state
    text = (folder / 'main.log').read_text(errors='replace')
    shutil.copy2(folder / 'main.log', logs / 'final_latex_log.txt')
    if (folder / 'main.blg').exists():
        shutil.copy2(folder / 'main.blg', logs / 'final_bibtex_log.txt')
    if not stabilized or re.search(r'undefined|multiply defined|Rerun to get|Rerun to get outlines', text, re.I):
        raise RuntimeError('References did not stabilize; inspect ' + str(logs))
    if re.search(r'Overfull \\[hv]box|Missing character:', text):
        raise RuntimeError('Layout overflow or missing glyphs; inspect ' + str(logs))
    warnings = re.findall(r'^.*Warning:.*$', text, flags=re.M)
    out = re.search(r'Output written on main.pdf \((\d+) pages?, (\d+) bytes\)', text)
    bbl = (folder / 'main.bbl').read_text(encoding='utf-8')
    refs = re.findall(r'\\bibitem(?:\[[^\]]*\])?\{([^}]+)\}', bbl)
    if not refs:
        raise RuntimeError('The bibliography is empty.')
    return {'steps': steps, 'auxiliary_files_stable': stabilized,
            'pages': int(out.group(1)) if out else None,
            'bibliography_items': len(refs), 'bibliography_keys': refs,
            'unresolved_references': 0, 'missing_glyphs': 0,
            'overfull_boxes': 0, 'underfull_boxes': len(re.findall(r'Underfull \\[hv]box', text)),
            'warnings': warnings}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir', type=Path, default=ROOT/'build'/'arxiv')
    args = parser.parse_args()
    dest = args.output_dir.resolve()
    dest.mkdir(parents=True, exist_ok=True)
    pdflatex = executable('pdflatex')
    # bibtex.original is a fallback for a broken Debian alternatives symlink.
    bibtex = executable('bibtex', 'bibtex.original')
    report: dict = {
        'scope': 'Technical local build and clean archive recompilation only',
        'publication_authorization': 'Dissemination approvals reported received by the corresponding author; emails remain private and are not examined by this build.',
        'release_checks': RELEASE_CHECKS,
        'license_for_original_content': 'CC-BY-4.0',
        'license_for_original_software': 'Apache-2.0',
        'arxiv_license_must_be_selected_manually': 'CC BY 4.0',
        'engine': subprocess.check_output([pdflatex, '--version'], text=True).splitlines()[0],
        'bibliography_engine': subprocess.check_output([bibtex, '--version'], text=True).splitlines()[0],
        'remote_repository_modified': False,
    }
    deps = dependencies()
    archive = dest / 'QI26-20_arxiv_sources.zip'
    with tempfile.TemporaryDirectory(prefix='qi26-20-build-') as tmp:
        tmpdir = Path(tmp)
        build = tmpdir / 'from_bib'
        build.mkdir()
        for p in deps:
            target = build / p.relative_to(SOURCE)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(p, target)
        report['fresh_bibtex_build'] = compile_pdf(build, dest/'logs_from_bib', pdflatex, bibtex)
        # Always regenerate from references.bib; never rely on a stale tracked .bbl.
        shutil.copy2(build/'main.bbl', SOURCE/'main.bbl')
        shutil.copy2(build/'main.pdf', ROOT/'paper'/'QI26_20_preprint.pdf')
        shutil.copy2(build/'main.pdf', dest/'QI26_20_preprint.pdf')
        entries = {p.relative_to(SOURCE).as_posix(): p for p in deps}
        entries['main.bbl'] = SOURCE/'main.bbl'
        for name, path in LICENSE_INPUTS.items():
            if not path.is_file():
                raise FileNotFoundError('Missing license/attribution file: ' + str(path))
            entries[name] = path
        for name in DATA_NAMES:
            entries['anc/Data/'+name] = contained(SOURCE, 'Data/'+name)
        note = (
            'QI26-20 ancillary research material\n\n'
            'The four data files in anc/Data/ are unmodified copies from the repository\n'
            'directory paper/latex_source/Data/. They are not needed to typeset main.tex.\n'
            'License texts and attribution are in anc/LICENSES/. See anc/LICENSING.txt\n'
            'for content/software scope and third-party exclusions.\n\n'
            'Repository: https://github.com/qubitmx/qi26-20-quantum-assignment-optimization\n'
        )
        scope = (
            'QI26-20 license scope\n\n'
            'Original manuscript, LaTeX content, figures and non-code research material:\n'
            'Creative Commons Attribution 4.0 International (CC-BY-4.0).\n'
            'Canonical URL: https://creativecommons.org/licenses/by/4.0/\n'
            'License text: anc/LICENSES/CC-BY-4.0.txt\n\n'
            'Original accompanying software, notebook code cells and reusable code examples:\n'
            'Apache License, Version 2.0 (Apache-2.0).\n'
            'Canonical URL: https://www.apache.org/licenses/LICENSE-2.0\n'
            'License text: anc/LICENSES/Apache-2.0.txt\n\n'
            'The full notebook and build script are provided in the repository, not this ZIP.\n'
            'Attribution is in anc/LICENSES/NOTICE.txt and the manuscript author list.\n'
            'The NOTICE reference to LICENSING.md points to the repository root.\n'
            'The content license applies only to rights held by the contributors.\n'
            'Unprotected facts are not made subject to copyright by this notice.\n'
            'Third-party materials, dependency licenses, trademarks and notices are preserved.\n'
            'The licenses apply by material type, not as alternatives for the same material.\n'
            'Select CC BY 4.0 in the arXiv submission form for the manuscript.\n'
            'No private approval correspondence or endorsement code is included.\n'
        )
        with zipfile.ZipFile(archive, 'w', compression=zipfile.ZIP_DEFLATED) as z:
            for name, p in sorted(entries.items()):
                z.writestr(name, p.read_bytes())
            z.writestr('anc/README.txt', note)
            z.writestr('anc/LICENSING.txt', scope)
        clean = tmpdir/'unpacked_archive'
        clean.mkdir()
        with zipfile.ZipFile(archive) as z:
            members = z.namelist()
            if 'main.tex' not in members or 'main.bbl' not in members:
                raise RuntimeError('Root main.tex/main.bbl missing.')
            for name in members:
                if Path(name).is_absolute() or '..' in Path(name).parts:
                    raise RuntimeError('Unsafe archive member: ' + name)
            z.extractall(clean)
        # Independent test: only the delivered ZIP is present, and BibTeX is NOT run.
        report['clean_archive_prebuilt_bbl_build'] = compile_pdf(clean, dest/'logs_clean_zip', pdflatex, None)
        pdftotext = shutil.which('pdftotext')
        if pdftotext:
            a = subprocess.check_output([pdftotext, '-layout', str(build/'main.pdf'), '-'])
            b = subprocess.check_output([pdftotext, '-layout', str(clean/'main.pdf'), '-'])
            report['clean_archive_pdf_text_identical'] = a == b
            if a != b:
                raise RuntimeError('PDF text differs between source and ZIP builds.')
        report['zip_root_validated'] = True
        report['zip_files'] = sorted(members)
        report['zip_file_count'] = len(members)
        report['used_figures'] = sum(n.startswith('Figures/') for n in members)
        report['tex_source_count'] = sum(n.endswith('.tex') for n in members)
        report['ancillary_file_count'] = sum(n.startswith('anc/') for n in members)
        report['omitted_unused_figures'] = sorted(p.name for p in (SOURCE/'Figures').iterdir()
                                                   if p.is_file() and 'Figures/'+p.name not in members)
        report['pdf_sha256'] = sha(dest/'QI26_20_preprint.pdf')
        report['arxiv_zip_sha256'] = sha(archive)
        report['main_bbl_sha256'] = sha(SOURCE/'main.bbl')
        with zipfile.ZipFile(archive) as zipped:
            report['manifest'] = {n: hashlib.sha256(zipped.read(n)).hexdigest()
                                  for n in sorted(zipped.namelist())}
    report['result'] = 'PASS - LOCAL COMPILATION AND SELF-CONTAINED LICENSED ARCHIVE'
    (dest/'BUILD_REPORT.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    (dest/'SHA256SUMS.txt').write_text(
        report['pdf_sha256']+'  QI26_20_preprint.pdf\n'+
        report['arxiv_zip_sha256']+'  QI26-20_arxiv_sources.zip\n'+
        report['main_bbl_sha256']+'  main.bbl\n', encoding='utf-8')
    print(report['result'])
    print('PDF:', dest/'QI26_20_preprint.pdf')
    print('Source ZIP:', archive)
    print('Report:', dest/'BUILD_REPORT.json')
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (RuntimeError, FileNotFoundError, ValueError, subprocess.SubprocessError) as exc:
        print('BUILD FAILED:', exc, file=sys.stderr)
        sys.exit(1)
