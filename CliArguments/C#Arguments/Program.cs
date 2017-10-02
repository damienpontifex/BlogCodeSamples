using System;
using Microsoft.Extensions.CommandLineUtils;

namespace ArgumentSample
{
    class Program
    {
        static void Main(string[] args)
        {
            var app = new CommandLineApplication();
            app.Name = "Sample tool";
            app.HelpOption("-h|--help");

            var verboseOption = app.Option("-v|--verbose", "Enable verbose output", CommandOptionType.NoValue);
            var urlOption = app.Option("-u|--url", "Url argument", CommandOptionType.SingleValue);

            app.OnExecute(() => {
                Console.WriteLine($"Verbose: {verboseOption.HasValue()}");
                Console.WriteLine($"URL: {urlOption.Value()}");

                return 0;
            });

            app.Execute(args);
        }
    }
}
