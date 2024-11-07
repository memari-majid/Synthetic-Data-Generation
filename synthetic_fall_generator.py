class SyntheticFallGenerator:
    """Generator for synthetic fall detection videos using Blender"""
    def __init__(self, model_dir, output_dir, resolution=(320, 240)):
        self.model_dir = Path(model_dir)
        self.output_dir = Path(output_dir)
        self.resolution = resolution
        
        # Create output directory if it doesn't exist
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    # [Rest of the class implementation remains the same] 