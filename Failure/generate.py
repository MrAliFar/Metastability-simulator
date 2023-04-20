import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser
    parser.add_argument_group('General')
    parser.add_argument('--num_failures',
                        type=int,
                        required=True,
                        help='The number of failures')
    parser.add_argument()