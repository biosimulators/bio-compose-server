import numpy as np


def generate_color_gradient(simulator_names) -> list[str]:
    """Generate a gradient of colors from red to green to blue for a list of simulator names."""
    num_simulators = len(simulator_names)

    red_to_green = np.linspace([1, 0, 0], [0, 1, 0], num=int(np.ceil(num_simulators / 2)), endpoint=False)
    green_to_blue = np.linspace([0, 1, 0], [0, 0, 1], num=int(np.ceil(num_simulators / 2 + 1)))

    full_gradient = np.vstack([red_to_green, green_to_blue])[1:num_simulators + 1]

    hex_colors = ['#{:02x}{:02x}{:02x}'.format(int(r * 255), int(g * 255), int(b * 255)) for r, g, b in full_gradient]

    return hex_colors
