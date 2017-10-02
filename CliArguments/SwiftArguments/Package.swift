// swift-tools-version:4.0
// The swift-tools-version declares the minimum version of Swift required to build this package.

import PackageDescription

let package = Package(
    name: "ArgumentSampleSwift",
    dependencies: [
        .package(url: "https://github.com/kylef/Commander.git", from: "0.7.1")
    ],
    targets: [
        .target(
            name: "ArgumentSampleSwift",
            dependencies: ["Commander"]),
    ]
)
