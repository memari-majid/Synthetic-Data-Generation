# SynFall - Simple Fall Video Generator

Generate tiny, synthetic fall detection videos using Blender and Mixamo animations. Perfect for creating training data for fall detection AI models.

## Overview

- 🎥 Generates small-sized fall videos (64x64 to 160x120)
- 🎭 Uses simple character animations from Mixamo
- 📦 Optimized for minimal file size
- 🚀 Perfect for initial ML model testing
- 🔄 Supports batch processing
- 🎮 Easy to use with Blender

## Prerequisites

### Required Software
- Blender 3.0+ ([Download](https://www.blender.org/download/))
- Mixamo Account ([Sign Up](https://www.mixamo.com/))

### Hardware Requirements
- Any modern CPU
- 4GB+ RAM
- Basic GPU (optional)
- 1GB free disk space

## Installation

1. **Clone Repository**
   ```bash
   git clone https://github.com/yourusername/synfall.git
   cd synfall
   ```

2. **Create Project Structure**
   ```bash
   mkdir -p models/combined output
   ```

3. **Enable Blender Add-ons**
   - Open Blender
   - Edit > Preferences > Add-ons
   - Search and enable "Rigify"

## Preparing Animation Data

1. **Download Character (from Mixamo)**
   - Go to [Mixamo](https://www.mixamo.com/)
   - Download "X Bot" (standard character)
   - Format: FBX
   - Skin: Without Skin

2. **Download Fall Animations**
   - Simple Forward Fall
   - Simple Backward Fall
   - Simple Side Fall
   - Export Settings:
     * Format: FBX
     * FPS: 30
     * No Skin
     * Keyframes: Reduced

3. **Organize Files**
   ```
   models/combined/
   ├── forward_fall.fbx
   ├── backward_fall.fbx
   └── side_fall.fbx
   ```

## Video Quality Options

| Quality | Resolution | FPS | File Size | Best For |
|---------|------------|-----|-----------|----------|
| tiny    | 64x64      | 5   | ~50KB     | Quick testing, prototypes |
| small   | 128x128    | 8   | ~150KB    | Initial training |
| medium  | 160x120    | 10  | ~300KB    | Final training |

## Video Generation Options

### Quality Presets

| Quality | Resolution | FPS | File Size | Best For |
|---------|------------|-----|-----------|----------|
| tiny    | 64x64      | 5   | ~50KB     | Quick testing, prototypes |
| small   | 128x128    | 8   | ~150KB    | Initial training |
| medium  | 160x120    | 10  | ~300KB    | Final training |

### Variation Levels

| Level   | Description | Use Case |
|---------|-------------|----------|
| minimal | Fixed camera, no rotation, standard lighting | Testing pipeline |
| low     | Basic variations in angle and lighting | Initial dataset |
| medium  | Moderate variations in all parameters | Standard training |
| high    | Maximum variation in all aspects | Robust training |

## Usage

### Basic Generation
```bash
# Generate 10 videos with medium variation
blender -b -P run_synfall.py -- \
    --model-dir "models/combined" \
    --output-dir "output" \
    --quality tiny \
    --num-videos 10 \
    --variation medium
```

### Python Script
```python
from synthetic_fall_generator import SyntheticFallGenerator

# Initialize generator with specific settings
generator = SyntheticFallGenerator(
    model_dir="models/combined",
    output_dir="output",
    quality='tiny',        # 64x64 resolution
    num_videos=10,         # Generate 10 videos
    variation_level='high' # Maximum variation
)

# Generate dataset
generator.generate_dataset()
```

### Advanced Usage Examples

1. **Quick Test (Minimal Variation)**
   ```bash
   blender -b -P run_synfall.py -- \
       --model-dir "models/combined" \
       --output-dir "output/test" \
       --quality tiny \
       --num-videos 5 \
       --variation minimal
   ```

2. **Large Dataset (High Variation)**
   ```bash
   blender -b -P run_synfall.py -- \
       --model-dir "models/combined" \
       --output-dir "output/training" \
       --quality small \
       --num-videos 100 \
       --variation high
   ```

3. **Multiple Quality Levels**
   Generate a comprehensive dataset with all quality and variation combinations. This script:
   - Creates 9 different subsets (3 qualities × 3 variations)
   - Generates 20 videos per combination (180 total videos)
   - Organizes outputs in separate folders by quality and variation
   - Takes approximately 30-45 minutes to complete
   
   ```bash
   # Create base output directory
   mkdir -p output

   # Generate all combinations of quality and variation levels
   for quality in tiny small medium  # Resolutions: 64x64, 128x128, 160x120
   do
       for variation in low medium high  # Different levels of randomization
       do
           echo "Generating ${quality} quality videos with ${variation} variation..."
           
           # Create specific output directory
           mkdir -p "output/${quality}_${variation}"
           
           # Run Blender with current settings
           blender -b -P run_synfall.py -- \
               --model-dir "models/combined" \
               --output-dir "output/${quality}_${variation}" \
               --quality "$quality" \
               --num-videos 20 \
               --variation "$variation" \
               --seed $RANDOM  # Add randomization between runs
           
           echo "Completed ${quality}_${variation} subset"
       done
   done

   echo "Dataset generation complete. Check output/ directory for results."
   ```

   Expected directory structure after completion:
   ```
   output/
   ├── tiny_low/      # 64x64 videos with low variation
   ├── tiny_medium/   # 64x64 videos with medium variation
   ├── tiny_high/     # 64x64 videos with high variation
   ├── small_low/     # 128x128 videos with low variation
   ├── small_medium/  # 128x128 videos with medium variation
   ├── small_high/    # 128x128 videos with high variation
   ├── medium_low/    # 160x120 videos with low variation
   ├── medium_medium/ # 160x120 videos with medium variation
   └── medium_high/   # 160x120 videos with high variation
   ```

## Variation Parameters

### Minimal Variation
- Fixed front camera (height: 4m)
- No character rotation
- Standard lighting
- Basic ground material
- No additional noise

### Low Variation
- 3 rotation angles (-15°, 0°, 15°)
- 2 camera heights (3m, 4m)
- 2 camera angles
- Basic lighting changes
- Simple ground variations

### Medium Variation
- 5 rotation angles
- 3 camera heights
- 4 camera angles
- Multiple lighting conditions
- Various ground materials
- Speed variations

### High Variation
- 7 rotation angles (-45° to 45°)
- 5 camera heights (2m to 6m)
- 6 camera angles
- 5 lighting conditions
- 4 ground materials
- Maximum position/rotation variation
- Full speed range

## Tips for Different Use Cases

### For Testing
```bash
# Generate minimal variation test set
blender -b -P run_synfall.py -- \
    --model-dir "models/combined" \
    --output-dir "output/test" \
    --quality tiny \
    --num-videos 5 \
    --variation minimal
```

### For Initial Training
```bash
# Generate medium-sized training set
blender -b -P run_synfall.py -- \
    --model-dir "models/combined" \
    --output-dir "output/training" \
    --quality small \
    --num-videos 50 \
    --variation medium
```

### For Production Dataset
```bash
# Generate large, varied dataset
blender -b -P run_synfall.py -- \
    --model-dir "models/combined" \
    --output-dir "output/production" \
    --quality medium \
    --num-videos 200 \
    --variation high
```

## Project Structure
```
synfall/
├── models/
│   └── combined/     # FBX files here
├── output/           # Generated videos
├── synthetic_fall_generator.py
├── run_synfall.py
└── README.md
```

## Optimization Tips

### For Smaller Files
- Use 'tiny' quality preset
- Keep animations short
- Use simple backgrounds
- Enable maximum compression

### For Faster Generation
- Use GPU acceleration
- Lower sample counts
- Reduce animation frames
- Close other applications

### For Better Quality
- Increase samples slightly
- Add minimal noise
- Use proper lighting
- Keep stable camera

## Troubleshooting

### Common Issues

1. **Blender Won't Start**
   ```bash
   # Check Blender installation
   blender --version
   ```

2. **Import Errors**
   - Run through Blender only
   - Check file paths
   - Use absolute paths

3. **Rendering Issues**
   - Start with 'tiny' quality
   - Check GPU settings
   - Monitor memory usage

### Error Messages

- `No module named 'bpy'`: Run through Blender
- `File not found`: Check paths
- `Out of memory`: Lower resolution

## Examples

### Command Line Options
```bash
# Basic usage
blender -b -P run_synfall.py -- --model-dir "models" --output-dir "output" --quality tiny

# Custom resolution
blender -b -P run_synfall.py -- --model-dir "models" --output-dir "output" --resolution 100 100

# Test mode
blender -b -P run_synfall.py -- --model-dir "models" --output-dir "output" --test-only
```

## Contributing
- Fork the repository
- Create feature branch
- Submit pull request

## GPU Resources
This project has been allocated 3,000 GPU hours through the National Science Foundation ACCESS program. If you need GPU resources for running large-scale video generation, please contact:

**Contact:** mmemari@uvu.edu

### About NSF ACCESS
[ACCESS](https://access-ci.org/) (Advanced Cyberinfrastructure Coordination Ecosystem: Services & Support) is the National Science Foundation's advanced computing ecosystem that provides computing resources to support scientific research.

## License
MIT License - See [LICENSE](LICENSE) file

## Acknowledgments
- Mixamo for animations
- Blender Foundation
- Open source community