import matplotlib
# Use a non-interactive backend to guarantee the terminal never hangs/freezes
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import os

def generate_morphing_curve(n=400, alpha=0.0):
    """
    Generates a morphing Jordan curve.
    alpha = 0.0 -> Perfect Circle
    alpha = 1.0 -> Full Bumpy Bezier Loop
    """
    t = np.linspace(0, 2 * np.pi, n, endpoint=False)
    # Smoothly ramp up the bumps based on alpha
    r = 1.0 + alpha * (0.18 * np.sin(3 * t) + 0.08 * np.cos(5 * t))
    return np.column_stack((r * np.cos(t), r * np.sin(t)))

def compute_midpoint_variance(curve, test_center):
    midpoints = []
    for x in curve:
        ray = x - test_center
        target_direction = test_center - ray
        dists = np.linalg.norm(curve - target_direction, axis=1)
        y = curve[np.argmin(dists)]
        midpoints.append((x + y) / 2.0)
    midpoints = np.array(midpoints)
    return np.var(midpoints[:, 0]) + np.var(midpoints[:, 1]), midpoints

def hunt_squares_ccrt(curve, center, tol=0.04):
    """Maps chords through the optimized center and isolates unique squares."""
    chords = []
    for x in curve:
        ray = x - center
        target_direction = center - ray
        dists = np.linalg.norm(curve - target_direction, axis=1)
        y = curve[np.argmin(dists)]
        chords.append({'x': x, 'y': y, 'midpoint': (x + y) / 2.0, 'length': np.linalg.norm(x - y)})

    n = len(chords)
    found_squares = []
    for i in range(n):
        c1 = chords[i]
        v1 = c1['x'] - c1['y']
        for j in range(i + 1, n):
            c2 = chords[j]
            if np.linalg.norm(c1['midpoint'] - c2['midpoint']) > tol: continue
            if abs(c1['length'] - c2['length']) > tol: continue

            v2 = c2['x'] - c2['y']
            norm1, norm2 = np.linalg.norm(v1), np.linalg.norm(v2)
            if norm1 < 1e-6 or norm2 < 1e-6: continue
            if abs(np.dot(v1, v2) / (norm1 * norm2)) < 0.1:
                duplicate = False
                for sq in found_squares:
                    # Accessing chord1 using index [0] of the saved square tuple
                    if np.linalg.norm(sq[0]['midpoint'] - c1['midpoint']) < 0.06:
                        duplicate = True
                        break
                if not duplicate:
                    found_squares.append((c1, c2))
    return found_squares

if __name__ == "__main__":
    print("====================================================")
    print("      UNIFIED JORDAN CURVE DEFORMATION TOUR         ")
    print("====================================================\n")

    output_dir = "deformation_frames"
    os.makedirs(output_dir, exist_ok=True)

    # We will sample 5 milestone steps across the morphing landscape
    tour_steps = [0.0, 0.25, 0.50, 0.75, 1.0]
    current_center = np.array([0.0, 0.0]) # Start at origin

    print(f"Morphing sequences will be exported directly to: ./{output_dir}/\n")

    for idx, alpha in enumerate(tour_steps):
        print(f"Processing Tour Frame {idx+1}/{len(tour_steps)} | Morphing Level Alpha = {alpha:.2f}")

        # 1. Generate the morph state curve
        curve = generate_morphing_curve(n=400, alpha=alpha)

        # 2. Re-center autonomously using a quick local mini-gradient update
        h = 1e-4
        for _ in range(5): # Quick local tracking steps
            v, _ = compute_midpoint_variance(curve, current_center)
            v_dx, _ = compute_midpoint_variance(curve, current_center + np.array([h, 0.0]))
            v_dy, _ = compute_midpoint_variance(curve, current_center + np.array([0.0, h]))
            current_center -= 0.1 * np.array([(v_dx - v)/h, (v_dy - v)/h])

        # Get final visual midpoints for this frame
        _, midpoints = compute_midpoint_variance(curve, current_center)

        # 3. Dynamic Tolerance Scaling: Scale tolerances relative to curve distortion
        dynamic_tol = 0.03 + (0.02 * alpha)
        squares = hunt_squares_ccrt(curve, current_center, tol=dynamic_tol)

        # FIXED: Explicit array index notation handles the coordinates cleanly
        print(f" -> Active Center Locked: [{current_center[0]:.4f}, {current_center[1]:.4f}]")
        print(f" -> Dynamic Tolerance Filter: {dynamic_tol:.3f} | Inscribed Squares Tracked: {len(squares)}")

        # 4. Render Frame Output
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.plot(curve[:, 0], curve[:, 1], 'b-', lw=2.5, label=f'Curve State (Alpha={alpha:.2f})')
        ax.scatter(midpoints[:, 0], midpoints[:, 1], color='red', s=4, label='Midpoint Caustics')
        ax.scatter(current_center[0], current_center[1], color='black', marker='X', s=100, zorder=4, label='Tracked Center')

        # Overlay squares
        for sq_idx, sq in enumerate(squares):
            c1, c2 = sq
            pts = np.array([c1['x'], c2['x'], c1['y'], c2['y'], c1['x']])
            ax.plot(pts[:, 0], pts[:, 1], color='limegreen', lw=2.5, zorder=3,
                    label="Verified Inscribed Square" if sq_idx == 0 else "")

        ax.set_title(f"Deformation Evolution: Frame {idx+1}")
        ax.set_aspect('equal')
        ax.grid(True, linestyle=':', alpha=0.5)
        ax.set_xlim(-1.4, 1.4)
        ax.set_ylim(-1.4, 1.4)
        if idx == 0: ax.legend(loc='upper right')

        frame_filename = f"{output_dir}/frame_{idx+1}.png"
        plt.savefig(frame_filename, dpi=150)
        plt.close()
        print(f" -> Frame saved as: {frame_filename}\n")

    print("====================================================")
    print("TOUR COMPLETION SUCCESSFUL!")
    print(f"All frames have been compiled into the folder: ./{output_dir}/")
    print("====================================================")
