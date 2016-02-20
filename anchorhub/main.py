"""
Command-line entry to AnchorHub, main method is here.
"""

import anchorhub.cmdparse as cmdparse
import anchorhub.messages as messages
import anchorhub.normalization.normalize_opts as normalize_opts
import anchorhub.validation.validate_opts as validate_opts
import anchorhub.validation.validate_files as validate_files
from anchorhub.util.getfiles import get_files
from anchorhub.builtin.github.collector import make_github_markdown_collector
from anchorhub.builtin.github.writer import make_github_markdown_writer


def main(argv=None):
    """
    Main entry method for AnchorHub. Takes in command-line arguments,
    finds files to parse within the specified input directory, and outputs
    parsed files to the specified output directory.

    :param argv: a list of string command line arguments
    """
    # Get command line arguments, validate them, and normalize them
    opts = cmdparse.parse_args(argv)
    assert validate_opts.validate(opts)
    opts = normalize_opts.normalize(opts)

    if opts.verbose:
        # Update client: print input and output directories
        messages.print_directories(opts)

    file_paths = get_files(opts.abs_input, opts.extensions,
                           exclude=[opts.abs_output])
    assert validate_files.validate(file_paths, opts)

    if opts.verbose:
        # Update client: print files that will be parsed
        messages.print_files(opts, file_paths)

    # For now, only using default GitHub Markdown for parsing
    # Collect tag/anchor combinations
    collector = make_github_markdown_collector(opts)
    anchors, duplicate_tags = collector.collect(file_paths)

    # Write
    writer = make_github_markdown_writer(opts)
    counter = writer.write(file_paths, anchors, opts)

    if opts.verbose:
        # Update client: print files that had modifications
        messages.print_modified_files(opts, anchors)

        # Print summary statistics
        messages.print_summary_stats(counter)

if __name__ == '__main__':
    main()