import argparse


def fetch_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, default="")  # input code location
    return parser.parse_args()
