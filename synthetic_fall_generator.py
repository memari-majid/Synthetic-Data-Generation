import bpy
import random
import math
from pathlib import Path
import numpy as np

class SyntheticFallGenerator:
    """Generator for synthetic fall detection videos using Blender"""
    def __init__(self, model_dir, output_dir, resolution=(320, 240), quality='surveillance'):
        self.model_dir = Path(model_dir)
        self.output_dir = Path(output_dir)
        self.resolution = resolution
        self.quality = quality
        
        # Updated quality presets optimized for surveillance footage
        self.QUALITY_PRESETS = {
            'tiny': {
                'resolution': (64, 64),
                'fps': 5,
                'noise': True,
                'samples': 4,
                'compression': 'HIGHEST'
            },
            'small': {
                'resolution': (128, 128),
                'fps': 8,
                'noise': True,
                'samples': 8,
                'compression': 'HIGH'
            },
            'medium': {
                'resolution': (160, 120),
                'fps': 10,
                'noise': True,
                'samples': 16,
                'compression': 'HIGH'
            }
        }
        
        # Create output directory if it doesn't exist
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def setup_scene(self):
        """Initialize the scene by removing default objects and setting up basic elements"""
        # Clear existing objects
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete(use_global=False)
        
        # Add ground plane
        bpy.ops.mesh.primitive_plane_add(size=10, location=(0, 0, 0))
        ground = bpy.context.active_object
        ground.name = "Ground"
        
        # Add basic material to ground
        mat = bpy.data.materials.new(name="GroundMaterial")
        mat.use_nodes = True
        ground.data.materials.append(mat)
        
        # Add camera
        bpy.ops.object.camera_add(location=(0, -7, 5), rotation=(1.1, 0, 0))
        camera = bpy.context.active_object
        camera.name = "Camera"
        bpy.context.scene.camera = camera
        
        # Add lighting
        bpy.ops.object.light_add(type='SUN', location=(0, 0, 10))
        light = bpy.context.active_object
        light.name = "Sun"
        
    def load_model(self, filepath):
        """Import the FBX model from Mixamo"""
        try:
            bpy.ops.import_scene.fbx(filepath=str(filepath))
            model = bpy.context.selected_objects[0]
            model.name = "Human"
            model.location.z = 0.1  # Slightly above ground
            return model
        except Exception as e:
            print(f"Error loading model {filepath}: {e}")
            return None
        
    def apply_fall_animation(self):
        """Configure the fall animation settings"""
        try:
            model = bpy.data.objects["Human"]
            armature = [obj for obj in model.children if obj.type == 'ARMATURE'][0]
            bpy.context.view_layer.objects.active = armature
            
            # Set animation length
            scene = bpy.context.scene
            scene.frame_start = 0
            scene.frame_end = 90  # 3 seconds at 30fps
            
            # Randomize animation speed
            scene.render.fps = self.QUALITY_PRESETS[self.quality]['fps']
            
        except Exception as e:
            print(f"Error applying animation: {e}")
        
    def adjust_camera(self):
        """Randomize camera position and angle"""
        camera = bpy.data.objects["Camera"]
        
        # Randomize camera position within realistic surveillance mounting positions
        camera.location.x = random.uniform(-2, 2)
        camera.location.y = random.uniform(-8, -6)
        camera.location.z = random.uniform(4, 6)
        
        # Adjust camera angle to look at the center of the scene
        camera.rotation_euler = (
            random.uniform(0.9, 1.2),  # Downward angle
            random.uniform(-0.1, 0.1),  # Slight horizontal variation
            random.uniform(-0.1, 0.1)   # Slight tilt
        )
        
    def adjust_lighting(self):
        """Randomize lighting conditions"""
        light = bpy.data.objects["Sun"]
        light.data.energy = random.uniform(0.5, 1.5)
        light.rotation_euler = (
            random.uniform(-0.1, 0.1),
            random.uniform(-0.1, 0.1),
            random.uniform(-math.pi, math.pi)
        )
        
        # Add slight color variation to simulate different times of day
        light.data.color = (
            random.uniform(0.95, 1.0),  # Red
            random.uniform(0.95, 1.0),  # Green
            random.uniform(0.95, 1.0)   # Blue
        )
        
    def setup_render_settings(self, output_path):
        """Configure render settings optimized for low-resolution output"""
        scene = bpy.context.scene
        scene.render.image_settings.file_format = 'FFMPEG'
        scene.render.ffmpeg.format = 'MPEG4'
        scene.render.ffmpeg.codec = 'H264'
        scene.render.filepath = str(output_path)
        
        # Apply quality preset settings
        preset = self.QUALITY_PRESETS[self.quality]
        scene.render.resolution_x, scene.render.resolution_y = preset['resolution']
        scene.render.fps = preset['fps']
        
        # Optimize render settings for low quality
        scene.render.resolution_percentage = 100
        scene.render.use_border = False
        scene.render.use_compositing = True
        scene.render.use_sequencer = False
        
        # Configure render engine for speed
        scene.render.engine = 'CYCLES'
        scene.cycles.samples = preset['samples']
        scene.cycles.use_denoising = True
        scene.cycles.preview_samples = 8
        
        # Optimize video compression for surveillance footage
        scene.render.ffmpeg.constant_rate_factor = preset['compression']
        scene.render.ffmpeg.gopsize = 10
        scene.render.ffmpeg.use_max_b_frames = False
        scene.render.ffmpeg.minrate = 0
        scene.render.ffmpeg.maxrate = 1000
        scene.render.ffmpeg.buffersize = 1000
        
    def add_noise(self):
        """Enhanced noise settings for surveillance look"""
        if self.QUALITY_PRESETS[self.quality]['noise']:
            scene = bpy.context.scene
            scene.use_nodes = True
            nodes = scene.node_tree.nodes
            nodes.clear()
            
            # Add and configure nodes
            render_layers = nodes.new(type="CompositorNodeRLayers")
            noise = nodes.new(type="CompositorNodeNoise")
            blur = nodes.new(type="CompositorNodeBlur")
            mix = nodes.new(type="CompositorNodeMixRGB")
            bright_contrast = nodes.new(type="CompositorNodeBrightContrast")
            output = nodes.new(type="CompositorNodeComposite")
            
            # Configure noise for surveillance look
            noise.inputs[1].default_value = 0.15  # Amount
            noise.inputs[2].default_value = 1500  # Size
            
            # Add slight blur
            blur.size_x = 0.5
            blur.size_y = 0.5
            
            # Adjust brightness and contrast
            bright_contrast.inputs[1].default_value = -0.05  # Brightness
            bright_contrast.inputs[2].default_value = 1.1    # Contrast
            
            # Configure mixing
            mix.blend_type = 'ADD'
            mix.inputs[0].default_value = 0.08  # Factor
            
            # Link nodes
            links = scene.node_tree.links
            links.new(render_layers.outputs[0], blur.inputs[0])
            links.new(blur.outputs[0], bright_contrast.inputs[0])
            links.new(bright_contrast.outputs[0], mix.inputs[1])
            links.new(noise.outputs[0], mix.inputs[2])
            links.new(mix.outputs[0], output.inputs[0])
        
    def generate_scene(self, model_path, output_path):
        """Generate a complete fall scene"""
        try:
            self.setup_scene()
            model = self.load_model(model_path)
            
            if model is None:
                return False
                
            self.apply_fall_animation()
            self.adjust_camera()
            self.adjust_lighting()
            self.add_noise()
            self.setup_render_settings(output_path)
            
            # Render animation
            bpy.ops.render.render(animation=True)
            return True
            
        except Exception as e:
            print(f"Error generating scene: {e}")
            return False
        
    def generate_dataset(self):
        """Generate multiple fall scenes from available models"""
        model_files = list(self.model_dir.glob('*.fbx'))
        
        if not model_files:
            raise FileNotFoundError(f"No FBX files found in {self.model_dir}")
            
        successful = 0
        for i, model_path in enumerate(model_files):
            output_path = self.output_dir / f"fall_scene_{i}.mp4"
            print(f"Generating scene {i+1}/{len(model_files)}: {output_path}")
            
            if self.generate_scene(model_path, output_path):
                successful += 1
                
        print(f"Generation complete. Successfully generated {successful}/{len(model_files)} scenes.")