# dc-law-tools

This repo contains tools for processing the dc-law.

The files in this repo will change significantly over time as our tooling needs change.

https://github.com/dccouncil/dc-law has issue tracker and full readme.

## requirements

 * In order to run the scripts in this repo, you must have python3 and pip installed.
 * Ensure you have the following directory structure:

```
|- root directory
  |- dc-law-tools
  |- dc-law-xml
  |- dc-law-html
```

### Linux

On Ubuntu Linux, be sure to install `python3` and `python3-dev` (required for
the `lxml` module). You'll also need to install a recent verson of `pip` if the
system version is too old; see the [pip installation page](https://pip.pypa.io/en/stable/installing/).

Alternatively, use a packaged Python distribution like [Miniconda](http://conda.pydata.org/miniconda.html)
to handle dependencies.

Some uses of `python` or `pip` in these instructions may need to be changed to
`python3` and `pip3`.

## installation

from the `dc-law-tools` directory run `pip install -r requirements.txt`

## build commands

Ensure that directories named `dc-law-xml` and `dc-law-html` exist under the
same parent directory as the `dc-law-tools` project; the files created in the
steps below will be put into those directories (clobbering any existing files).

* `build html all`: build the dc code html by sequentially running all the follow commands:
	* `build html merge_xml`: resolve all xml references; turn into one single xml document
	* `build html preprocess_xml`: run expensive operations once and cache where needed in the xml document
	* `build html template_xml`: repeatedly apply the xslt template to the single xml document to create the entire html site.
* `build xml all`: process the raw xml parsed from the Publisher, convert to something we can use to build the html. Sequentially runs all the following commands: 
    * `build xml insert_t1_ch15`:
    * `build xml insert_tables`: insert hand-made tables into parsed xml.
    * `build xml insert_placeholders`:
    * `build xml process_annotations`: convert annotations into computer-readable structured data (wip)
    * `build xml add_refs`:
    * `build xml split_up`: split the single xml document into a file for each title, and each section, with link between. The split-up code is placed in a `../dc-law-xml` (a sibling to this directory)

## License

This software is released under a CC0 license.
