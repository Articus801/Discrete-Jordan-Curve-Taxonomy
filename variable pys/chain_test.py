# chain_test.py - Lazy phi memory blowup test
import time
from deval import PVA  # adjust import to your module

def chain_test(ops=1000, p=2, q=3):
    a = PVA(p, 1)  # phi_2^1
    b = PVA(q, 1)  # phi_3^1

    start = time.perf_counter()
    lengths = []

    for i in range(ops):
        a = a * b  # no final phi_n, stays lazy
        if i % 100 == 0:
            lengths.append(len(a.tuple))  # adjust to your internal field name

    elapsed = time.perf_counter() - start
    print(f"Ops: {ops}, Final tuple length: {len(a.tuple)}")
    print(f"Length growth: {lengths}")
    print(f"Time: {elapsed:.4f}s, Time/op: {elapsed/ops*1e6:.2f}µs")

    # Test eager reduction threshold
    if len(a.tuple) > 50:
        print("Warning: Tuple > 50 primes. Add eager_threshold logic.")

    return a

if __name__ == "__main__":
    a = chain_test(ops=1000)
    print("Final:", a.tuple)
