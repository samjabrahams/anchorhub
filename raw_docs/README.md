![AnchorHub graphic](img/graphic.png)

# AnchorHub {#up}

**AnchorHub** is a command-line tool that makes it easy and intuitive to utilize GitHub's auto-generated anchor tags in your [Markdown](https://daringfireball.net/projects/markdown/) documents, allowing you to create rich, user-friendly documentation in your GitHub repos without having to figure out what those auto-generated tags will be.

## Features {#features}

* Easily use GitHub's automatically generated anchor tags
* Simple, customizable syntax that just works
* Works with single files, a single directory level, or an entire directory tree

---

**Readme** | [Table of Contents](CONTENTS.md#up) | [AnchorHub User Guide](GUIDE.md#up) | [AnchorHub Definitions](DEFINITIONS.md#up) | [FAQ](FAQ.md#up) | [About AnchorHub](ABOUT.md#up) 

---

## Installation {#install}

You can install AnchorHub using [pip](https://pip.pypa.io/en/stable/installing/):

```
$ pip install anchorhub
```

If you're having trouble with pip, you can also install from source:

```
$ git clone https://github.com/samjabrahams/anchorhub.git
$ cd anchorhub
$ python setup.py install
```

## To-do List {#todos}

* Verify cross-platform compatibility (currently only tested on OSX)
* Support for ReStructuredText
* Define API for using custom anchor generation or 
* More tests!

## Known Issues {#bugs}

* Should not change text within in-line code blocks (those marked by \` backticks)

---

# Quick Start Guide {#quick}

## 1. Define your tags {#step1}

Inside your Markdown files, define tags at the end of header lines. By default, the syntax for this is `{#my-tag-here}`:


```markdown
# This is a header that I would like to make a tag for {#tag}

You can also use Setext (underlined) style headers {#setext}
------------------------------------------------------------
```

The default is similar to [Pandoc's Markdown header identifiers](http://pandoc.org/README.html#header-identifiers)

## 2. Use the tags as you would regular HTML anchors {#step2}

Elsewhere, you can use the previously defined tags inlinks to provide a direct path to the header:

```markdown
[This links back to the header using the AnchorHub tag 'tag'](#tag)

[This one links to the Setext header](#setext)
```

## 3. Run AnchorHub on your Markdown files {#step3}

`anchorhub` will parse your Markdown files. You've got a few options for running `anchorhub`: run it on a single file, run it on a single level of a directory, or run it on an entire directory tree.

```
Single file use:
$ anchorhub mytags.md

Directory use (single level):
$ anchorhub .

Directory use (provided directory level and all subdirectories):
$ anchorhub . -r
```

This will output your processed files in a new folder in your current directory, 'anchorhub-out/'

## 4. Enjoy your (relatively) hassle-free GitHub anchor links {#step4}
 
Assuming all of the above Markdown was in a file named 'mytags.md', here is what we'd find inside of 'anchorhub-out/mytags.md':

```markdown
# This is a header that I would like to make a tag for

You can also use Setext (underlined) style headers
------------------------------------------------------------
...
[This links back to the header using the AnchorHub tag 'tag'](#this-is-a-header-that-i-would-like-to-make-a-tag-for)

[This one links to the Setext header](#you-can-also-use-setext-underlined-style-headers)
```

---

# License {#license}

```
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
```

---

[Back to top](#up)