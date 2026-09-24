# QI26-20 — Quantum Computing for Combinatorial Assignment Optimization

## A Reproducible QUBO–QAOA Benchmark for Generalized Bipartite Assignment on NISQ Hardware

This repository contains the executable research artifact developed for **QI26-20 / QIntern 2026 (QWorld)**. The project studies generalized bipartite assignment as a **Quadratic Unconstrained Binary Optimization (QUBO)** problem and benchmarks classical optimization, standard **Quantum Approximate Optimization Algorithm (QAOA)**, and **Grover-Mixer QAOA (GM-QAOA)** in ideal simulation and on real IBM Quantum hardware.

The central objective is not to claim quantum advantage. Instead, the project establishes a controlled and reproducible benchmark in which the same assignment instances, scoring function, feasibility decoder, classical ground truth, and hardware protocol are used to determine what the quantum algorithms actually achieve on small NISQ-era problems.

---

## Research Team

- **Iván Barrientos Salas** — Mentor, conceptualization, supervision, scientific auditing, integration of generalized capacities and GM-QAOA, hardware methodology, validation, and manuscript preparation
- **Ilia Fazeli**
- **Jiya Maurya**
- **Marcos Jiménez**
- **Abhishek Raj**
- **Satkar Juneja**

**QI26-20 / QIntern 2026 Research Team**

---

## Project Overview

Assignment problems occur whenever agents must be matched with resources or tasks under constraints. They appear in scheduling, logistics, resource allocation, operations research, and enterprise systems.

QI26-20 formulates this problem in QUBO form and evaluates a complete hybrid workflow:

1. Mathematical formulation of generalized bipartite assignment.
2. Deterministic synthetic instances.
3. Classical optimization baselines.
4. Standard QAOA in ideal simulation.
5. GM-QAOA with feasible-subspace state preparation and a Grover mixer.
6. Transpilation and execution on IBM Quantum hardware.
7. Error, resource, and scientific-traceability analysis.

The implemented benchmark includes both **one-to-one assignment** and **exact-capacity assignment**.

### Fixed benchmark instances

| Instance | Problem | Qubits | Feasible states | Classical optimum |
|---|---|---:|---:|---:|
| `reference_3x3` | 3×3 one-to-one | 9 | 6 | 2.70 |
| `one_to_one_4x4` | 4×4 one-to-one | 16 | 24 | 3.08 |
| `exact_capacity_4x2` | 4×2 exact capacity, C=(2,2) | 8 | 6 | 3.25 |

---

## Classical Ground Truth

Exact enumeration and the Hungarian algorithm establish the reference optima for the one-to-one cases. Greedy and simulated annealing are included as additional baselines.

The classical experiments confirm:

- `reference_3x3`: optimum **2.70**.
- `one_to_one_4x4`: optimum **3.08**; greedy obtains 2.80 and simulated annealing 3.01.
- `exact_capacity_4x2`: optimum **3.25**.

These baselines are important because the quantum results are evaluated against known global optima rather than against weak or ambiguous reference solutions.

---

## Standard QAOA Results

Standard QAOA was evaluated with ideal statevector simulation at depths **p = 1, 2, 3**.

For the 3×3 instance, feasible probability increased from **0.36% at p=1** to **11.86% at p=3**, with an optimal-state probability of **4.15% at p=3**.

For the 4×4 instance, the exact optimum of **3.08** was recovered at **p=2**. The experiment also demonstrates that increasing QAOA depth does not guarantee monotonic improvement: the p=3 result was worse for this instance.

The clearest standard-QAOA progression occurs on the 4×2 exact-capacity problem:

| p | Feasible probability | Optimal probability | Best score |
|---:|---:|---:|---:|
| 1 | 9.16% | 2.34% | 3.25 |
| 2 | 34.89% | 5.41% | 3.25 |
| 3 | **43.99%** | **6.11%** | **3.25** |

Standard QAOA is therefore functional on the benchmark: it recovers optimal solutions in multiple tested configurations, although its behavior is instance- and depth-dependent.

---

## GM-QAOA: Main Ideal-Simulation Result

GM-QAOA was evaluated at **p=1** using exact feasible-state preparations for the three fixed benchmark instances.

| Instance | Feasible probability | Optimal probability | Best score | State-preparation fidelity | Circuit fidelity |
|---|---:|---:|---:|---:|---:|
| `reference_3x3` | **100%** | **69.23%** | 2.70 | 1.0 | 1.0 |
| `one_to_one_4x4` | **100%** | **10.74%** | 3.08 | 1.0 | 1.0 |
| `exact_capacity_4x2` | **100%** | **50.37%** | 3.25 | 1.0 | 1.0 |

This is the strongest ideal result of Phase 1.

