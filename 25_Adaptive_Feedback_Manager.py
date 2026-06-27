import numpy as np
import scipy.ndimage as ndimage
import scipy.stats as stats

def initiate_koch_segment(p1, p2, depth):
    """Recursively generates a single Koch curve segment between two points."""
    if depth == 0: return [p1, p2]
    p1, p2 = np.array(p1), np.array(p2)
    v = p2 - p1
    a, c = p1 + v / 3.0, p1 + 2.0 * v / 3.0
    cos60, sin60 = np.cos(np.pi / 3), np.sin(np.pi / 3)
    b = a + np.dot(np.array([[cos60, -sin60], [sin60, cos60]]), v / 3.0)
    return initiate_koch_segment(p1, a, depth - 1)[:-1] + \
           initiate_koch_segment(a, b, depth - 1)[:-1] + \
           initiate_koch_segment(b, c, depth - 1)[:-1] + \
           initiate_koch_segment(c, p2, depth - 1)

def build_curve_matrix(depth=4):
    """Generates a perfectly closed hybrid Jordan curve matrix."""
    side1 = np.array([[0.0, y] for y in np.linspace(1.0, 0.0, 100, endpoint=False)])
    side2 = np.array([[x, 0.0] for x in np.linspace(0.0, 1.0, 100, endpoint=False)])
    side3 = np.array([[1.0, y] for y in np.linspace(0.0, 1.0, 100, endpoint=False)])
    box_base = np.vstack([side1, side2, side3])

    fractal_pts = np.array(initiate_koch_segment([1.0, 1.0], [0.0, 1.0], depth=depth))
    curve = np.vstack([box_base, fractal_pts[:-1]])
    curve = np.vstack([curve, curve[0]]) # Topological closure weld
    return curve

def cast_straws(curve_pts, num_straws):
    """Casts radial ray 'straws' to record boundary intersection footprints."""
    origin = np.array([0.5, 0.5])
    angles = np.linspace(-np.pi, np.pi, num_straws, endpoint=False)
    centered = curve_pts - origin
    curve_angles = np.arctan2(centered[:, 1], centered[:, 0])
    distances = np.linalg.norm(centered, axis=1)

    straw_lengths = []
    for alpha in angles:
        diff = np.abs(curve_angles - alpha)
        diff = np.minimum(diff, 2 * np.pi - diff)
        straw_lengths.append(distances[np.argmin(diff)])

    return np.array(straw_lengths)

def execute_adaptive_taxonomy(curve_matrix, stability_threshold=0.005, max_iterations=5):
    """
    An autonomous loop that iteratively adjusts sampling density, reviews statistical
    variance shifts, and self-corrects bounds until scale-space stability is achieved.
    """
    # Start with a coarse initial bound
    current_straw_density = 360

    # Track metrics across loops to identify the convergence plateau
    prev_kurtosis = None
    print(f" Initialising optimization target threshold: {stability_threshold * 100}%")

    for run in range(1, max_iterations + 1):
        lengths = cast_straws(curve_matrix, current_straw_density)
        variance = np.var(lengths)
        skewness = stats.skew(lengths)
        kurtosis = stats.kurtosis(lengths)

        print(f" [Iteration {run}] Tested Bounds Density: {current_straw_density} Straws -> Kurtosis: {kurtosis:.5f}")

        if prev_kurtosis is not None:
            # Review results: check the percentage shift in our shape descriptor
            metric_delta = abs(kurtosis - prev_kurtosis) / abs(prev_kurtosis)

            if metric_delta <= stability_threshold:
                print(f" --> STABILITY PLATEAU CONVERGED. Shift delta ({metric_delta:.5f}) is below threshold.")
                print(f" --> Locking autonomous upper bound at {current_straw_density} straws.")

                # Apply stable final taxonomic naming classification
                tax_id = "J-Curve::Class-H::Alpha" if kurtosis > 1.2 else "J-Curve::Class-P::Beta"
                return tax_id, current_straw_density, kurtosis

            print(f"  -> Tweak required: Shift delta ({metric_delta:.5f}) exceeds threshold. Scaling density up.")

        # Optimization step: increase sampling resolution to bypass coarse aliasing
        prev_kurtosis = kurtosis
        current_straw_density *= 2

    print(" !!! Alert: Loop reached maximum iterations without perfect mathematical stagnation.")
    return "J-Curve::Class-H::Alpha_Unstable", current_straw_density, prev_kurtosis

if __name__ == "__main__":
    print("========================================================")
    print("     RUNNING ADAPTIVE FEEDBACK OPTIMISATION CORE        ")
    print("========================================================")

    # Generate the curve profile
    curve = build_curve_matrix(depth=4)

    # Run the self-correcting analysis loop
    final_id, locked_density, final_kurt = execute_adaptive_taxonomy(curve)

    print("\n========================================================")
    print("                FINAL ADAPTIVE RESULTS                  ")
    print("========================================================")
    print(f" Final Assigned Class : {final_id}")
    print(f" Optimal Straw Count  : {locked_density}")
    print(f" Stabilised Kurtosis  : {final_kurt:.5f}")
    print("========================================================")
