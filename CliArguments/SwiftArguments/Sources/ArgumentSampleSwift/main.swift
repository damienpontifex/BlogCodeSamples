import Commander

let main = command(
    Flag("verbose", description: "Enable verbose output"),
    Option<String>("url", "", description: "Url argument")
) { verbose, url in
    print("Verbose: \(verbose)")
    print("URL: \(url)")
}
main.run()
