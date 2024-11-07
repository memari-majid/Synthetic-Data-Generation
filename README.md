# Synthetic Fall Video Generator (SynFall)

A Python-based tool that leverages Blender and Mixamo to generate synthetic fall detection videos for AI training. This tool automates the creation of diverse, annotated fall scenarios using 3D animation.

## Project Overview

SynFall creates realistic synthetic fall videos by:
- Automating 3D character animations in Blender
- Generating diverse fall scenarios
- Simulating surveillance camera perspectives
- Creating varied lighting conditions
- Producing training data for fall detection AI models

## Prerequisites

1. **Blender Installation**
   - Download and install Blender from [blender.org](https://www.blender.org/download/)
   - Minimum version required: 2.80
   - Recommended: Blender 3.0+ for better performance

2. **Mixamo Account and Models**
   - Create a free account at [mixamo.com](https://www.mixamo.com/)
   - Download the following recommended fall animations:
     * Forward Fall
     * Backward Fall
     * Side Fall
     * Stumble Backwards
     * Trip and Fall
     * Drunk Fall
     * Slip Fall
   - For each animation, download with these settings:
     * Format: FBX
     * FPS: 30
     * No Skin
     * Without Character (if downloading just the animation)

3. **Hardware Requirements**
   - Recommended: 16GB RAM
   - GPU with 4GB+ VRAM
   - 50GB+ free disk space for rendered videos

## Detailed Project Setup

1. **Enable Rigify Add-on in Blender**
   - Open Blender
   - Go to Edit > Preferences
   - Select Add-ons
   - Search for "Rigify"
   - Enable the add-on by checking the box
   - Click "Save Preferences"

2. **Prepare Your Models (Detailed Steps)**
   
   a. **Download Character Models**:
   - Go to Mixamo
   - Recommended base characters:
     * X Bot (standard male character)
     * Y Bot (standard female character)
     * Prisoner
     * Business Casual Man
     * Office Lady
   - Download each character in T-pose

   b. **Download Fall Animations**:
   - Search for each fall type
   - Recommended settings per animation:
     * In Place: Yes
     * Character Facing: Forward
     * Trim: Start from 0%
     * Loop: None

   c. **Organize Your Files**:
   ```
   models/
   ├── characters/
   │   ├── xbot.fbx
   │   ├── ybot.fbx
   │   └── ...
   ├── animations/
   │   ├── forward_fall/
   │   ├── backward_fall/
   │   └── ...
   └── combined/          # After combining characters with animations
   ```

3. **Project Structure**
```
fall_detection_generator/
├── models/                 # Store your FBX files here
│   ├── combined/          # Character + animation combinations
│   ├── characters/        # Base characters
│   └── animations/        # Fall animations
├── output/                # Generated videos will be saved here
│   ├── raw/              # Full quality renders
│   └── processed/        # Compressed surveillance-style footage
├── fall_detection_generator.py
├── run_generator.py
└── README.md
```

## Creating Diverse Fall Scenarios

### 1. Basic Fall Types to Generate

- **Forward Falls**
  - Normal speed
  - Slow motion
  - With rotation
  - With stumbling

- **Backward Falls**
  - Straight back
  - Angular back
  - With sitting attempt
  - With reaching out

- **Side Falls**
  - Left side
  - Right side
  - With recovery attempt
  - With twisting

- **Complex Falls**
  - Slip and fall
  - Trip and fall
  - Gradual collapse
  - Sudden collapse

### 2. Environment Variations

Configure these in the script for variety:

```python
# Camera angles (modify adjust_camera method)
CAMERA_POSITIONS = [
    {'location': (0, -7, 5), 'rotation': (1.1, 0, 0)},    # Front view
    {'location': (7, 0, 5), 'rotation': (1.1, -1.57, 0)}, # Side view
    {'location': (5, -5, 7), 'rotation': (0.9, -0.7, 0)}, # Corner view
]

# Lighting conditions (modify adjust_lighting method)
LIGHTING_SCENARIOS = [
    {'energy': 1.5, 'rotation': (0, 0, 0)},      # Bright day
    {'energy': 0.8, 'rotation': (0.2, 0, 0)},    # Evening
    {'energy': 0.3, 'rotation': (0.4, 0, 0)},    # Night
]
```

### 3. Video Quality Variations

Generate different quality versions:

```python
QUALITY_PRESETS = {
    'high': {
        'resolution': (1920, 1080),
        'fps': 60,
        'noise': False
    },
    'medium': {
        'resolution': (1280, 720),
        'fps': 30,
        'noise': True
    },
    'surveillance': {
        'resolution': (640, 480),
        'fps': 15,
        'noise': True
    },
    'low_quality': {
        'resolution': (320, 240),
        'fps': 10,
        'noise': True
    }
}
```

## Running the Generator

1. **Basic Usage**
   ```bash
   blender -b -P run_generator.py -- --model-dir models/combined --output-dir output/raw
   ```

2. **With Quality Presets**
   ```bash
   blender -b -P run_generator.py -- \
       --model-dir models/combined \
       --output-dir output/surveillance \
       --resolution 640 480 \
       --quality surveillance
   ```

3. **Batch Processing**
   ```bash
   # Create a batch script to generate multiple variations
   for quality in surveillance low_quality medium
   do
       blender -b -P run_generator.py -- \
           --model-dir models/combined \
           --output-dir output/$quality \
           --quality $quality
   done
   ```

## Tips for Realistic Surveillance Footage

1. **Camera Placement**
   - Mount height: 2.5-3 meters (adjust camera.location.z)
   - Slight downward angle (15-30 degrees)
   - Corner placement for wider view

2. **Video Quality**
   - Use lower resolutions (320x240 to 640x480)
   - Reduce frame rate (10-15 fps)
   - Add noise and grain
   - Consider motion blur
   - Compress output files

3. **Lighting Considerations**
   - Simulate different times of day
   - Add shadows and dark areas
   - Include occasional glare
   - Simulate fluorescent flickering

4. **Scene Variations**
   - Different floor textures
   - Various background objects
   - Multiple character positions
   - Different clothing colors

## Performance Optimization

1. **Rendering Speed**
   - Use GPU rendering if available
   - Reduce sample count for faster renders
   - Disable unnecessary features
   - Use lower resolution for initial tests

2. **Batch Processing**
   - Split generation into smaller batches
   - Use multiple Blender instances
   - Monitor system resources
   - Save intermediate results

## Troubleshooting

1. **ImportError: No module named 'bpy'**
   - This is normal when running outside Blender
   - Make sure to run the script through Blender's Python interpreter

2. **FBX Import Fails**
   - Verify file paths are correct
   - Ensure FBX files are properly exported from Mixamo
   - Check Blender's console for specific error messages

3. **Rendering Issues**
   - Verify GPU drivers are up to date
   - Check available system memory
   - Reduce resolution if system is struggling

## Contributing

Feel free to submit issues and enhancement requests!

## License

```
MIT License

Copyright (c) 2024 SynFall (Synthetic Fall Video Generator)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## Acknowledgments

- [Mixamo](https://www.mixamo.com/) for providing 3D character models and animations
- [Blender Foundation](https://www.blender.org/) for their powerful 3D creation suite
- Community contributors for testing and feedback
- Research community in fall detection for inspiration and guidance