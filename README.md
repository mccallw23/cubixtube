# CubixTube

A 3D puzzle game similar to Rubik's Cube with unique piece orientations and movement rules.

## Visualization

The puzzle state can be visualized in 3D using matplotlib. The visualization shows:
- Corner pieces as L-shapes
- Straight pieces as lines
- Colors: Red, Blue, Yellow
- Multiple views: isometric, front, top, and right

### Installation

```bash
# For Mac x86_64 users
arch -x86_64 python -m pip install --upgrade pip
arch -x86_64 python -m pip install -r requirements.txt

# For other platforms
pip install -r requirements.txt
```

### Usage

To visualize the cube:

```bash
# View solved state
python visualize_cubixtube.py --state solved

# View custom configuration
python visualize_cubixtube.py --state custom

# Specify custom output directory
python visualize_cubixtube.py --state solved --output-dir my_views
```

The visualization will create PNG files in the specified output directory (defaults to `cube_views/`):
- `isometric.png`: 3D view at 30° elevation, 45° azimuth
- `front.png`: Front view
- `top.png`: Top-down view
- `right.png`: Right side view

### Testing

Run the test scripts to verify visualization:
```bash
# Basic cube visualization test
python test_matplotlib_vis.py

# Test cube movements
python test_movements.py

# Verify cube configuration
python verify_cube.py
```