The implemented feasible-state preparation and Grover mixer preserve the fixed feasible subspaces exactly in ideal simulation. Consequently, all probability mass remains on feasible assignments, while the optimal-state probabilities are substantially higher than those obtained with standard QAOA for the corresponding tested configurations.

This result applies to the exact fixed-size constructions implemented here. It is **not** a claim of a general scalable state-preparation method.

---

## IBM Quantum Hardware Experiment

The end-to-end pipeline was executed on the **`ibm_marrakesh`** IBM Quantum backend using the `exact_capacity_4x2` instance.

Both p=1 circuits were executed under a controlled protocol:

- Same backend
- Same IBM Runtime job
- 1,024 shots per circuit
- Optimization level 3
- Dynamical decoupling
- Gate twirling
- Same transpilation/hardware methodology

**IBM Quantum Runtime job:** `d9vl8qfo3ppc73akfak0`

### Hardware results

| Metric | Standard QAOA | GM-QAOA |
|---|---:|---:|
| Best feasible score | **3.25** | **3.25** |
| Optimization gap | **0.00** | **0.00** |
| Observed feasible probability | 7.71% | 11.91% |
| Observed optimal probability | 1.56% | 2.83% |
| Transpiled depth | 143 | 1,357 |
| Instructions | 293 | 2,180 |
| Native CZ gates | 63 | 496 |

**Both physical circuits sampled the exact optimal bitstring `10011001`.**

Thus, both standard QAOA and GM-QAOA reached real quantum hardware and sampled the known global optimum.

However, best-sample success must not be confused with high-probability or statistically reliable optimum recovery.

---

## Ideal vs. Hardware Behavior

The hardware experiment exposes the most important physical limitation observed in the study.

For standard QAOA on the 4×2 instance:

- Ideal feasible probability: **9.16%**
- Hardware feasible probability: **7.71%**
- Ideal optimal probability: **2.34%**
- Hardware optimal probability: **1.56%**

For GM-QAOA:

- Ideal feasible probability: **100%**
- Hardware feasible probability: **11.91%**
- Ideal optimal probability: **50.37%**
- Hardware optimal probability: **2.83%**

The optimum was therefore present in both hardware distributions, but GM-QAOA's strong ideal probability concentration did not survive physical execution.

The measured global-distribution errors reinforce this conclusion:

| Metric | Standard QAOA | GM-QAOA |
|---|---:|---:|
| Total variation distance (TVD) | 0.208 | 0.881 |
| Hellinger distance | 0.235 | 0.828 |
| Classical fidelity | 0.893 | 0.098 |

The correct interpretation is:

> **The optimum was sampled on hardware; it was not recovered with high probability.**

---

## Transpilation and Physical Overhead

GM-QAOA does not fail as an ideal feasible-subspace ansatz. The principal issue observed in this implementation is the physical cost of realizing its exact state preparation and selective-phase operations.

Relative to standard QAOA, the transpiled GM-QAOA circuit required approximately:

- **9.49×** greater circuit depth
- **7.44×** more instructions
- **7.87×** more native CZ gates

Standard QAOA transpiled to depth **143** with **63 CZ gates**, while GM-QAOA reached depth **1,357** with **496 CZ gates**.

These measurements strongly support circuit length and synthesis/routing overhead as major explanatory factors for the degradation observed on hardware, although this experiment does not establish circuit depth alone as a causal explanation.

---

## What the Project Demonstrates

The executed artifact supports the following conclusions:

1. **The generalized QUBO formulation works** for both one-to-one and fixed exact-capacity assignment.
2. **Standard QAOA is functional** and recovers optimal scores in multiple tested configurations.
3. **GM-QAOA works as an ideal feasible-subspace ansatz** for the fixed benchmark instances, achieving 100% feasibility and unit state-preparation/circuit fidelity.
4. **The complete workflow reaches real quantum hardware.**
5. **Both physical circuits sampled the exact optimum** on `ibm_marrakesh`.
6. **Hardware overhead is measurable and consequential:** the implemented GM-QAOA circuit is substantially deeper and more expensive after transpilation.
7. **The repository provides traceable evidence** through the executable notebook, result tables, hardware metadata, claims checklist, compliance matrix, presentation, and preprint.

---

## Preliminary Originality Assessment

The individual components of this project have established precedents: QUBO assignment formulations, standard QAOA, Grover-mixer QAOA, constraint-preserving mixers, IBM Quantum execution, and distribution/error metrics are not individually claimed as novel.

The preliminary literature review instead concerns their **controlled experimental combination**:

- exact-capacity bipartite QUBO;
- standard QAOA versus GM-QAOA;
- matched IBM backend and Runtime job;
- full-distribution degradation analysis; and
- transpilation-resource analysis.

