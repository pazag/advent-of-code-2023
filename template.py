


# Standard library import
import argparse
import logging
import os


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="File to parse")

    args = parser.parse_args()
    if not os.path.exists(args.filename):
        logging.error(f"File {args.filename} does not exist.")



if __name__ == "__main__":
    main()