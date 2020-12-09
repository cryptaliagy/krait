#!/bin/bash

gitchangelog $(python scripts/extract_version.py)..HEAD
