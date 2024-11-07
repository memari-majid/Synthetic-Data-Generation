import argparse
import sys
import bpy

def parse_args():
    # Get all args after "--"
    argv = sys.argv
    if "--" not in argv:
        argv = []
    else:
        argv = argv[argv.index("--") + 1:]

    parser = argparse.ArgumentParser(description='Generate synthetic fall detection videos using Blender')
    parser.add_argument('--model-dir', type=str, required=True, help='Directory containing FBX models')
    parser.add_argument('--output-dir', type=str, required=True, help='Directory for output videos')
    parser.add_argument('--resolution', type=int, nargs=2, default=[320, 240], help='Video resolution (width height)')
    
    return parser.parse_args(argv)

if __name__ == "__main__":
    args = parse_args()
    
    from synthetic_fall_generator import SyntheticFallGenerator
    
    generator = SyntheticFallGenerator(
        model_dir=args.model_dir,
        output_dir=args.output_dir,
        resolution=tuple(args.resolution)
    )
    
    generator.generate_dataset() 