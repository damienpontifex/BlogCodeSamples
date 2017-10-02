#!/usr/bin/env bash

VERBOSE=false
URL=

function usage()
{
    echo "Usage: arguments [-h] [-v] -u URL"
    echo "\nSample tool"
    echo "\nOptional arguments:"
    echo "  -h, --help          show this help message and exit"
    echo "  -v, --verbose       Enable verbose output"
    echo "  -u URL, --url URL   Url argument"
}

OPTS=$(getopt -o :hvu: --long help,verbose,url: -n 'parse-options' -- "$@")

while true; do
    case "$1" in
        -h|--help) usage(); exit 0;;
        -v|--verbose) VERBOSE=true; shift ;;
        -u|--url) URL="$2"; shift; shift ;;
        --) shift; break ;;
        * ) break ;;
    esac
done

echo "Verbose: $VERBOSE"
echo "URL: $URL\n"
