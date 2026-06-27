# chain_test.py - Naive vs Lazy φ_n comparison
import time
from deval import PVA
import sys
import matplotlib.pyplot as plt

sys.set_int_max_str_digits(20000)

class NaivePVA:
    """No reduction, just appends forever. For comparison only."""
    def __init__(self, prime, exp=1):
        self.tuple = [(prime, exp)]

    def __mul__(self, other):
        new = NaivePVA(2, 0)
        new.tuple = self.tuple + other.tuple # No reduce ever
        return new

    def __len__(self):
        return len(self.tuple)

def chain_test(ops=5000, p=7, q=19, label="run", use_lazy=True):
    PVAClass = PVA if use_lazy else NaivePVA
    a = PVAClass(p, 1)
    b = PVAClass(q, 1)

    start = time.perf_counter()
    lengths = []
    timestamps = []

    for i in range(ops):
        a = a * b
        if i % 50 == 0:
            lengths.append(len(a))
            timestamps.append(i)

    elapsed = time.perf_counter() - start

    return {
        "label": label,
        "ops": ops,
        "final_len": len(a),
        "lengths": lengths,
        "timestamps": timestamps,
        "time": elapsed,
        "us_per_op": elapsed/ops*1e6
    }

def bench_suite():
    """Run Lazy vs Naive side by side"""
    tests = [
        (5000, 7, 19, "Lazy φ_n - EAGER_THRESHOLD=50"),
        (5000, 7, 19, "Naive append - No reduction")
    ]

    results = []
    for ops, p, q, label in tests:
        use_lazy = "Lazy" in label
        print(f"\n=== {label} ===")
        try:
            res = chain_test(ops, p, q, label, use_lazy)
            print(f"Ops: {res['ops']}, Final length: {res['final_len']}")
            print(f"Time: {res['time']:.4f}s, {res['us_per_op']:.2f}µs/op")
            results.append(res)
        except MemoryError:
            print("💥 MemoryError: Naive version blew up")
            results.append({"label": label, "lengths": [0], "timestamps": [0]})

    plot_comparison(results)
    return results

def plot_comparison(results):
    """Knockout graph: Flat line vs Red spike"""
    plt.figure(figsize=(11, 6))

    for r in results:
        color = 'green' if 'Lazy' in r['label'] else 'red'
        lw = 3 if 'Lazy' in r['label'] else 2
        plt.plot(r['timestamps'], r['lengths'],
                 label=r['label'], color=color, linewidth=lw, marker='o', markersize=3)

    plt.axhline(y=50, color='gray', linestyle='--', alpha=0.4, label='EAGER_THRESHOLD=50')
    plt.xlabel('Operations', fontsize=12)
    plt.ylabel('Tuple Count / Memory Usage', fontsize=12)
    plt.title('Lazy φ_n vs Naive: Memory Scaling Comparison', fontsize=14, weight='bold')
    plt.legend(fontsize=10)
    plt.grid(alpha=0.3)
    plt.ylim(bottom=0)
    plt.tight_layout()
    plt.savefig('phi_knockout_demo.png', dpi=200)
    print("\n✅ Saved knockout graph: phi_knockout_demo.png")

if __name__ == "__main__":
    bench_suite()
