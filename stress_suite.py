def stress_suite():
    """Break it, or prove it unbreakable"""
    cases = [
        ("2^10000", 10000, 2, 2, "Max 50% collapse"),
        ("19^5000", 5000, 19, 19, "94.7% collapse demo"),
        ("Mixed_9973_2", 2000, 9973, 2, "Big prime + small prime"),
        ("Prime_chain_3_5_7_11", 3000, 3, 5, "Multi-prime stress")
    ]

    for label, ops, p, q, note in cases:
        print(f"\n=== {label} ===")
        print(f"Note: {note}")
        try:
            res = chain_test(ops, p, q, label)
            print(f"✅ Survived: {res['ops']} ops → {res['final_len']} tuples")
            print(f"Speed: {res['us_per_op']:.2f}µs/op")
        except Exception as e:
            print(f"💥 Died at: {e}")
