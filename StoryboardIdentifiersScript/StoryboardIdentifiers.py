#!/usr/bin/env python

import sys, os
import xml.etree.ElementTree as et

segueIdentifiers = {}
controllerIdentifiers = {}
reuseIdentifiers = {}


def addSegueIdentifier(identifier):
    key = identifier[0].upper() + identifier[1:]

    segueIdentifiers[key] = identifier


def addControllerIdentifier(identifier):
    key = identifier[0].upper() + identifier[1:]

    controllerIdentifiers[key] = identifier


def addReuseIdentifier(identifier):
    key = identifier[0].upper() + identifier[1:]

    reuseIdentifiers[key] = identifier


def process_storyboard(file):
    tree = et.parse(file)
    root = tree.getroot()

    for segue in root.iter("segue"):
        segueIdentifier = segue.get("identifier")
        if segueIdentifier == None:
            continue
        addSegueIdentifier(segueIdentifier)

    for controller in root.findall(".//*[@storyboardIdentifier]"):
        controllerIdentifier = controller.get("storyboardIdentifier")
        if controllerIdentifier == None:
            continue
        addControllerIdentifier(controllerIdentifier)

    for cell in root.findall(".//*[@reuseIdentifier]"):
        reuseIdentifier = cell.get("reuseIdentifier")
        if reuseIdentifier == None:
            continue
        addReuseIdentifier(reuseIdentifier)


def writeSwiftFile(file, identifiers, structName):
    constants = sorted(identifiers.keys())

    file.write("public struct " + structName + " {\n")

    for constantName in constants:
        file.write("\tpublic static let " + constantName + " = \"" + identifiers[constantName] + "\"\n")

    file.write("}")


count = os.environ["SCRIPT_INPUT_FILE_COUNT"]
for n in range(int(count)):
    process_storyboard(os.environ["SCRIPT_INPUT_FILE_" + str(n)])

with open(os.environ["SCRIPT_OUTPUT_FILE_0"], "w+") as swiftFile:
    swiftFile.write("/* Generated document. DO NOT CHANGE */\n\n")
    writeSwiftFile(swiftFile, segueIdentifiers, "Segue")
    swiftFile.write("\n\n")

    writeSwiftFile(swiftFile, controllerIdentifiers, "Controller")
    swiftFile.write("\n\n")

    writeSwiftFile(swiftFile, reuseIdentifiers, "Reuse")
    swiftFile.write("\n")

    swiftFile.close()
