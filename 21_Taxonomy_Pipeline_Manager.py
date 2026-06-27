import numpy as np
import scipy.ndimage as ndimage
import scipy.stats as stats
import matplotlib.pyplot as plt
import os

# =============================================================================
# MODULE 1: THE GENERATION AND INTEGRITY LAYER
# =============================================================================
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
    Generates target boundaries and performs an upfront integrity check
    to prevent processing invalid topological loops.
    """
    # Define baseline smooth sides of the box bounding domain
    side1 = np.array([[0.0, y] for y in np.linspace(1.0, 0.0, 100, endpoint=False)])
    side2 = np.array([[x, 0.0] for x in np.linspace(0.0, 1.0, 100, endpoint=False)])
    side3 = np.array([[1.0, y] for y in np.linspace(0.0, 1.0, 100, endpoint=False)])
    box_base = np.vstack([side1, side2, side3])

    if curve_type == "hybrid":
        fractal_pts = np.array(initiate_koch_segment([1.0, 1.0], [0.0, 1.0], depth=depth))
        if smooth:
            fractal_pts[:, 0] = ndimage.gaussian_filter1d(fractal_pts[:, 0], sigma=sigma, mode='wrap')
            fractal_pts[:, 1] = ndimage.gaussian_filter1d(fractal_pts[:, 1], sigma=sigma, mode='wrap')
        curve = np.vstack([box_base, fractal_pts[:-1]])
    elif curve_type == "degenerate_open":
        # INTENTIONAL FAILURE UNIT: Creates an invalid non-closed loop to test alerts
        curve = np.vstack([box_base, np.array([[1.0, 1.0], [0.5, 1.2]])])
    else:
        raise ValueError("Unknown curve profile configuration.")

    # CRITICAL INTEGRITY CHECK: Verify Jordan Loop Closure Definition
    start, end = curve[0], curve[-1]
    is_closed = np.allclose(start, end) or np.linalg.norm(start - end) < 0.05

    if not is_closed:
        # Gracefully throw a custom exception rather than letting the code crash later
        raise ValueError(f"CRITICAL FAULT: Boundary fails Jordan Closure criteria. Distance delta: {np.linalg.norm(start - end):.4f}")

    return curve

# =============================================================================
# MODULE 2: THE MEASUREMENT LAYER (STRAWS)
# =============================================================================
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

# =============================================================================
# MODULE 3: THE TAXONOMY AND VISUALIZATION ENGINE
# =============================================================================
def automate_pipeline(curve_id, curve_type, depth, smooth, sigma):
    """Executes the end-to-end automated processing engine for a target curve."""
    print(f"\n[Pipeline] Processing Job {curve_id} ({'Smooth ' if smooth else 'Sharp '}{curve_type})...")

    # Step 1: Securely Generate Curve with integrated error routing
    try:
        curve_matrix = build_curve_matrix(curve_type, depth, smooth, sigma)
    except Exception as error_msg:
        print(f" !!! ALERT [Job {curve_id}]: Processing Aborted.")
        print(f"     Diagnostic: {error_msg}")
        print(f"     Action: Bypassing queue item. Returning framework focus to Step 17/18 integrity controls.")
        return False # Queue preserved, pipeline unaffected

    # Step 2: Measure Straw footprint signatures
    lengths = cast_straws(curve_matrix, num_straws=1440)
    variance = np.var(lengths)
    skewness = stats.skew(lengths)
    kurtosis = stats.kurtosis(lengths)

    # Step 3: Classify Automatically via Taxonomy Decision Core
    if kurtosis > 1.2 and abs(skewness) > 0.8:
        tax_id = "J-Curve::Class-H::Alpha"
    else:
        tax_id = "J-Curve::Class-P::Beta"

    print(f" -> SUCCESS: Assigned ID: {tax_id}")
    print(f"    Metrics: Var={variance:.5f} | Skew={skewness:.5f} | Kurt={kurtosis:.5f}")

    # Step 4: Output Human-Comprehensible Visual Artifacts
    plt.figure(figsize=(5, 5), dpi=100)
    plt.plot(curve_matrix[:, 0], curve_matrix[:, 1], color='purple', lw=1.5)
    plt.scatter(0.5, 0.5, color='black', zorder=5)
    plt.title(f"Job {curve_id}: {tax_id}", fontsize=9, fontweight='bold')
    plt.xlim(-0.1, 1.1)
    plt.ylim(-0.1, 1.4)
    plt.grid(True, linestyle=':', alpha=0.5)

    img_name = f"21_output_job_{curve_id}.png"
    plt.savefig(img_name, bbox_inches='tight')
    plt.close()
    print(f" -> ASSET EXPORTED: Visualized layout saved as '{img_name}'.")
    return True

# =============================================================================
# PIPELINE EXECUTION QUEUE MANAGER
# =============================================================================
if __name__ == "__main__":
    print("========================================================")
    print("     INITIALIZING AUTOMATED TOPOLOGICAL FACTORY CORE     ")
    print("========================================================")

    # Setup our batch queue processing environment
    job_queue = [
        {"id": "001_PureSharp", "type": "hybrid", "depth": 4, "smooth": False, "sigma": 0.0},
        {"id": "002_SmoothVar", "type": "hybrid", "depth": 4, "smooth": True, "sigma": 4.0},
        {"id": "003_FaultTest", "type": "degenerate_open", "depth": 2, "smooth": False, "sigma": 0.0}, # Fault Injection
        {"id": "004_ValidFinal", "type": "hybrid", "depth": 3, "smooth": True, "sigma": 2.0}
    ]

    success_count = 0
    for job in job_queue:
        status = automate_pipeline(
            curve_id=job["id"],
            curve_type=job["type"],
            depth=job["depth"],
            smooth=job["smooth"],
            sigma=job["sigma"]
        )
        if status: success_count += 1
        print("-" * 56)

    print(f"\n[Pipeline Summary] Queue processing concluded. {success_count}/{len(job_queue)} jobs successfully indexed into the Taxonomy.")
