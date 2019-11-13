#!/usr/bin/env python3

import sys
import subprocess
import argparse
import tempfile
import os, os.path

ap = argparse.ArgumentParser(description='Check margins of a PDF file.')
ap.add_argument('infile', help='input PDF file')
ap.add_argument('-m', '--margin', metavar='DIM', help='minimum margin on all sides')
ap.add_argument('-t', '--top', metavar='DIM', help='minimum top margin')
ap.add_argument('-r', '--right', metavar='DIM', help='minimum right margin')
ap.add_argument('-b', '--bottom', metavar='DIM', help='minimum bottom margin')
ap.add_argument('-l', '--left', metavar='DIM', help='minimum left margin')
args = ap.parse_args()

def parse_dim(s):
    """Convert to inches."""
    s = s.rstrip()
    if s.endswith('cm'):
        return float(s[:-2]) / 2.54
    elif s.endswith('in'):
        return float(s[:-2])
    else:
        raise ValueError('unknown units: {}'.format(s))

top = right = bottom = left = 0
if args.margin is not None:
    m = parse_dim(args.margin)
    top = max(top, m)
    right = max(right, m)
    bottom = max(bottom, m)
    left = max(left, m)
if args.top is not None: 
    top = max(top, parse_dim(args.top))
if args.right is not None: 
    right = max(right, parse_dim(args.right))
if args.bottom is not None: 
    bottom = max(bottom, parse_dim(args.bottom))
if args.left is not None: 
    left = max(left, parse_dim(args.left))

dpi = 75

with tempfile.TemporaryDirectory() as tmpdir:

    try:
        proc = subprocess.run(['pdftoppm', '-gray', '-r', str(dpi), args.infile, tmpdir + '/page'])
    except KeyboardInterrupt:
        raise
    except Exception:
        sys.stderr.write("error: could not run pdftoppm\n")
        raise

    if proc.returncode != 0:
        sys.stderr.write("error: pdftoppm returned nonzero exit code\n")
        exit(1)

    pages = {}
    for fn in os.listdir(tmpdir):
        page = int(fn[-10:-4]) # filename is of the form page-nnnnnn.pgm
        pages[page] = fn

    for page in sorted(pages):
        fn = pages[page]
        with open(os.path.join(tmpdir, fn), "rb") as f:
            magic = f.readline().strip()
            if magic != b"P5":
                sys.stderr.write("error: expected pdftoppm to output PGM format\n")
                continue
            dims = f.readline()
            width, height = map(int, dims.split())
            white = int(f.readline())
            data = f.read()
            error = False

            if top > 0 and any(v < white for v in data[:int(top*dpi*width)]):
                print("page {} exceeds top margin".format(page))
                error = True
            if bottom > 0 and any(v < white for v in data[-int(bottom*dpi*width):]):
                print("page {} exceeds bottom margin".format(page))
                error = True
            if left > 0 and any(v < white for y in range(height) 
                             for v in data[y*width:y*width+int(left*dpi)]):
                print("page {} exceeds left margin".format(page))
                error = True
            if right > 0 and any(v < white for y in range(height) 
                             for v in data[(y+1)*width-int(right*dpi):(y+1)*width]):
                print("page {} exceeds right margin".format(page))
                error = True

    if error:
        exit(1)
    else:
        exit(0)
