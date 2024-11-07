# SynFall (Synthetic Fall Video Generator)

A Python-based tool that leverages Blender and Mixamo to generate synthetic fall detection videos for AI training. This tool automates the creation of diverse, annotated fall scenarios using 3D animation.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Advanced Configuration](#advanced-configuration)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Overview
SynFall creates realistic synthetic fall videos by:
- Automating 3D character animations in Blender
- Generating diverse fall scenarios
- Simulating surveillance camera perspectives
- Creating varied lighting conditions
- Producing training data for fall detection AI models

## Features
- Multiple fall types (forward, backward, side, complex)
- Customizable camera angles and positions
- Various lighting conditions
- Multiple quality presets
- Batch processing capabilities
- Realistic surveillance footage simulation

## Prerequisites

### Hardware Requirements
- CPU: Multi-core processor (recommended: 4+ cores)
- RAM: 16GB minimum
- GPU: NVIDIA/AMD GPU with 4GB+ VRAM
- Storage: 50GB+ free disk space

### Software Requirements
1. **Blender**
   - Version 2.80 or higher (3.0+ recommended)
   - [Download Blender](https://www.blender.org/download/)

2. **Mixamo Account**
   - Free account at [mixamo.com](https://www.mixamo.com/)
   - Access to character models and animations

## Installation

1. **Clone Repository**
   ```bash
   git clone https://github.com/yourusername/synfall.git
   cd synfall
   ```

2. **Setup Project Structure**
   ```bash
   mkdir -p models/{characters,animations,combined}
   mkdir -p output/{raw,processed}
   ```

3. **Enable Blender Add-ons**
   - Open Blender
   - Go to Edit > Preferences > Add-ons
   - Enable "Rigify"

4. **Download Required Assets**
   - Character Models from Mixamo:
     * X Bot (standard male)
     * Y Bot (standard female)
     * Additional characters as needed
   - Fall Animations:
     * Forward Fall
     * Backward Fall
     * Side Fall
     * Stumble Backwards
     * Trip and Fall
     * Drunk Fall
     * Slip Fall

## Usage

### Basic Usage
1. **Prepare Environment**
   ```python
   from synthetic_fall_generator import SyntheticFallGenerator
   
   generator = SyntheticFallGenerator(
       model_dir="models/combined",
       output_dir="output/raw",
       resolution=(640, 480),
       quality='surveillance'
   )
   
   generator.generate_dataset()
   ```

2. **Command Line Usage**
   ```bash
   blender -b -P run_synfall.py -- \
       --model-dir "models/combined" \
       --output-dir "output/raw" \
       --resolution 640 480
   ```

### Quality Presets
```python
QUALITY_PRESETS = {
    'high': {
        'resolution': (1920, 1080),
        'fps': 60,
        'noise': False,
        'samples': 128
    },
    'surveillance': {
        'resolution': (640, 480),
        'fps': 15,
        'noise': True,
        'samples': 32
    }
    # Additional presets available
}
```

## Advanced Configuration

### Camera Settings
```python
def adjust_camera(self):
    camera = bpy.data.objects["Camera"]
    camera.location.x = random.uniform(-2, 2)
    camera.location.y = random.uniform(-8, -6)
    camera.location.z = random.uniform(4, 6)
```

### Lighting Configuration
```python
def adjust_lighting(self):
    light = bpy.data.objects["Sun"]
    light.data.energy = random.uniform(0.5, 1.5)
    light.data.color = (
        random.uniform(0.95, 1.0),
        random.uniform(0.95, 1.0),
        random.uniform(0.95, 1.0)
    )
```

### Performance Optimization
1. **Rendering**
   - Enable GPU acceleration
   - Adjust sample counts
   - Use appropriate resolution

2. **Batch Processing**
   - Split into smaller batches
   - Monitor system resources
   - Use multiple instances

## Troubleshooting

### Common Issues
1. **Import Errors**
   - Run through Blender
   - Check Python path

2. **Rendering Problems**
   - Verify GPU drivers
   - Check memory usage
   - Reduce resolution

## Contributing
Contributions are welcome! Please feel free to submit issues and pull requests.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments
- [Mixamo](https://www.mixamo.com/) for 3D models and animations
- [Blender Foundation](https://www.blender.org/) for the 3D creation suite
- Community contributors and testers