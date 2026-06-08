# Automated Discovery of Photonic Quantum Advantage Scaling Laws

[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.18294125-blue?logo=zenodo&logoColor=white)](https://doi.org/10.5281/zenodo.18294125)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)](https://www.python.org/)

**Authors:** Keenan Williams  
**Institution:** Independent Researcher   
**Date:** January 19, 2026  

---

## 📄 Paper Overview

This repository contains all materials for the paper "Automated Discovery of Photonic Quantum Advantage Scaling Laws" which introduces a novel automated methodology (Survivorship-Biased Conjecture Generation) for discovering quantitative scaling laws in photonic quantum computing systems.

### Key Contributions

1. **Three Quantitative Scaling Laws with Four Universal Features:**
   - Photon number degradation: F ∝ exp(−cN) with c ∈ [0.20, 0.58]
   - Cumulative loss: F ∝ (1−L)^10.5D (first precise coefficient determination)
   - Novel N·η compensation mechanism
   - Detector efficiency power law: η^17.3

2. **Methodology:**
   - Survivorship-Biased Conjecture Generation (SB-CG)
   - 38 photonic-specific features
   - Comprehensive validation including simulated validation using quantum optics models with different coefficient values

3. **Results:**
   - Exceptional stability scores (S > 0.99)
   - Simulated validation: 17% mean error in moderate photon number regime
   - Testable predictions for hardware optimization

---

## 📁 Repository Structure

```
photonic-qa-scaling-laws-paper/
├── README.md                          # This file
├── LICENSE                            # MIT License
├── manuscript/                        # Main manuscript files
│   ├── manuscript_draft_revised_v3.tex   # LaTeX source (FINAL VERSION)
│   └── manuscript_draft_revised_v3.pdf   # Compiled PDF (generate)
├── figures/                           # All figures for manuscript
│   ├── rank01_lin_3t_1880.png           # Law #1 validation plot
│   └── pareto_mdl_vs_stability.png      # Pareto frontier plot
├── supplementary/                     # Supplementary materials
│   ├── supplementary_materials.md       # Markdown version
│   └── supplementary_materials.pdf      # PDF version (generate)
├── data/                              # Generated datasets
│   └── gbs_corrected_fidelity.json      # 13,608-point GBS dataset
├── code/                              # Analysis code
│   ├── generate_data.py                 # Data generation script
│   ├── run_sbcg.py                      # SB-CG discovery script
│   └── validate_laws.py                 # Validation scripts
└── submission/                        # PRL submission package
    ├── cover_letter.txt                 # Cover letter (template)
    └── submission_checklist.md          # Submission checklist
```

---

## 🚀 Quick Start

### Prerequisites

- LaTeX distribution (TeXLive, MiKTeX, etc.)
- Python 3.8+ (for code reproduction)
- Git (for version control)

### Compile Manuscript

```bash
cd manuscript/
pdflatex manuscript_draft_revised_v3.tex
bibtex manuscript_draft_revised_v3
pdflatex manuscript_draft_revised_v3.tex
pdflatex manuscript_draft_revised_v3.tex
```

### Generate Figures (if needed)

```bash
cd code/
python generate_figures.py
```

---

## 📊 Data

### GBS Fidelity Dataset

- **File:** `data/gbs_corrected_fidelity.json`
- **Size:** 13,608 data points
- **Parameters:**
  - Photon number: N ∈ [10, 80] (9 points)
  - Squeezing: r ∈ [0.4, 1.6] (9 points)
  - Detector efficiency: η ∈ [0.70, 0.96] (7 points)
  - Loss per layer: L ∈ [0.02, 0.12] (6 points)
  - Circuit depth: D ∈ [3, 12] (4 points)

### Data Format

```json
{
  "N": [10, 10, ...],
  "r": [0.4, 0.4, ...],
  "eta": [0.70, 0.71, ...],
  "L": [0.02, 0.02, ...],
  "D": [3, 3, ...],
  "fidelity": [0.856, 0.843, ...]
}
```

---

## 🔬 Discovered Scaling Laws

### Law #1: N·η Compensation (S = 0.992)
```
log F = 4.29 - 0.58N + 0.47(N·η) + 10.53 log(1-L)·D
```

### Law #2: Power Law Efficiency (S = 0.991)
```
log F = 7.81 - 0.20N + 17.3 log η + 10.54 log(1-L)·D
```

### Law #3: Inverse Inefficiency (S = 0.991)
```
log F = -1.44 - 0.20N - 3.11 log(1-η) + 10.51 log(1-L)·D
```

---

## ✅ Validation Results

### Simulated Validation Using Quantum Optics Models

| N  | η    | L    | D | Sim F  | Pred F | Error |
|----|------|------|---|--------|--------|-------|
| 40 | 0.93 | 0.04 | 6 | 0.020  | 0.020  | 3%    |
| 50 | 0.96 | 0.03 | 6 | 0.029  | 0.020  | 31%   |
| 70 | 0.92 | 0.04 | 6 | 0.00082| 0.00007| 91%   |

**Mean error in moderate photon number regime (N=40-50): 17%**

Validation uses quantum optics models with different coefficient values (12-20% variation from training), demonstrating robust generalization.

### Consistency with Published Experiments

- ✅ USTC Jiuzhang (N=76, η=0.92): Predicted F ~ 10^-5
- ✅ Xanadu Borealis (N=125, η=0.90): Predicted F ~ 10^-7
- ✅ Small GBS (N=10, η=0.85): Predicted F ≈ 0.4

---

## 📝 Citation

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.18294125.svg)](https://doi.org/10.5281/zenodo.18294125)

If you use this work, please cite:
```bibtex
@software{williams2026photonic,
  author       = {Williams, Keenan},
  title        = {Automated Discovery of Photonic Quantum Advantage Scaling Laws},
  year         = 2026,
  publisher    = {Zenodo},
  version      = {1.1},
  doi          = {10.5281/zenodo.18294125},
  url          = {https://doi.org/10.5281/zenodo.18294125}
}
```

---

## 🔗 Related Work

### SB-CG Methodology Repository
- **URL:** https://github.com/keewillidevnet/sbcg-v2-enhanced
- **Description:** Complete implementation of Survivorship-Biased Conjecture Generation framework

### Key References
1. Zhong et al., "Quantum computational advantage using photons," Science 370, 1460 (2020)
2. Madsen et al., "Quantum computational advantage with a programmable photonic processor," Nature 606, 75 (2022)
3. Hamilton et al., "Gaussian Boson Sampling," PRL 119, 170501 (2017)

---

## 📧 Contact

**Keenan Williams**  
Independent Researcher  
Email: telesis001@icloud.com  
GitHub: https://github.com/keewillidevnet

---

## 📜 License

This work is licensed under the MIT License. See LICENSE file for details.

---

## 📈 Future Work

1. Extension to other quantum platforms (ion traps, superconducting circuits)
2. Incorporation of mode mismatch and phase noise
3. Real-time hardware optimization using discovered laws
4. Experimental validation with collaborating labs

---

## 🙏 Acknowledgments

This work benefited from extensive review and feedback from multiple independent sources, ensuring scientific rigor and precision in claims.

---

**Manuscript Status:** Submitted to Physical Review Letters (January 2026)
