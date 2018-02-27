#!/usr/bin/env python
"""
Merge multiple JUnit XML files into a single results file. See `def usage()`.
"""
# Edited from https://gist.github.com/cgoldberg/4320815
import os
import sys
import xml.etree.ElementTree as ET


def main():
    args = sys.argv[1:]
    if not args:
        usage()
        sys.exit(2)
    if '-h' in args or '--help' in args:
        usage()
        sys.exit(2)
    output_file = args[0]
    merge_results(output_file, args[1:])


def merge_results(output_file, xml_files):
    failures = 0
    tests = 0
    errors = 0
    time = 0.0
    cases = []

    for file_name in xml_files:
        if not os.path.exists(file_name):
            print("{} not found. Continue...".format(file_name))
            continue
        print("{} found. Parsing...".format(file_name))

        tree = ET.parse(file_name)
        test_suite = tree.getroot()
        failures += int(test_suite.attrib['failures'])
        tests += int(test_suite.attrib['tests'])
        errors += int(test_suite.attrib['errors'])
        time += float(test_suite.attrib['time'])
        cases.append(test_suite.getchildren())

    new_root = ET.Element('testsuite')
    new_root.attrib['failures'] = '%s' % failures
    new_root.attrib['tests'] = '%s' % tests
    new_root.attrib['errors'] = '%s' % errors
    new_root.attrib['time'] = '%s' % time
    for case in cases:
        new_root.extend(case)
    new_tree = ET.ElementTree(new_root)
    new_tree.write(output_file, encoding="utf8")


def usage():
    this_file = os.path.basename(__file__)
    print('Usage: %s output.xml results1.xml results2.xml' % this_file)


if __name__ == '__main__':
    main()
