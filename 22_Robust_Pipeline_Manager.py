import numpy as np
import scipy.ndimage as ndimage
import scipy.stats as stats
import matplotlib.pyplot as plt

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

def build_curve_matrix(curve_type="hybrid", depth=4, smooth=False, sigma=4.0):
    """
    Generates target boundaries and applies a rigid Boundary Anchor Boundary
    Condition to guarantee absolute closure of the Jordan manifold.
    """
    # 1. Standard Euclidean box segments (100 discrete coordinates per side)
    side1 = np.array([[0.0, y] for y in np.linspace(1.0, 0.0, 100, endpoint=False)])
    side2 = np.array([[x, 0.0] for x in np.linspace(0.0, 1.0, 100, endpoint=False)])
    side3 = np.array([[1.0, y] for y in np.linspace(0.0, 1.0, 100, endpoint=False)])
    box_base = np.vstack([side1, side2, side3])

    if curve_type == "hybrid":
        fractal_pts = np.array(initiate_koch_segment([1.0, 1.0], [0.0, 1.0], depth=depth))

        if smooth and len(fractal_pts) > 4:
            # ROBUST ANCHOR MECHANIC: Preserve the original exact connection endpoints
            anchor_start = np.copy(fractal_pts[0])
            anchor_end = np.copy(fractal_pts[-1])

            # Apply Gaussian smoothing to internal coordinates only
            smoothed = np.copy(fractal_pts)
            smoothed[:, 0] = ndimage.gaussian_filter1d(fractal_pts[:, 0], sigma=sigma, mode='nearest')
            smoothed[:, 1] = ndimage.gaussian_filter1d(fractal_pts[:, 1], sigma=sigma, mode='nearest')

            # Snap endpoints back to their geometric home to prevent any spatial gaps
            smoothed[0] = anchor_start
            smoothed[-1] = anchor_end
            curve = np.vstack([box_base, smoothed[:-1]])
        else:
            curve = np.vstack([box_base, fractal_pts[:-1]])

    elif curve_type == "degenerate_open":
        # Controlled failure vector to verify alert routing remains operational
        curve = np.vstack([box_base, np.array([[1.0, 1.0], [0.5, 1.2]])])
    else:
        raise ValueError("Unknown curve profile configuration.")

    # Strict Jordan Closure Test
    start_pt, end_pt = curve[0], curve[-1]
    is_closed = np.allclose(start_pt, end_pt) or np.linalg.norm(start_pt - end_pt) < 0.01

    if not is_closed:
        raise ValueError(f"CRITICAL FAULT: Boundary fails closure criteria. Delta: {np.linalg.norm(start_pt - end_pt):.4f}")

    return curve

def cast_straws(curve_pts, origin=np.array([0.5, 0.5]), num_straws=1000):
    """Casts radial ray 'straws' to record boundary intersection footprints."""
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

def automate_pipeline(curve_id, curve_type, depth, smooth, sigma):
    """Executes the end-to-end automated processing engine for a target curve."""
    print(f"\n[Pipeline] Processing Job {curve_id} ({'Smooth ' if smooth else 'Sharp '}{curve_type})...")

    try:
        curve_matrix = build_curve_matrix(curve_type, depth, smooth, sigma)
    except Exception as error_msg:
        print(f" !!! ALERT [Job {curve_id}]: Processing Aborted.")
        print(f"     Diagnostic: {error_msg}")
        return False

    lengths = cast_straws(curve_matrix, num_straws=1440)
    variance = np.var(lengths)
    skewness = stats.skew(lengths)
    kurtosis = stats.kurtosis(lengths)

    # Classify Automatically via Taxonomy Core
    if kurtosis > 1.2 and abs(skewness) > 0.8:
        tax_id = "J-Curve::Class-H::Alpha"
    else:
        tax_id = "J-Curve::Class-P::Beta"

    print(f" -> SUCCESS: Assigned ID: {tax_id}")
    print(f"    Metrics: Var={variance:.5f} | Skew={skewness:.5f} | Kurt={kurtosis:.5f}")

    # Export layout visualization asset
    plt.figure(figsize=(5, 5), dpi=100)
    plt.plot(curve_matrix[:, 0], curve_matrix[:, 1], color='purple', lw=1.5)
    plt.scatter(0.5, 0.5, color='black', zorder=5)
    plt.title(f"Job {curve_id}: {tax_id}", fontsize=9, fontweight='bold')
    plt.xlim(-0.1, 1.1)
    plt.ylim(-0.1, 1.4)
    plt.grid(True, linestyle=':', alpha=0.5)

    img_name = f"22_output_job_{curve_id}.png"
    plt.savefig(img_name, bbox_inches='tight')
    plt.close()
    return True

if __name__ == "__main__":
    print("========================================================")
    print("     RUNNING ROBUST TOPOLOGICAL FACTORY CORE [VER 22]    ")
    print("========================================================")

    job_queue = [
        {"id": "001_PureSharp", "type": "hybrid", "depth": 4, "smooth": False, "sigma": 0.0},
        {"id": "002_SmoothVar", "type": "hybrid", "depth": 4, "smooth": True, "sigma": 4.0},
        {"id": "003_FaultTest", "type": "degenerate_open", "depth": 2, "smooth": False, "sigma": 0.0},
        {"id": "004_ValidFinal", "type": "hybrid", "depth": 3, "smooth": True, "sigma": 2.0}
    ]

    success_count = 0
    for job in job_queue:
        status = automate_pipeline(job["id"], job["type"], job["depth"], job["smooth"], job["sigma"])
        if status: success_count += 1
        print("-" * 56)

    print(f"\n[Pipeline Summary] Queue processing concluded. {success_count}/{len(job_queue)} jobs successfully indexed.")
