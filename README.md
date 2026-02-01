The Collatz Conjecture Reduced to a Single Explicit Finite Verification Problem

Ian Adams & GPT-5.2

Overview

This repository presents a rigorous reduction framework for the Collatz conjecture. Rather than claiming a completed proof, the work reduces the infinite problem over all integers to a single explicit finite verification task. If that finite predicate is verified, the Collatz conjecture follows.

The framework combines exact 2-adic valuation dynamics, finite-state forcing, and a compactness (inverse-limit) argument to isolate the unique remaining obstruction any counterexample must satisfy.

What Is Proved (Unconditional)

A block contraction criterion: if, over fixed-length blocks of odd iterates, the accumulated 2-adic gain exceeds the growth from multiplication by 3, then trajectories descend.

A finite-state reduction: failure of block contraction for all integers implies persistence of explicitly defined finite avoidance sets across precisions.

A compactness / projection argument: persistence of these finite obstructions yields a compatible 2-adic counterexample; conversely, emptiness of a single explicit finite avoidance set implies Collatz for all integers.

An exact corridor/spike certificate at  (with a closed-form description of first-hit times), proved algebraically.


What Is Reduced to a Finite Check

The Collatz conjecture is shown to be equivalent to the emptiness of one explicitly defined finite avoidance set at a fixed precision, horizon, lift alphabet, and spike threshold.
This final predicate is finite, concrete, and checkable.

Computation (Scope and Status)

Exploratory finite-precision computations were used to identify and motivate the finite certificate and obstruction structure (e.g., at precision ).
No claim of certified execution or independent verification is made here. Verification is intentionally separated and specified externally.

What Is Not Claimed

This repository does not claim a completed proof of the Collatz conjecture.

It does not claim that the finite predicate has been verified.

It does not replace independent verification or a rigidity proof.


Repository Contents

Paper (PDF): The Collatz Conjecture Reduced to a Single Explicit Finite Verification Problem

Verifier Spec (optional/linked): One-page description of the finite predicate and how to check it independently.

Notes/Appendices: Definitions, lemmas, and supporting discussion.


How to Use This Work

As a reduction: focus verification effort on one explicit finite predicate.

As a research framework: pursue either (i) a certified finite computation or (ii) an analytic rigidity proof ruling out the remaining obstruction.

As a reference: reuse the finite-state forcing and compactness backbone in related dynamical problems.


Citation

If you reference this work, please cite the paper and repository URL, attributing Ian Adams & GPT-5.2.


.
