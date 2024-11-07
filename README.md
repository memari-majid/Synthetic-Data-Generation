# Automated Fall Detection Video Generator

This project automates the generation of fall detection videos using Blender's Python API. It creates realistic fall scenarios that can be used for training machine learning models in fall detection systems.

## Prerequisites

1. **Blender Installation**
   - Download and install Blender from [blender.org](https://www.blender.org/download/)
   - Minimum version required: 2.80

2. **Mixamo Account**
   - Create a free account at [mixamo.com](https://www.mixamo.com/)
   - Download character models and fall animations in FBX format

## Project Setup

1. **Enable Rigify Add-on in Blender**
   - Open Blender
   - Go to Edit > Preferences
   - Select Add-ons
   - Search for "Rigify"
   - Enable the add-on by checking the box
   - Click "Save Preferences"

2. **Prepare Your Models**
   - Create a directory for your models
   - Download various fall animations from Mixamo
   - Save the FBX files in your models directory

3. **Project Structure**
```
fall_detection_generator/
├── models/                 # Store your FBX files here
├── output/                # Generated videos will be saved here
├── fall_detection_generator.py
└── README.md
```

## Usage

1. **Running from Blender's Text Editor**
   ```python
   from fall_detection_generator import FallSceneGenerator
   
   # Initialize the generator
   generator = FallSceneGenerator(
       model_dir="path/to/your/models",
       output_dir="path/to/output",
       resolution=(320, 240)
   )
   
   # Generate the dataset
   generator.generate_dataset()
   ```

2. **Running from Command Line**
   ```bash
   blender -b -P run_generator.py -- --model-dir /path/to/models --output-dir /path/to/output
   ```

## Customization Options

### Resolution
Adjust video resolution in the FallSceneGenerator initialization:
```python
generator = FallSceneGenerator(
    model_dir="models",
    output_dir="output",
    resolution=(160, 120)  # Lower resolution for more realistic surveillance footage
)
```

### Camera Settings
Modify camera positions in the `adjust_camera` method:
```python
def adjust_camera(self):
    camera = bpy.data.objects["Camera"]
    camera.location.x = random.uniform(-2, 2)  # Adjust range as needed
    camera.location.y = random.uniform(-8, -6)
    camera.location.z = random.uniform(4, 6)
```

### Lighting Conditions
Customize lighting in the `adjust_lighting` method:
```python
def adjust_lighting(self):
    light = bpy.data.objects["Sun"]
    light.data.energy = random.uniform(0.5, 1.5)  # Adjust range for different lighting intensities
```

## Tips for Best Results

1. **Model Preparation**
   - Download various fall animations from Mixamo
   - Use different character models for diversity
   - Ensure models are properly rigged

2. **Video Quality**
   - Lower resolution (e.g., 320x240) simulates surveillance cameras
   - Enable noise for more realistic footage
   - Use different camera angles for variety

3. **Performance**
   - Close other applications while rendering
   - Monitor system resources
   - Consider batch processing for large datasets

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

This project is licensed under the MIT License - see the LICENSE file for details.