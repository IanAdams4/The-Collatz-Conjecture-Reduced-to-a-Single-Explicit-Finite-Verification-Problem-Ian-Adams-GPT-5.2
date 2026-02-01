# Deterministic verifier for the finite certificate lemma at:
# (m0, J, K, lifts) = (16, 16, 4, {0..15})
#
# This script makes no probabilistic choices and uses only exact integer arithmetic.
# It halts immediately if it finds any surviving residue.

M_BITS = 16
M = 1 << M_BITS
J = 16
K = 4
LIFTS = range(16)


def v2(n: int) -> int:
    """2-adic valuation v2(n) for positive integer n."""
    # n & -n isolates the lowest set bit; its index is v2(n).
    return (n & -n).bit_length() - 1


def odd_collatz_step(x: int) -> tuple[int, int]:
    """Return (next_odd, b) where b=v2(3x+1) and next_odd=(3x+1)/2^b."""
    t = 3 * x + 1
    b = v2(t)
    return (t >> b), b


def main() -> None:
    total_residues = M // 2
    checked = 0

    # Track diagnostics (optional but useful)
    max_best_j = -1
    hardest = None  # (r, ell, j, b)

    for r in range(1, M, 2):
        checked += 1
        best = None  # (j, ell, b)

        for ell in LIFTS:
            x = r + (ell << M_BITS)

            for j in range(J):
                x_next, b = odd_collatz_step(x)

                if b >= K:
                    candidate = (j, ell, b)
                    if best is None or candidate[0] < best[0]:
                        best = candidate
                    break

                x = x_next

            # Early exit if we already found a spike at j=0
            if best is not None and best[0] == 0:
                break

        if best is None:
            print("FAILURE: survivor residue r =", r)
            print("Meaning: for this residue, no lift in 0..15 hits b>=4 within 16 odd steps.")
            return

        # Update hardest case stats
        if best[0] > max_best_j:
            max_best_j = best[0]
            hardest = (r, best[1], best[0], best[2])

        # Optional progress indicator (comment out if undesired)
        # if checked % 4096 == 0:
        #     print(f"Progress: {checked}/{total_residues} residues checked...")

    print("SUCCESS: No survivors. A_16 is empty for (J=16, K=4, lifts=0..15).")
    print("Worst best-hit time (max over r of min over lifts hit-time):", max_best_j)
    print("Hardest case (r, ell, j, b):", hardest)


if __name__ == "__main__":
    main()
