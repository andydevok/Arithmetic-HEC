# THE ARITHMETIC EVENT HORIZON v1.0
# =================================
# A Deterministic Probe for High-Rank Elliptic Curves via Dynamic Entropy
#
# Author: Andrés Sebastián Pirolo (2025)
# License: MIT
# Based on the "Dynamic-Arithmetic Rigidity Hypothesis"
#
# Usage:
#   python event_horizon.py
#
# Dependencies: numpy, numba, sympy

import numpy as np
import random
import time
import sys
from sympy import sieve
from numba import njit

# --- 1. THEORETICAL CONSTANTS ---
# Primes for BSD Proxy (Truncated L-function)
PRIMES_COUNT = 400  # p <= 2741
print(f"🌌 INITIALIZING PRIMALITY-ENTROPY ENGINE (P_max index: {PRIMES_COUNT})...")

# Pre-compute primes and log weights for O(1) lookups
PRIMES = np.array(list(sieve.primerange(2, 3000))[:PRIMES_COUNT], dtype=np.int64)
LOGS2 = np.log2(PRIMES)

# --- 2. JIT-COMPILED CORE (The Engine) ---
@njit(inline='always')
def power_mod(base, exp, mod):
    """Fast Modular Exponentiation for Legendre Symbols."""
    res = 1
    base %= mod
    while exp > 0:
        if exp % 2 == 1: res = (res * base) % mod
        base = (base * base) % mod
        exp >>= 1
    return res

@njit(fastmath=True)
def analyze_physics(a, b):
    """
    Computes the two fundamental signatures of the curve:
    1. Analytic Signature (BSD_Log2): The algebraic density.
    2. Dynamic Signature (Max_Glide): The entropic resistance.
    """
    bsd_score = 0.0
    max_glide = 0
    
    for i in range(PRIMES_COUNT):
        p = PRIMES[i]
        
        # A. Calculate Local Trace (ap) via Legendre Sum
        # This measures the "error" of the curve vs a flat line mod p
        ls_sum = 0
        for x in range(p):
            fx = (x*x*x + a*x + b) % p
            if fx == 0: 
                val = 0
            else:
                # Euler's Criterion for Legendre Symbol (val = f(x)^((p-1)/2) mod p)
                val = power_mod(fx, (p - 1) // 2, p)
                if val == p - 1: val = -1
            ls_sum += val
        
        ap = -ls_sum
        
        # B. Accumulate Analytic Signal (BSD Proxy)
        # Weighting by log2(p)/p highlights high-rank density
        bsd_score += (ap * LOGS2[i]) / p
        
        # C. Measure Dynamic Entropy (Collatz Glide)
        # Np = p + 1 - ap is the Local Group Order
        Np = p + 1 - ap
        steps = 0
        curr = Np
        
        # Run 3x+1 map until orbit collapses below start point (Glide)
        while curr > 1 and steps < 300:
            if curr % 2 == 0: 
                curr >>= 1
            else: 
                curr = 3 * curr + 1
            steps += 1
            if curr < Np: break # Glided
        
        if steps > max_glide: max_glide = steps

    return bsd_score, max_glide

# --- 3. INTERFACE MODES ---

def probe_manual():
    """Mode 1: Surgical Analysis of a Single Curve."""
    print("\n🔎 MANUAL PROBE INITIATED")
    print("   Enter Weierstrass coefficients for y^2 = x^3 + Ax + B")
    try:
        a = int(input("   Input A: "))
        b = int(input("   Input B: "))
    except ValueError:
        print("   ❌ Error: Integers only.")
        return

    print(f"\n   Processing physics for E: [{a}, {b}]...")
    start_t = time.time()
    score, glide = analyze_physics(a, b)
    dt = time.time() - start_t
    
    print(f"\n   📊 DIAGNOSTIC REPORT")
    print(f"   -------------------")
    print(f"   Analytic Signature (BSD):   {score:.4f}")
    print(f"   Dynamic Resistance (Glide): {glide}")
    print(f"   Compute Time:               {dt*1000:.2f} ms")
    
    # The Diamond Cut Classification (Eq 7 from Paper)
    if score < -25.0 and glide > 65:
        print(f"   🏆 CLASSIFICATION: HIGH RANK CANDIDATE (R >= 3)")
        print(f"      Use Magma/Sage to verify exact Rank.")
    elif score > -10.0:
        print(f"   ⚪ CLASSIFICATION: Low Rank (Likely 0 or 1)")
    else:
        print(f"   🟡 CLASSIFICATION: Indeterminate / Transitional Zone")

def mine_titans():
    """Mode 2: Deep Space Scanning for Records."""
    print("\n🚀 MINING STARTED. Searching for 'Titans' (BSD < -28.0)...")
    print("   Press Ctrl+C to stop.")
    attempts = 0
    start_total = time.time()
    
    try:
        while True:
            # Generate random curve in 10^12 range
            a = random.randint(-10**12, 10**12)
            b = random.randint(-10**12, 10**12)
            
            if 4*a**3 + 27*b**2 == 0: continue # Singular
            
            score, glide = analyze_physics(a, b)
            
            # "Titan" Threshold (Stricter than manual probe)
            if score < -28.0 and glide > 80:
                print(f"\n💎 TITAN DETECTED! (Iter {attempts})")
                print(f"   y^2 = x^3 + ({a})x + ({b})")
                print(f"   Analytic: {score:.4f} | Resistance: {glide}")
                print(f"   ------------------------------------------")
                # Save to file
                with open("titans_found.txt", "a") as f:
                    f.write(f"A={a}, B={b}, BSD={score:.4f}, Glide={glide}\n")
            
            attempts += 1
            if attempts % 10000 == 0:
                rate = attempts / (time.time() - start_total)
                sys.stdout.write(f"\r   Scanning... {attempts} curves | Rate: {rate:.0f} curves/sec")
                sys.stdout.flush()
                
    except KeyboardInterrupt:
        print("\n\n🛑 Mining halted by user.")

# --- 4. MAIN ENTRY POINT ---
if __name__ == "__main__":
    print("\nChoose Operation Mode:")
    print("1. 🔎 Probe a specific curve (Manual Entry)")
    print("2. 🚀 Mine for Titans (Random Search)")
    
    choice = input("\nSelect (1/2): ")
    
    if choice == "1":
        probe_manual()
    elif choice == "2":
        mine_titans()
    else:
        print("Invalid selection.")
