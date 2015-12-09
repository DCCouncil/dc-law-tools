# dc-law-tools

This repo contains tools for processing the dc-law.

The files in this repo will change significantly over time as our tooling needs change.

https://github.com/dccouncil/dc-law has issue tracker and full readme.

## requirements

In order to run the scripts in this repo, you must have python3  and pip installed.

## installation

from the `dc-law-tools` directory run `pip install .`

## build commands

* `./process_annotations.py`: runs all the following commands (which can be run individually)
    * `./process_xml_jobs/insert_tables.py`: insert hand-made tables into parsed xml.
    * `./process_annotations`: convert annotations into computer-readable structured data (wip)
    * `split_up.py`: split the single xml document into a file for each title, and each section, with link between. The split-up code is placed in a `../dc-law-xml` (a sibling to this directory)

## License

This software is released under a CC0 license.
