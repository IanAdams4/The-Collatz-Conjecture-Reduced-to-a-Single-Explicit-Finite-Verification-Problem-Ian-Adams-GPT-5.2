#!/usr/bin/env python3
"""
verify_gate_cycle_m16.py

Directly verifies the rigidity certificate:

  "No directed cycle in (V_m, F_m) intersects the gate I_m"

for m = 16, where:

  V_m = { (r, ell) : r odd mod 2^m, ell in {0..15} }
  x(r,ell) = r + ell*2^m
  U(x) = (3x+1)/2^{v2(3x+1)}  (odd Collatz map)
  F_m(r,ell) = successor lift-state determined by U(x) reduced mod 2^{m+4}

Gate:
  I_m = { (2^m - 1, ell) with ell odd }
equivalently x ≡ -1 (mod 2^{m+1}).

Method:
- For each gate state, compute the eventual cycle via Floyd's algorithm.
- Fail if the eventual cycle contains any gate state.
- Pass otherwise.

Options:
  --hash-script   prints SHA256 of this script file
  --save-output   writes stdout to a file and prints its SHA256
  --quiet         less verbose

No external dependencies.
"""

from __future__ import annotations
import argparse
import hashlib
import os
import sys
from typing import List, Optional, Tuple


def v2(n: int) -> int:
    """2-adic valuation of n for n>0."""
    return (n & -n).bit_length() - 1


def step_F(r: int, ell: int, m: int = 16) -> Tuple[int, int]:
    """
    One lift-state update F_m on V_m.

    Start with x = r + ell*2^m (odd).
    Compute x_next = U(x) = (3x+1)/2^{v2(3x+1)}.

