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

## Usage

### Quick Test
```bash
# Generate a single test video
blender -b -P run_synfall.py -- \
    --model-dir "models/combined" \
    --output-dir "output" \
    --quality tiny
```

### Python Script
```python
from synthetic_fall_generator import SyntheticFallGenerator

# Initialize generator
generator = SyntheticFallGenerator(
    model_dir="models/combined",
    output_dir="output",
    quality='tiny'  # 64x64 resolution
)

# Generate dataset
generator.generate_dataset()
```

### Batch Processing
```bash
# Generate all qualities
for quality in tiny small medium
do
    blender -b -P run_synfall.py -- \
        --model-dir "models/combined" \
        --output-dir "output/$quality" \
        --quality "$quality"
done
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

## License
MIT License - See [LICENSE](LICENSE) file

## Acknowledgments
- Mixamo for animations
- Blender Foundation
- Open source community