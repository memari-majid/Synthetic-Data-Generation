import bpy
import random
import os
import math
from pathlib import Path

class FallSceneGenerator:
    def __init__(self, model_dir, output_dir, resolution=(320, 240)):
        self.model_dir = Path(model_dir)
        self.output_dir = Path(output_dir)
        self.resolution = resolution
        
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
        bpy.ops.import_scene.fbx(filepath=str(filepath))
        model = bpy.context.selected_objects[0]
        model.name = "Human"
        model.location.z = 0.1  # Slightly above ground
        return model
        
    def apply_fall_animation(self):
        """Configure the fall animation settings"""
        model = bpy.data.objects["Human"]
        armature = [obj for obj in model.children if obj.type == 'ARMATURE'][0]
        bpy.context.view_layer.objects.active = armature
        
        # Randomize animation speed
        bpy.context.scene.render.fps = random.choice([24, 30, 60])
        
    def adjust_camera(self):
        """Randomize camera position and angle"""
        camera = bpy.data.objects["Camera"]
        camera.location.x = random.uniform(-2, 2)
        camera.location.y = random.uniform(-8, -6)
        camera.location.z = random.uniform(4, 6)
        camera.rotation_euler = (
            random.uniform(1.0, 1.2),
            random.uniform(-0.1, 0.1),
            random.uniform(-0.1, 0.1)
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
        
    def setup_render_settings(self, output_path):
        """Configure render settings for video output"""
        scene = bpy.context.scene
        scene.render.image_settings.file_format = 'FFMPEG'
        scene.render.ffmpeg.format = 'MPEG4'
        scene.render.ffmpeg.codec = 'H264'
        scene.render.filepath = str(output_path)
        scene.render.resolution_x, scene.render.resolution_y = self.resolution
        scene.render.film_transparent = True
        scene.render.ffmpeg.constant_rate_factor = 'HIGH'  # Lower quality for realistic footage
        
    def add_noise(self):
        """Add noise to simulate real camera footage"""
        scene = bpy.context.scene
        scene.use_nodes = True
        nodes = scene.node_tree.nodes
        
        # Add noise node
        noise_node = nodes.new(type="CompositorNodeDenoise")
        render_layers = nodes["Render Layers"]
        composite = nodes["Composite"]
        
        # Connect nodes
        scene.node_tree.links.new(render_layers.outputs[0], noise_node.inputs[0])
        scene.node_tree.links.new(noise_node.outputs[0], composite.inputs[0])
        
    def generate_scene(self, model_path, output_path):
        """Generate a complete fall scene"""
        self.setup_scene()
        self.load_model(model_path)
        self.apply_fall_animation()
        self.adjust_camera()
        self.adjust_lighting()
        self.add_noise()
        self.setup_render_settings(output_path)
        bpy.ops.render.render(animation=True)
        
    def generate_dataset(self):
        """Generate multiple fall scenes from available models"""
        model_files = list(self.model_dir.glob('*.fbx'))
        
        if not model_files:
            raise FileNotFoundError(f"No FBX files found in {self.model_dir}")
            
        for i, model_path in enumerate(model_files):
            output_path = self.output_dir / f"fall_scene_{i}.mp4"
            print(f"Generating scene {i+1}/{len(model_files)}: {output_path}")
            self.generate_scene(model_path, output_path) 