**To the extent of the literature search conducted, no prior publication was found reporting this same experimental combination.**

This is deliberately a narrow and provisional originality statement. The literature review was heterogeneous and is not claimed to be exhaustive of all arXiv, IEEE Xplore, Scopus, or other indexed literature.

---

## Scientific Scope and Limitations

This repository does **not** claim:

- quantum advantage;
- practical runtime superiority over classical algorithms;
- high-probability optimum recovery on current hardware;
- preservation of the GM-QAOA feasible subspace on the QPU;
- a general scalable feasible-state preparation construction;
- universal hardware-overhead ratios;
- scalability beyond the small benchmark instances studied here.

At these problem sizes, classical exact and Hungarian methods remain substantially more efficient. The purpose of Phase 1 is a **correctness, reproducibility, NISQ implementation, and error/resource benchmark**, not a classical-versus-quantum runtime competition.

---

## Repository Contents

```text
.
├── QI26_20_QUBO_QAOA_GM_QAOA_Benchmark.ipynb
├── QI26-20_QIntern2026_QWorld_Style_Presentation.pdf
├── requirements.txt
├── results/
│   ├── phase1_classical_baselines.csv
│   ├── phase1_standard_qaoa_depth_results.csv
│   ├── phase1_gm_qaoa_ideal_results.csv
│   ├── phase1_hardware_summary.csv
│   ├── phase1_hardware_top_outcomes.csv
│   ├── phase1_transpilation_metrics.csv
│   ├── phase1_claims_checklist.csv
│   └── phase1_compliance_matrix.csv
└── paper/
    ├── QI26_20_preprint.pdf
    └── latex_source/
        ├── main.tex
        ├── references.bib
        ├── Sections/
        ├── Appendices/
        ├── Figures/
        └── Data/
```

The notebook is the primary executable artifact. The `results/` directory contains machine-readable evidence for the reported numerical results, while `paper/` contains the preprint and its complete LaTeX source.

---

## Reproducibility

Install the Python dependencies with:

```bash
pip install -r requirements.txt
```

Then execute:

```text
QI26_20_QUBO_QAOA_GM_QAOA_Benchmark.ipynb
```

The repository preserves fixed benchmark instances, deterministic seeds where applicable, common scoring and feasibility logic, exported CSV/JSON evidence, hardware metadata, and an explicit claims boundary.

Execution on IBM Quantum hardware requires appropriate IBM Quantum access and credentials. **Do not commit API tokens or private credentials to the repository.**

---

## Next Research Directions

Phase 1 establishes the experimental foundation for subsequent work. The principal next steps are:

1. Repeat matched hardware jobs across time and multiple quantum backends.
2. Replace generic fixed feasible-state preparation with structured, more scalable circuits.
3. Perform mitigation and ablation studies for dynamical decoupling, twirling, readout effects, and postselection.
4. Construct controlled problem families across increasing sizes and capacity structures.
5. Report total physical resource costs and statistically aggregate repeated hardware experiments.
6. Extend the assignment model toward more realistic capacity-constrained and enterprise resource-allocation problems.

---

## Citation and Research Status

This repository represents the **Phase 1 QI26-20 / QIntern 2026 research artifact**.

The associated preprint documents the mathematical formulation, classical baselines, standard QAOA and GM-QAOA methodology, IBM Quantum experiment, distribution-error analysis, transpilation overhead, limitations, and reproducibility evidence.

**Research status:** Phase 1 complete. The results establish a reproducible small-instance benchmark and a foundation for a broader experimental campaign; they do not establish quantum advantage.


## arXiv source preparation

The source package and local PDF build have been checked. `paper/latex_source/main.bbl` is generated and intentionally tracked. Run `python3 tools/build_arxiv.py` from the repository root to regenerate and independently test the submission ZIP.

The corresponding author reports that the preprint dissemination approvals have been received by email. The manuscript now contains the final author-approval sentence and the confirmed statement that no specific monetary grant was received. Approval correspondence remains private and is not distributed with the repository or the arXiv sources. Local compilation is not an arXiv acceptance decision.


## Licenses

Original manuscript and non-code content: **CC BY 4.0**. Original software, including notebook code cells: **Apache 2.0**. Third-party materials retain their respective licenses and notices.

See [LICENSING.md](LICENSING.md), [LICENSE-CONTENT](LICENSE-CONTENT), [LICENSE](LICENSE), and [NOTICE](NOTICE). The notebook includes an explicit mixed-content license notice. Select **CC BY 4.0** for the manuscript when submitting to arXiv.

See [the preparation guide](docs/ARXIV_PREPARATION_ES.md) for packaging, private record-keeping, and submission steps.
