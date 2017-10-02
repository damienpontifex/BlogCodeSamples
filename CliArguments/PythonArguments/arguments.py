#!/usr/bin/env python3

if __name__ == '__main__':
    from argparse import ArgumentParser
    
    parser = ArgumentParser(description='Sample tool')
    parser.add_argument('-v', '--verbose', 
                        help='Enable verbose output', 
                        action='store_true')
    parser.add_argument('-u', '--url',
                        help='Url argument',
                        required=True)
    
    args = parser.parse_args()
    
    print(f'Verbose: {args.verbose}')
    print(f'URL: {args.url}')
