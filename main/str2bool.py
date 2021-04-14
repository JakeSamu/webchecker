import sys
import argparse

# Allow several arguments besides True and False
def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1', 'yy', ''):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0', 'nn'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')
