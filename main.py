import sys
from pathlib import Path
from argparse import ArgumentParser

import imagesize  # finds the size without loading the whole image


def positive_float(string):
    v = float(string)
    if v <= 0:
        raise ValueError('value cannot be negative')
    return v


def nonneg_int(string):
    v = int(string)
    if v < 0:
        raise ValueError('value cannot be negative')
    return v


def posi_int(string):
    v = int(string)
    if v <= 0:
        raise ValueError('vaue must be positive')
    return v


def existing_path(string):
    path = Path(string)
    if not path.exists():
        raise ValueError('path does not exist')
    return path


def unoccupied_file_valid_path(string):
    path = Path(string)
    if path.is_file():
        raise ValueError('path is occupied')
    if not path.parent.exists():
        raise ValueError('directory does not exist')
    return path


def get_parser() -> ArgumentParser:
    parser = ArgumentParser(description='Crops long images and compiles them to a pdf.', add_help=False)
    parser.add_argument('--help', action='help', help='Show this help message and exit.')

    parser.add_argument('--width', '-w',        nargs=1,    type=posi_int,      default=None,
            required=False, help='Width of each page including the margins. '
            'If omitted, program will try to find and use the maximum width among all inputs plus left and right margins.')
    parser.add_argument('--margins', '-m',      nargs=4,    type=nonneg_int,    default=[72, 72, 72, 72],
            required=False, help='Margins of pages, default to 72.', metavar=('TOP', 'RIGHT', 'BOTTOM', 'LEFT'))
    parser.add_argument('--ratio', '-r',        nargs=1,    type=posi_int,      default=1.294,
            required=False, help='Aspect ratio measured by dividing height by width, '
            'defaults to 11.294, the ratio of ANSI Letter.')
    parser.add_argument('--height', '-h',       nargs=1,    type=posi_int,      default=None,
            required=False, help='Height of each page including the margins. '
            'Can be used instead of ratio and takes precedence over it.')
    parser.add_argument('--height-tolerance', '-t', nargs=1,    type=posi_int,      default=0.65,
            required=False, help='Minimum percentage of the height each page can be cut into, '
            'defaults to 11.')
    parser.add_argument('--locality', '-l',     nargs=1,    type=posi_int,      default=11,
            required=False, help='Range of neighboring pixels considered when cutting pages, '
            'defaults to 11. 1 means no locality and only considering the current pixel; '
            'while 11 means a all pixels within a 11x11 box centered at each pixel.')

    parser.add_argument('input',                            type=existing_path,
            help='Input image or directory of input images.'
            'If a directory is used, the ordering depends on file name.')
    parser.add_argument('output',                           type=unoccupied_file_valid_path,
            help='Path of the compiled pdf, cannot occupied.')
    return parser



def main():
    args = get_parser().parse_args(sys.argv[1:])
    args.input: list[Path] = [p for p in args.input.iterdir()] if args.input.is_dir() else [args.input]
    args.input.sort(key=lambda x: str(x))
    if args.width is None:
        args.width = max(imagesize.get(str(p))[0] for p in args.input) + args.margins[1] + args.margins[3]
    if args.height is None:
        args.height = int(args.width * args.ratio)
    
    return

   
if __name__ == '__main__':
    main()
