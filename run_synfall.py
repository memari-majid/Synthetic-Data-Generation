import argparse
import sys
import bpy

def parse_args():
    argv = sys.argv[argv.index("--") + 1:] if "--" in sys.argv else []

    parser = argparse.ArgumentParser(description='Generate synthetic fall detection videos')
    parser.add_argument('--model-dir', type=str, required=True, help='Directory containing FBX models')
    parser.add_argument('--output-dir', type=str, required=True, help='Directory for output videos')
    parser.add_argument('--quality', type=str, default='tiny', choices=['tiny', 'small', 'medium'],
                        help='Video quality preset')
    parser.add_argument('--num-videos', type=int, default=10,
                        help='Number of videos to generate')
    parser.add_argument('--variation', type=str, default='medium',
                        choices=['minimal', 'low', 'medium', 'high'],
                        help='Level of variation in generated videos')
    parser.add_argument('--resolution', type=int, nargs=2, help='Custom resolution (width height)')
    
    return parser.parse_args(argv)

if __name__ == "__main__":
    args = parse_args()
    
    from synthetic_fall_generator import SyntheticFallGenerator
    
    # Initialize generator with new options
    generator = SyntheticFallGenerator(
        model_dir=args.model_dir,
        output_dir=args.output_dir,
        quality=args.quality,
        num_videos=args.num_videos,
        variation_level=args.variation
    )
    
    if args.resolution:
        generator.resolution = tuple(args.resolution)
    
    generator.generate_dataset() 