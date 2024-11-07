import bpy
import random
import math
from pathlib import Path
import numpy as np

class SyntheticFallGenerator:
    """Generator for synthetic fall detection videos using Blender"""
    def __init__(self, model_dir, output_dir, resolution=(320, 240), quality='surveillance', 
                 num_videos=10, variation_level='medium'):
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
        
        # Add variation settings
        self.VARIATION_SETTINGS = {
            # Character variations
            'rotations': [-45, -30, -15, 0, 15, 30, 45],  # More rotation angles
            'initial_poses': [
                {'bend': 0.0, 'twist': 0.0},    # Standing straight
                {'bend': 0.1, 'twist': 0.1},    # Slightly bent
                {'bend': -0.1, 'twist': -0.1},  # Leaning back
            ],
            
            # Fall variations
            'fall_speeds': [0.6, 0.8, 1.0, 1.2, 1.5],  # More speed options
            'fall_types': [
                'forward_straight',
                'forward_twist',
                'backward_simple',
                'backward_sit',
                'sideways_left',
                'sideways_right',
                'stumble_forward',
                'stumble_backward',
                'collapse_vertical'
            ],
            
            # Environment variations
            'camera_heights': [2, 3, 4, 5, 6],  # More height options
            'camera_angles': [
                (1.0, 0, 0),      # Front view
                (1.1, 0.5, 0),    # Side-front right
                (1.1, -0.5, 0),   # Side-front left
                (1.2, 0.8, 0),    # Side right
                (1.2, -0.8, 0),   # Side left
                (0.8, 0, 0),      # High angle
                (1.4, 0, 0),      # Low angle
            ],
            
            # Lighting variations
            'lighting_conditions': [
                {'energy': 1.5, 'color': (1, 1, 1)},        # Bright daylight
                {'energy': 1.2, 'color': (1, 0.95, 0.8)},   # Warm light
                {'energy': 0.8, 'color': (0.9, 0.9, 0.8)},  # Dim indoor
                {'energy': 0.5, 'color': (0.8, 0.8, 0.9)},  # Dark area
                {'energy': 0.3, 'color': (0.7, 0.7, 1.0)},  # Night time
            ],
            
            # Ground variations
            'ground_materials': [
                {'color': (0.2, 0.2, 0.2), 'roughness': 0.8},  # Concrete
                {'color': (0.3, 0.2, 0.1), 'roughness': 0.9},  # Wood
                {'color': (0.4, 0.4, 0.4), 'roughness': 0.7},  # Tile
                {'color': (0.15, 0.15, 0.15), 'roughness': 0.6}  # Smooth floor
            ],
        }
        
        # Create output directory if it doesn't exist
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.num_videos = num_videos
        self.variation_level = variation_level
        
        # Variation levels configuration
        self.VARIATION_LEVELS = {
            'minimal': {
                'rotations': [0],  # No rotation
                'camera_heights': [4],  # Fixed height
                'camera_angles': [(1.0, 0, 0)],  # Front only
                'lighting_conditions': [{'energy': 1.0, 'color': (1, 1, 1)}],  # Standard lighting
                'fall_speeds': [1.0],  # Normal speed
                'ground_materials': [{'color': (0.2, 0.2, 0.2), 'roughness': 0.8}],  # Basic ground
                'use_noise': False,
                'position_range': 0.5,
                'rotation_chance': 0
            },
            'low': {
                'rotations': [-15, 0, 15],
                'camera_heights': [3, 4],
                'camera_angles': [(1.0, 0, 0), (1.1, 0.5, 0)],
                'lighting_conditions': [
                    {'energy': 1.2, 'color': (1, 1, 1)},
                    {'energy': 0.8, 'color': (0.9, 0.9, 0.9)}
                ],
                'fall_speeds': [0.8, 1.0, 1.2],
                'ground_materials': [
                    {'color': (0.2, 0.2, 0.2), 'roughness': 0.8},
                    {'color': (0.3, 0.2, 0.1), 'roughness': 0.9}
                ],
                'use_noise': True,
                'position_range': 1.0,
                'rotation_chance': 0.1
            },
            'medium': {
                # ... existing variation settings ...
            },
            'high': {
                'rotations': [-45, -30, -15, 0, 15, 30, 45],
                'camera_heights': [2, 3, 4, 5, 6],
                'camera_angles': [
                    (1.0, 0, 0), (1.1, 0.5, 0), (1.1, -0.5, 0),
                    (1.2, 0.8, 0), (1.2, -0.8, 0), (0.8, 0, 0)
                ],
                'lighting_conditions': [
                    {'energy': 1.5, 'color': (1, 1, 1)},
                    {'energy': 1.2, 'color': (1, 0.95, 0.8)},
                    {'energy': 0.8, 'color': (0.9, 0.9, 0.8)},
                    {'energy': 0.5, 'color': (0.8, 0.8, 0.9)},
                    {'energy': 0.3, 'color': (0.7, 0.7, 1.0)}
                ],
                'fall_speeds': [0.6, 0.8, 1.0, 1.2, 1.5],
                'ground_materials': [
                    {'color': (0.2, 0.2, 0.2), 'roughness': 0.8},
                    {'color': (0.3, 0.2, 0.1), 'roughness': 0.9},
                    {'color': (0.4, 0.4, 0.4), 'roughness': 0.7},
                    {'color': (0.15, 0.15, 0.15), 'roughness': 0.6}
                ],
                'use_noise': True,
                'position_range': 2.0,
                'rotation_chance': 0.5
            }
        }
        
        # Use variation level settings
        self.current_variations = self.VARIATION_LEVELS[variation_level]
        
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
        
    def apply_initial_pose(self, model):
        """Apply random initial pose variation"""
        pose = random.choice(self.VARIATION_SETTINGS['initial_poses'])
        armature = [obj for obj in model.children if obj.type == 'ARMATURE'][0]
        
        # Apply slight variations to the armature
        for bone in armature.pose.bones:
            if 'spine' in bone.name.lower():
                bone.rotation_euler.x = pose['bend']
                bone.rotation_euler.y = pose['twist']
        
    def apply_fall_animation(self):
        """Configure the fall animation with enhanced variations"""
        try:
            model = bpy.data.objects["Human"]
            
            # Apply initial pose variation
            self.apply_initial_pose(model)
            
            # Rotate character randomly
            model.rotation_euler.z = math.radians(
                random.choice(self.VARIATION_SETTINGS['rotations'])
            )
            
            # Set animation length and speed
            scene = bpy.context.scene
            scene.frame_start = 0
            scene.frame_end = 90  # 3 seconds at 30fps
            
            # Vary animation speed
            speed_multiplier = random.choice(self.VARIATION_SETTINGS['fall_speeds'])
            scene.render.fps = int(self.QUALITY_PRESETS[self.quality]['fps'] * speed_multiplier)
            
            # Add position variations
            offset_range = 1.5  # Increased range for more variation
            model.location.x += random.uniform(-offset_range, offset_range)
            model.location.y += random.uniform(-offset_range, offset_range)
            
            # Add slight rotation variation during fall
            if random.random() < 0.3:  # 30% chance of additional rotation
                model.keyframe_insert(data_path="rotation_euler", frame=0)
                model.rotation_euler.z += math.radians(random.uniform(-30, 30))
                model.keyframe_insert(data_path="rotation_euler", frame=45)
            
        except Exception as e:
            print(f"Error applying animation: {e}")
        
    def adjust_camera(self):
        """Enhanced camera position and angle variations"""
        camera = bpy.data.objects["Camera"]
        
        # Choose random camera height
        height = random.choice(self.VARIATION_SETTINGS['camera_heights'])
        
        # Choose random camera angle preset
        angle = random.choice(self.VARIATION_SETTINGS['camera_angles'])
        
        # Set camera position with some random variation
        camera.location = (
            random.uniform(-2, 2),  # X position
            random.uniform(-8, -6), # Y position
            height + random.uniform(-0.5, 0.5)  # Z position with slight variation
        )
        
        # Set camera rotation with slight random variation
        camera.rotation_euler = (
            angle[0] + random.uniform(-0.1, 0.1),
            angle[1] + random.uniform(-0.1, 0.1),
            angle[2] + random.uniform(-0.1, 0.1)
        )
        
    def adjust_lighting(self):
        """Enhanced lighting variations"""
        light = bpy.data.objects["Sun"]
        
        # Choose random lighting condition
        lighting = random.choice(self.VARIATION_SETTINGS['lighting_conditions'])
        
        # Apply lighting with slight random variation
        light.data.energy = lighting['energy'] * random.uniform(0.9, 1.1)
        light.data.color = (
            lighting['color'][0] * random.uniform(0.95, 1.05),
            lighting['color'][1] * random.uniform(0.95, 1.05),
            lighting['color'][2] * random.uniform(0.95, 1.05)
        )
        
        # Vary light direction
        light.rotation_euler = (
            random.uniform(-0.2, 0.2),
            random.uniform(-0.2, 0.2),
            random.uniform(-math.pi, math.pi)
        )
        
    def add_background_variation(self):
        """Enhanced background variations"""
        ground = bpy.data.objects["Ground"]
        mat = ground.data.materials[0]
        nodes = mat.node_tree.nodes
        
        # Choose random ground material
        material = random.choice(self.VARIATION_SETTINGS['ground_materials'])
        
        # Add material nodes
        color = nodes.new(type='ShaderNodeRGB')
        roughness = nodes.new(type='ShaderNodeValue')
        
        # Set material properties
        color.outputs[0].default_value = (*material['color'], 1.0)
        roughness.outputs[0].default_value = material['roughness']
        
        # Connect to material output
        principled = nodes.get("Principled BSDF")
        mat.node_tree.links.new(color.outputs[0], principled.inputs[0])
        mat.node_tree.links.new(roughness.outputs[0], principled.inputs[7])
        
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
        """Generate a complete fall scene with variations"""
        try:
            self.setup_scene()
            model = self.load_model(model_path)
            
            if model is None:
                return False
            
            self.add_background_variation()  # Add background variation
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
        """Generate specified number of fall scenes with controlled variation"""
        model_files = list(self.model_dir.glob('*.fbx'))
        
        if not model_files:
            raise FileNotFoundError(f"No FBX files found in {self.model_dir}")
        
        # Generate specified number of videos
        successful = 0
        for i in range(self.num_videos):
            # Cycle through available models
            model_path = model_files[i % len(model_files)]
            output_path = self.output_dir / f"fall_scene_{i:03d}.mp4"
            
            print(f"Generating scene {i+1}/{self.num_videos}: {output_path}")
            if self.generate_scene(model_path, output_path):
                successful += 1
        
        print(f"Generation complete. Successfully generated {successful}/{self.num_videos} scenes.")
        print(f"Variation level: {self.variation_level}")