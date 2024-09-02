# Create Rekordbox Playlists

## Description

This Python project can:
1. Parse .pls files (either a filepath or directory path may be passed)
1. Determine which files need to be converted for use with Pioneer CDJs
1. Perform the conversion and export the converted file
1. Write tags to exported files
1. Fix enhanced multichannel audio files to work with Pioneer CDJs
1. Create and export an updated playlist for import to Rekordbox

## Installation

The Makefile at the root of this project has an init step to install requirements

## Usage

`python main.py {PATH} {CONVERTED_FILES_PATH} {EXPORTED_PLAYLISTS_PATH}`

## Support

Cormac Geraghty

[Cormac1902@hotmail.com](mailto:Cormac1902@hotmail.com)

## Roadmap

1. Add unit tests
1. Refactor to use Strategy and Flyweight patterns for conversion algorithms
1. Add support for Ogg files
1. Benchmark and improve parallelism
1. Investigate caching information about already-processed files and only updating tags/fixing enhanced multichannel audio where necessary
