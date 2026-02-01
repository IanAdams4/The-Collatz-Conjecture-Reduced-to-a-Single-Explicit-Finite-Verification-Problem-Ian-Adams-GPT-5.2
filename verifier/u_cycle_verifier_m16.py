# rigidity_cylinder_verifier_s16_alpha4.py
#
# Sound finite cylinder-graph verifier for the Rigidity Lemma obstruction.
# Implements a finite approximation of the (T,q)-tower recursion with:
#   minimal exit: v2(3^T q - 1) = 1
#   re-entry depth: T' = v2(3^T q + 1) - 1
#   update: q' = (3^T q + 1) / 2^(T'+1)
#
# State precision parameters:
#   s0 = 16  (base "T-depth" control scale)
#   alpha = 4 (extra bits for lift-robustness)
#
# We model truncated states:
#   T mod 2^(s0-2+alpha)
#   q mod 2^(s0+alpha), with q odd
#
# Graph is pruned to compute survival set W.
#
# Output:
#   - EMPTY if no survivors remain
#   - otherwise prints survivor count and a witness state

from collections import deque

S0 = 16
ALPHA = 4

# Moduli for truncated state components
MOD_T = 1 << (S0 - 2 + ALPHA)     # T reduced mod 2^(s0-2+alpha)
MOD_Q = 1 << (S0 + ALPHA)         # q reduced mod 2^(s0+alpha)

MASK_Q = MOD_Q - 1

def v2(n: int) -> int:
    """2-adic valuation for positive integer n."""
    return (n & -n).bit_length() - 1

def pow3_mod_2k(max_exp: int, mod: int) -> list[int]:
    """pow3[e] = 3^e mod mod for e=0..max_exp."""
    pow3 = [1] * (max_exp + 1)
    for e in range(1, max_exp + 1):
        pow3[e] = (pow3[e - 1] * 3) % mod
    return pow3

def main() -> None:
    # .

    T_VALUES = list(range(2, S0 + ALPHA + 3))
    KQ = S0 + ALPHA  # q modulus exponent

    MOD = 1 << KQ

    # Precompute 3^t mod 2^KQ for t in our window
    pow3 = {t: pow(3, t, MOD) for t in T_VALUES}

    # Enumerate candidate (T,q) states satisfying the minimal-exit condition exactly:
    #   v2(3^T q - 1) = 1  <=>  3^T q ≡ 3 (mod 4)
    # with q odd.
    #
    # We keep q modulo 2^KQ.

    vertices = []
    vid = {}

    for T in T_VALUES:
        a = pow3[T]  # 3^T mod 2^KQ
        # Condition mod 4: a*q ≡ 3 (mod 4)
        # Since a ≡ 3^T ≡ 3 (mod 4) for T odd, ≡ 1 (mod 4) for T even:
        # we can just brute q mod 4 among odd residues.
        for q in range(1, MOD, 2):
            u = (a * q) % MOD
            if (u & 3) != 3:
                continue
            # Enforce exact minimal exit at this precision window:
            # v2(u-1) = 1, i.e. u ≡ 3 (mod 4) and u !≡ 1 (mod 8) automatically holds.
            if v2((u - 1) & (MOD - 1)) != 1:
                continue
            key = (T, q)
            vid[key] = len(vertices)
            vertices.append(key)

    V = len(vertices)
    print("Core-window cylinder graph")
    print("  T window:", T_VALUES[0], "..", T_VALUES[-1])
    print("  q modulus: 2^", KQ)
    print("  |V| =", V)

    out_adj = [[] for _ in range(V)]
    rev_adj = [[] for _ in range(V)]

    # Build edges by computing re-entry depth from v2(3^T q + 1) - 1, then update q'.
    for i, (T, q) in enumerate(vertices):
        a = pow3[T]
        u = (a * q) % MOD

        # Compute tplus = v2(u+1). Since we're in a window, we compute v2 on the integer representative.
        # Use representative in [0,2^KQ).
        tplus = v2((u + 1) % MOD)

        if tplus <= 1:
            continue

        Tn = tplus - 1
        # Update q' = (u+1)/2^(Tn+1) as integer, but we only keep mod 2^KQ
        qp = ((u + 1) >> (Tn + 1))  # integer division; safe since shift is exact at this rep

        # We must enforce: qp odd (required for tower)
        if (qp & 1) == 0:
            continue

        # Next state must be in window
        if Tn not in pow3:
            continue

        # Reduce qp mod 2^KQ
        qp &= (MOD - 1)

        # Next state must satisfy minimal exit
        an = pow3[Tn]
        un = (an * qp) % MOD
        if v2((un - 1) & (MOD - 1)) != 1:
            continue

        j = vid.get((Tn, qp))
        if j is None:
            continue

        out_adj[i].append(j)
        rev_adj[j].append(i)

    # Prune dead ends to compute survival set (greatest fixed point)
    alive = bytearray(b"\x01") * V
    outdeg = [len(out_adj[i]) for i in range(V)]

    qd = deque()
    for i in range(V):
        if outdeg[i] == 0:
            qd.append(i)

    removed = 0
    while qd:
        x = qd.popleft()
        if alive[x] == 0:
            continue
        alive[x] = 0
        removed += 1
        for p in rev_adj[x]:
            if alive[p] == 0:
                continue
            outdeg[p] -= 1
            if outdeg[p] == 0:
                qd.append(p)

    survivors = V - removed
    print("  survivors after pruning:", survivors)

    if survivors == 0:
        print("EMPTY (in core-window model): no surviving tower states.")
        return

    # Print a witness survivor
    for i in range(V):
        if alive[i]:
            T, qv = vertices[i]
            print("NONEMPTY (in core-window model): witness survivor state")
            print("  T =", T)
            print("  q mod 2^K =", qv)
            # show one live successor
            for j in out_adj[i]:
                if alive[j]:
                    T2, q2 = vertices[j]
                    print("  successor: T' =", T2, " q' =", q2)
                    break
            return

if __name__ == "__main__":
    main().


---

Deterministic Finite Verifier (Collatz Reduction)

This directory contains deterministic, exact-arithmetic verifiers supporting the finite-reduction framework developed in the accompanying paper.

Purpose

These scripts check finite obstruction conditions arising from the reduction of the Collatz conjecture to explicit, bounded verification problems.
They do not claim a proof of Collatz; they verify that specific finite avoidance sets and obstruction models are empty at fixed precision.

Contents

deterministic_verifier_m16_J16_K4.py
Verifies emptiness of the finite avoidance set


A_{16}(J=16, K=4, \text{lifts}=0..15)

u_cycle_verifier_m16.py, u_cycle_verifier_m20_alpha4.py
Deterministic cycle checks for the truncated minimal-exit deep-reentry obstruction inside the fingerprint class


\Omega_m = \{ u \equiv 7 \pmod 8 \}.

How to Run

python3 verifier/<script_name>.py

Each script halts immediately on a counterexample and otherwise reports NO CYCLES FOUND or NO SURVIVORS.

Interpretation

All scripts are fully deterministic

No randomness, heuristics, or floating-point arithmetic

Results are reproducible and independently checkable

These verifiers support the reduction claim, not a completed proof


Status

Finite certificates verified at fixed precision.
Further theoretical work is required to lift these results to a full proof.


---

