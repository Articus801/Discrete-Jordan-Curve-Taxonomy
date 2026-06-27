import matplotlib
# Use a non-interactive backend to guarantee the terminal never hangs/freezes
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

def generate_shifted_bumpy_bezier(n=400, shift_x=0.4, shift_y=-0.3):
    """
    Generates our bumpy shape family but intentionally throws it off-center
    by a massive spatial offset (shift_x, shift_y).
    """
    t = np.linspace(0, 2 * np.pi, n, endpoint=False)
    r = 1.0 + 0.18 * np.sin(3 * t) + 0.08 * np.cos(5 * t)
    x = r * np.cos(t) + shift_x
    y = r * np.sin(t) + shift_y
    return np.column_stack((x, y))

def compute_midpoint_variance(curve, test_center):
    """
    Executes the Central Chord Radial Transform relative to an arbitrary test_center
    and returns the total structural variance of the resulting midpoint cloud.
    """
    midpoints = []
    for x in curve:
        # Cast a ray from point x through our test_center
        ray = x - test_center
        target_direction = test_center - ray

        # Find where it strikes the opposite side of the loop
        dists = np.linalg.norm(curve - target_direction, axis=1)
        y = curve[np.argmin(dists)]

        midpoints.append((x + y) / 2.0)

    midpoints = np.array(midpoints)
    # Total structural variance is the sum of variances across X and Y axes
    return np.var(midpoints[:, 0]) + np.var(midpoints[:, 1])

def autonomous_center_hunt(curve, initial_guess, learning_rate=0.1, max_steps=50, tolerance=1e-5):
    """
    Uses numerical gradient descent to automatically crawl across the 2D plane,
    minimizing midpoint variance until it isolates the true geometric center.
    """
    center = np.array(initial_guess)
    history = [center.copy()]

    print(f"Starting autonomous hunt from initial guess: {center}")

    for step in range(1, max_steps + 1):
        current_var = compute_midpoint_variance(curve, center)

        # Numerical gradient estimation: nudge the center slightly along X and Y
        h = 1e-4
        var_dx = compute_midpoint_variance(curve, center + np.array([h, 0.0]))
        var_dy = compute_midpoint_variance(curve, center + np.array([0.0, h]))

        grad_x = (var_dx - current_var) / h
        grad_y = (var_dy - current_var) / h
        gradient = np.array([grad_x, grad_y])

        # Take a step opposite to the gradient direction (downhill into the potential well)
        center -= learning_rate * gradient
        history.append(center.copy())

        print(f"Step {step:02d} | Current Position: [{center[0]:.4f}, {center[1]:.4f}] | Midpoint Variance: {current_var:.6f}")

        # Stop early if the center barely moves (convergence criteria reached)
        if np.linalg.norm(gradient) < tolerance:
            print(f"-> Target isolated early due to gradient convergence at step {step}.")
            break

    return center, np.array(history)

if __name__ == "__main__":
    print("====================================================")
    print("      AUTONOMOUS JORDAN CURVE CENTER-FINDER        ")
    print("====================================================\n")

    # 1. Instantiate our test domain with a known manual shift
    true_offset = np.array([0.4, -0.3])
    curve = generate_shifted_bumpy_bezier(n=400, shift_x=true_offset[0], shift_y=true_offset[1])
    print(f"Generated a distorted Jordan curve intentionally shifted to: {true_offset}\n")

    # 2. Launch the robot blindly from the origin [0.0, 0.0]
    initial_guess = np.array([0.0, 0.0])
    found_center, path_history = autonomous_center_hunt(curve, initial_guess)

    print(f"\n====================================================")
    print(f"HUNT COMPLETE!")
    print(f" -> True Offset Location Was: {true_offset}")
    print(f" -> Autonomous Recovered Center: [{found_center[0]:.4f}, {found_center[1]:.4f}]")
    print("====================================================\n")

    # 3. Render a visual diagnostic trace of the optimization path
    print("Exporting optimization trajectory map...")
    fig, ax = plt.subplots(figsize=(7, 7))
    ax.plot(curve[:, 0], curve[:, 1], 'b-', lw=2, label='Shifted Jordan Curve')
    ax.plot(path_history[:, 0], path_history[:, 1], 'ro-', lw=1.5, ms=5, label='Gradient Descent Path')
    ax.scatter(found_center[0], found_center[1], color='green', marker='X', s=150, zorder=5, label='Recovered Center')
    ax.scatter(true_offset[0], true_offset[1], color='black', marker='o', s=50, zorder=4, label='True Symmetry Axis')

    ax.set_title("Autonomous Center Recovery Trajectory")
    ax.set_aspect('equal')
    ax.grid(True, linestyle=':')
    ax.legend(loc='upper right')

    output_filename = "autonomous_center_recovery_path.png"
    plt.savefig(output_filename, dpi=300)
    print(f"Trajectory chart saved as: {output_filename}")

