# Aventail IOC Parser for Palo Alto XDR

This Python script parses Indicators of Compromise (IOCs) available from Aventail and generates automated Palo Alto XDR (Extended Detection and Response) XQL queries to identify these IOCs within an environment.

## Overview

The Aventail platform ([https://aventail.cyber.gc.ca/](https://aventail.cyber.gc.ca/)) provides a curated list of IOCs that may pose a threat to organizations. This script automates the process of parsing these IOCs and generating XQL queries compatible with Palo Alto's XDR platform to facilitate threat detection and response.

## Features

- Parses IOCs from Aventail and extracts relevant information.
- Generates automated Palo Alto XDR XQL queries based on the parsed IOCs.
- Supports IOCs in various formats, including IP addresses, domains, and URLs.
- Provides flexibility for integrating with existing security infrastructure.

## Dependencies
- Python 3
- argparse

## Usage

1. **Retrieve IOCs from Aventail**: Visit the Aventail platform ([https://aventail.cyber.gc.ca/](https://aventail.cyber.gc.ca/)) to obtain the latest list of IOCs.

2. **Run the script**: Execute the Python script, providing the path to the CSV file containing the IOCs obtained from Aventail as an argument.

   ```bash
   python ioc-to-xdr.py --file <path_to_csv>

