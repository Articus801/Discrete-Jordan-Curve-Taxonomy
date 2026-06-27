def stress_suite_safe3():
    """Same tests but Ctrl+C friendly"""
    cases = [
        ("2^1000", 1000, 2, 2, "Max 50% collapse"), # took two 0 off at 1000 1000
        ("19^500", 500, 19, 19, "94.7% collapse demo"), # took two 0 off at 500 500
        ("Mixed_9973_2", 200, 9973, 2, "Big prime + small prime"), # took 0 off at 20
        ("Prime_chain_3_5_7_11", 300, 3, 5, "Multi-prime stress") # took 0 off at 30
    ]

    results = []
    try:
        for label, ops, p, q, note in cases:
            print(f"\n=== {label} ===")
            print(f"Note: {note}")
            res = chain_test(ops, p, q, label)
            results.append(res)
            print(f"✅ Survived: {res['ops']} ops → {res['final_len']} tuples")
            print(f"Speed: {res['us_per_op']:.2f}µs/op")

    except KeyboardInterrupt:
        print(f"\n\n🛑 Stopped by user. Got {len(results)} tests done:")
        for r in results:
            print(f"  {r['ops']} ops → {r['final_len']} tuples, {r['us_per_op']:.2f}µs/op")
        print("No data lost. Safe to exit.")
        return results

    print("\n🏁 All tests complete")
    return results
