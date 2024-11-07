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

## Basic Usage

### Command Line Options
```bash
# Basic usage
blender -b -P run_synfall.py -- --model-dir "models" --output-dir "output" --quality tiny

# Custom resolution
blender -b -P run_synfall.py -- --model-dir "models" --output-dir "output" --resolution 100 100

# Test mode
blender -b -P run_synfall.py -- --model-dir "models" --output-dir "output" --test-only
```

### Python Script
```python
from synthetic_fall_generator import SyntheticFallGenerator

generator = SyntheticFallGenerator(
    model_dir="models/combined",
    output_dir="output",
    quality='tiny',        
    num_videos=10,         
    variation_level='high' 
)

generator.generate_dataset()
```

## Advanced Usage

### Video Quality Options

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

## HPC and GPU Resources

### Available Resources
This project has been allocated 3,000 GPU hours through the National Science Foundation ACCESS program. If you need GPU resources for running large-scale video generation, please contact:

**Contact:** mmemari@uvu.edu

### About NSF ACCESS
[ACCESS](https://access-ci.org/) (Advanced Cyberinfrastructure Coordination Ecosystem: Services & Support) is the National Science Foundation's advanced computing ecosystem that provides computing resources to support scientific research.

### HPC Installation and Requirements

1. **Basic Requirements**
   - OpenGL library (usually Mesa or libGLU)
   - Multi-process support
   - GPU support (optional but recommended)

2. **Module Loading**
   ```bash
   # Example module load command
   module load Mesa/.20.2.1-GCCcore-10.2.0
   module load blender
   ```

### HPC Job Submission

1. **Basic CPU Job Script (SLURM)**
   ```bash
   #!/bin/bash
   #SBATCH --job-name=synfall
   #SBATCH --output=render.out
   #SBATCH --error=render.err
   #SBATCH --time=24:00:00
   #SBATCH --nodes=1
   #SBATCH --ntasks-per-node=20
   #SBATCH --partition=epyc2
   #SBATCH --mem-per-cpu=5GB

   module load Mesa/.20.2.1-GCCcore-10.2.0
   module load blender

   blender -b -P run_synfall.py -- \
       --model-dir "models/combined" \
       --output-dir "output" \
       --quality medium \
       --num-videos 100
   ```

2. **GPU Job Script (SLURM)**
   ```bash
   #!/bin/bash
   #SBATCH --job-name=synfall_gpu
   #SBATCH --output=render_gpu.out
   #SBATCH --error=render_gpu.err
   #SBATCH --time=12:00:00
   #SBATCH --nodes=1
   #SBATCH --gres=gpu:4
   #SBATCH --partition=gpu
   #SBATCH --mem=64G

   module load blender

   blender -b -P run_synfall.py -- \
       --model-dir "models/combined" \
       --output-dir "output" \
       --quality high \
       --num-videos 100 \
       --variation high
   ```

### Performance Considerations

1. **CPU Scaling**
   | Number of CPU | Render Time (s) |
   |---------------|----------------|
   | 2             | 97            |
   | 4             | 40            |
   | 8             | 25            |
   | 16            | 13            |
   | 32            | 11            |
   | 64            | 8             |

2. **Important Notes**
   - Use CYCLES render engine (EEVEE doesn't support headless rendering)
   - For multi-node support, Blender needs to be built manually
   - GPU support requires proper CUDA/OpenCL configuration

### Resource Request Guidelines

For optimal performance, request:
- 4-8 GPUs (V100 or A100)
- 1TB storage
- 3-month allocation
- 3,000 GPU hours

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
- National Science Foundation ACCESS program