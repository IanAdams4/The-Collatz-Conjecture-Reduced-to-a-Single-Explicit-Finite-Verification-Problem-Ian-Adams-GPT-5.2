
"""
verify_A16.py

Verifies the finite-certificate predicate for the Collatz reduction at base resolution m0=16:

A_16 := { r odd mod 2^16 : for all lifts ell in {0..15}, for all j in {0..15},
                          v2(3*x_j + 1) <= 3 },
where x_0 = r + ell*2^16 and x_{j+1} = U(x_j) = (3*x_j+1)/2^{v2(3*x_j+1)} (odd Collatz map).

Certificate goal: A_16 is empty (no residue r survives all lifts and 16 steps without a spike >=4).

This script:
- exhaustively checks all 32,768 odd residues r mod 2^16,
- finds a witness (ell, j, b) with b=v2(3*x_j+1) >= 4 for each r (if possible),
- reports whether A_16 is empty,
- optionally produces a SHA256 hash of the witness stream for reproducibility,
- optionally prints a sample of witnesses.

No external dependencies.
"""

from __future__ import annotations
import argparse
import hashlib
import struct
import sys
from typing import Optional, Tuple, List


def v2(n: int) -> int:
    """2-adic valuation of n for n>0."""
    # n & -n isolates lowest set bit; bit_length-1 gives index.
    return (n & -n).bit_length() - 1


def odd_collatz_step(x: int) -> Tuple[int, int]:
    """
    One step of the odd Collatz map U on odd x.
    Returns (x_next, b) where b=v2(3x+1).
    """
    t = 3 * x + 1
    b = v2(t)
    return (t >> b), b


def find_witness_for_r(
    r: int,
    m0: int = 16,
    J: int = 16,
    K: int = 4
) -> Optional[Tuple[int, int, int]]:
    """
    Try to find (ell, j, b) such that starting from x0=r+ell*2^m0,
    within j in [0..J-1], we get b=v2(3*x_j+1) >= K.

    Returns first witness found in lexicographic search order:
      ell=0..15, then j=0..J-1
    or None if no witness exists (meaning r would be in A_16).
    """
    base = 1 << m0
    for ell in range(16):
        x = r + (ell << m0)
        for j in range(J):
            _, b = odd_collatz_step(x)  # b for current x
            if b >= K:
                return (ell, j, b)
            x, _ = odd_collatz_step(x)  # advance
    return None


def main() -> int:
    ap = argparse.ArgumentParser(description="Verify A_16 emptiness for Collatz finite certificate.")
    ap.add_argument("--m0", type=int, default=16, help="Base resolution m0 (default 16).")
    ap.add_argument("--J", type=int, default=16, help="Horizon J (default 16).")
    ap.add_argument("--K", type=int, default=4, help="Spike threshold K (default 4, i.e. b>=4).")
    ap.add_argument("--hash", action="store_true", help="Compute SHA256 of witness stream.")
    ap.add_argument("--print-sample", type=int, default=0, help="Print first N witnesses.")
    ap.add_argument("--print-survivors", action="store_true", help="Print any survivors (should be none if A_16 empty).")
    args = ap.parse_args()

    m0, J, K = args.m0, args.J, args.K
    MOD = 1 << m0

    # Hash witness stream in canonical order over odd residues.
    h = hashlib.sha256() if args.hash else None

    survivors: List[int] = []
    sample_left = args.print_sample

    checked = 0
    witnesses_found = 0

    for r in range(1, MOD, 2):  # all odd residues mod 2^m0
        checked += 1
        w = find_witness_for_r(r, m0=m0, J=J, K=K)
        if w is None:
            survivors.append(r)
            if args.print_survivors:
                print(f"SURVIVOR r={r}")
        else:
            ell, j, b = w
            witnesses_found += 1

            # Update digest with canonical packing: (r, ell, j, b)
            if h is not None:
                # r fits in uint16 for m0=16; ell,j,b in uint8.
                h.update(struct.pack("<HBBB", r, ell, j, b))

            # Print sample witnesses if requested
            if sample_left > 0:
                print(f"r={r:5d} -> (ell={ell:2d}, j={j:2d}, b={b:2d})")
                sample_left -= 1

    print("\n=== Summary ===")
    print(f"m0={m0}, J={J}, K={K}")
    print(f"Odd residues checked: {checked}")
    print(f"Witnesses found:     {witnesses_found}")
    print(f"Survivors (A_m0):    {len(survivors)}")

    if len(survivors) == 0:
        print("RESULT: A_m0 is EMPTY (finite certificate condition holds).")
    else:
        print("RESULT: A_m0 is NONEMPTY (certificate fails).")
        if not args.print_survivors:
            print("Tip: rerun with --print-survivors to list survivors.")

    if h is not None:
        print(f"SHA256(witness-stream) = {h.hexdigest()}")

    return 0 if len(survivors) == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
