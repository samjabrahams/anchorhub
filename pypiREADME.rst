.. figure:: img/graphic.png
   :alt: AnchorHub graphic

   AnchorHub graphic

AnchorHub
=========

**AnchorHub** is a command-line tool that makes it easy and intuitive to
utilize GitHub's auto-generated anchor tags in your
`Markdown <https://daringfireball.net/projects/markdown/>`__ documents,
allowing you to create rich, user-friendly documentation in your GitHub
repos without having to figure out what those auto-generated tags will
be.

Features
--------

-  Easily link to sections of Markdown documents on GitHub
-  Simple, customizable syntax that just works
-  Works within the entire directory tree automatically

--------------

`Table of Contents <CONTENTS.md>`__ \| `FAQ <FAQ.md>`__ \| `About
AnchorHub <ABOUT.md>`__

--------------

Installation
------------

You can install AnchorHub using
`pip <https://pip.pypa.io/en/stable/installing/>`__:

::

    $ pip install anchorhub

Quick Start Guide
-----------------

Inside your Markdown files, define and use header anchors like the
following:

..

    # This is a header that I would like to make an id for {#head}
    [This link points to that header!](#head)

Navigate to the root of the directory tree you'd like to process and
type:

::

    $ anchorhub .

This will output your processed files in a new folder in your current
directory, 'anchorhub-out'. The output of AnchorHub on the Markdown
written above is this:

..

    # This is a header that I would like to make an id for
    [This link points to that header!](#this-is-a-header-that-i-would-like-to-make-an-id-for)

Using AnchorHub
===============

This section goes over how to write your Markdown files in order to
utilize AnchorHub, as well as how to use the command-line interface to
AnchorHub.

1. `Defining anchors on header lines <#defining-anchors>`__
2. `Using those anchors in links <#link-syntax>`__
3. `Processing files with the ``anchorhub`` command line
   interface <#anchorhubs-command-line-interface>`__

Defining Anchors
----------------

Place identifiers with a leading '#' inside of ``{ }`` wrappers at end
of header lines you'd like to reference. For example:

..

    # This is the header I'd like to create an anchor for {#head}

*Note: You can specify your own style of wrappers if ``{ }`` braces
don't suit your needs. `See below <>`__ for an example.*

Link Syntax
-----------

Write links to your specified anchors as if you had created an HTML
element with an ``id`` or ``name`` parameter:

..

    In the middle of this sentence, I'd like to link back to [the header specified above](#head)

AnchorHub automatically automatically works for all files within a
directory tree, so if you had a file named 'other.md' with '#ref'
defined as an anchor, you can link to it from your original file without
any additional effort:

.. code:: markdown

    Let's link to that [other file's anchor!](other.md#ref)

*Note: Make sure you use AnchorHub on the highest-level directory that
you'd like to process. AnchorHub will search in all sub-directories of
the input directory, but it will never step backwards. `See below <>`__
for details.*

AnchorHub's Command Line Interface
----------------------------------

Usage
~~~~~

..

    anchorhub [-h] [-v] [-X] [-e EXTENSIONS [EXTENSIONS ...]] [-w WRAPPER] input [output]

Input
~~~~~

The only required argument to ``anchorhub`` is the desired input root.
AnchorHub will walk through all subdirectories within the input and
process all Markdown files it finds.

..

    $ anchorhub path/to/my/input

Output
~~~~~~

The second argument, if provided, specifies the desired output
directory. By default, AnchorHub will output to ``anchorhub-out`` within
the present working directory. Regardless of where the output is
located, the structure of the output directory will match that of the
input directory.

..

    $ anchorhub input path/to/my/output

Options
~~~~~~~

**-h / --help:** Display the terminal help prompt for ``anchorhub``

..

    $ anchorhub -h

**-v / --version:** Display the installed version of ``anchorhub``

..

    $ anchorhub -v

**-X / --overwrite:** Instead of outputting to a separate directory,
overwrite the input files

..

    $ anchorhub -X ./input

**-e / --extension EXTENSION [EXTENSIONS ...]:** Process files that end
with the provided extensions

The default value is ``".md"``. You can provide multiple extensions if
you have files that use various extensions:

..

    $ anchorhub ./input -e .md .markdown .MD 

**-w / --wrapper:** Specify the wrapper syntax for defining anchors

The default value is ``"{ }"``. Make sure you have a space between your
opening and closing patterns and to wrap the whole thing in quotation
marks:

..

    $ anchorhub ./input -w "[--> <--]"

Additional Info
===============

Examples
--------

Single file
~~~~~~~~~~~

Input
^^^^^

..

    # This is the top of my document! {#top}
    Going to have some more cool text explaining stuff.

    Skip to features header with [this link!](#features).

    ## Here is my feature list! {#features}
    * Gotta have some bullet points!
    * Let's keep it up!
    * This bullet point is here for the rule of three

    [Link back to the top!](#top)

Output
^^^^^^

..

    # This is the top of my document! 
    Going to have some more cool text explaining stuff.

    Skip to features header with [this link!](#here-is-my-feature-list).

    ## Here is my feature list! 
    * Gotta have some bullet points!
    * Let's keep it up!
    * This bullet point is here for the rule of three

    [Link back to the top!](#this-is-the-top-of-my-document)

Multi-file
~~~~~~~~~~

AnchorHub automatically looks at the entire directory tree when checking
for anchor matches, so you can link to other documents in the same
fashion. Each file has its own distinct set of anchors, so you can reuse
the same tags on different pages. Here's a super simple demonstration
below:

Input
^^^^^

file1.md

..

    # Some header for this file {#go-here}
    [Link to another file's header](dir/file2.md#awesome)

dir/file2.md

..

    # The awesome header in file2.md {#awesome}
    [Link back to file1.md](../file1.md#go-here)

Output
^^^^^^

file1.md

..

    # Some header for this file 
    [Link to another file's header](dir/file2.md#the-awesome-header-in-file2md)

dir/file2.md

..

    # The awesome header in file2.md 
    [Link back to file1.md](../file1.md#some-header-for-this-file)

To-do List
----------

-  Support for reference-style Markdown links
-  Support for Setext ("underlined") style headers
-  Verify cross-platform compatibility (currently only tested on OSX)
-  Proper exception handling
-  Support for ReStructuredText
-  Support for arbitrary generated anchor styles (not just GitHub-style)
-  Clean, refactor, reorganize
-  More tests!

Known Issues
------------

-  Should not change text within in-line code (those marked by \`
   backticks)

License
-------

::

    Copyright 2016, Sam Abrahams. All rights reserved.

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

`Back to top <#anchorhub>`__
