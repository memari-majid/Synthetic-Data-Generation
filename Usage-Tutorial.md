# Usage Tutorial

## Basic Usage

### 1. Prepare Models
1. Download character models from Mixamo
2. Download fall animations
3. Place files in appropriate directories

### 2. Generate Videos
```bash
blender -b -P run_synfall.py -- --model-dir models/combined --output-dir output/raw
```

## Advanced Usage

### Quality Presets
```bash
blender -b -P run_synfall.py -- \
    --model-dir models/combined \
    --output-dir output/surveillance \
    --resolution 640 480 \
    --quality surveillance
```

### Batch Processing
```bash
for quality in surveillance low_quality medium
do
    blender -b -P run_synfall.py -- \
        --model-dir models/combined \
        --output-dir output/$quality \
        --quality $quality
done
```

## Configuration Options

### Camera Settings
- Height: 2.5-3 meters
- Angle: 15-30 degrees downward
- Position: Corner or wall-mounted

### Video Quality
- Resolution: 320x240 to 1920x1080
- FPS: 10-60
- Noise: Optional grain effect 