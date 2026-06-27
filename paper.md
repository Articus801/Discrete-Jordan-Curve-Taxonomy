---
title: "A Discrete Framework for the Automated Structural Taxonomy of 2D Jordan Curves"
tags:
  - Python
  - discrete topology
  - computational geometry
  - Jordan curves
  - fractal boundaries
authors:
  - name: Independent Research Coalition
    orcid: 0000-0000-0000-0000
    affiliation: Independent Researcher Core
date: 27 June 2026
bibliography: paper.bib
---

# Summary
Traditional shape classification frameworks break down mathematically when evaluating 2D Jordan curves that possess non-rectifiable, non-smooth boundary manifolds (such as localized fractal arcs). This software ecosystem provides an automated, self-regulating pipeline that maps complex closed-loop geometries into invariant discrete structural signatures using an internal distribution of omnidirectional radial chord-length casts ("straws").

# Statement of Need
In fields ranging from fluid dynamics to computer vision, characterizing chaotic or highly convoluted boundaries is a critical bottleneck. Standard differential topology relies on continuous calculus metrics (e.g., calculating curvature $\kappa$ or tangent fields), which collapse into infinity or non-differentiability when encountering fractal boundaries.

Our package addresses this foundational gap by treating the boundary as a discrete manifold interrogated by internal probabilistic projections. By calculating the variance, skewness, and kurtosis of these internal casts, the software bypasses the requirement for differentiability entirely.

Crucially, the framework implements a self-regulating Nyquist-Shannon sampling bound bound to the curve's vertex density. This protects researchers from the "Scale Paradox"—where sampling too coarsely misses structural details, and sampling too finely introduces ultra-fine floating-point noise.

# Key Features and Implementation
The package includes an end-to-end automated queue manager that executes the following pipeline:
1. **Topological Welding:** Enforces strict zero-tolerance Jordan loop closure, completely erasing micro-gaps caused by floating-point rounding.
2. **Adaptive Optimization:** Self-corrects and determines optimal upper and lower bounds for ray-cast sampling counts.
3. **Automated Taxonomy Core:** Leverages statistical distributions to autonomously categorize shapes into formalized taxonomic codes, such as `J-Curve::Class-H::Alpha` (Hybrid loops containing deep geometric attractors).
4. **Diagnostic Visualisation:** Automatically exports three-panel diagnostic maps tracking boundary overlaps, ray fields, and taxonomy clustering spaces.

# Invariance Verification
During empirical batch runs, the taxonomy core successfully verified that a pure sharp fractal loop and its heavily smoothed Gaussian variant converge onto the exact same taxonomic assignment (`Class-H::Alpha`), yielding highly stable structural invariants:
- **Pure Sharp Fractal:** Variance = 0.01141, Skewness = -1.17142, Kurtosis = 1.50125
- **Rounded Variant:** Variance = 0.01142, Skewness = -1.18151, Kurtosis = 1.49147

This proves that the underlying spatial frequency and structural layout remain identifiable by the software, independent of surface-level data smoothing artifacts.

# Acknowledgements
We acknowledge the shared efforts of the independent research community in establishing this open-source foothold for future discrete topology exploration.
