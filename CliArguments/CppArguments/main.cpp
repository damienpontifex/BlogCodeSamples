#include <iostream>
#include <getopt.h>

#define NO_ARGUMENT 0
#define REQUIRED_ARGUMENT 1
#define OPTIONAL_ARGUMENT 2

void print_help()
{
    std::cout << "usage: SampleTool [-h] [-v] -u URL\n\n
    Sample tool\n\n
    optional arguments:\n
      -h, --help         show this help message and exit\n
      -v, --verbose      Enable verbose output\n
      -u URL, --url URL  Url argument\n";
    exit(1);
}

int main(int argc, char * argv[])
{
    bool verbose = false;
    std::string url = nullptr;

    const char* const short_opts = ":hvu";
    const option long_opts[] = {
        { "help", OPTIONAL_ARGUMENT, nullptr, 'h' },
        { "verbose", OPTIONAL_ARGUMENT, nullptr, 'v' },
        { "url", REQUIRED_ARGUMENT, nullptr, 'u' }
    };

    while((const auto opt = getopt_long(argc, argv, short_opts, long_opts, nullptr)) != -1)
    {
        switch (opt)
        {
        case 'v':
            verbose = true;
            break;
        case 'u':
            url = std::string(optarg);
            break;
        case 'h':
        case '?':
        default:
            print_help();
            break;
        }
    }

    std::cout << "Verbose: " << verbose << std::endl;
    std::cout << "URL: " << url << std::endl;

    return 0;
}