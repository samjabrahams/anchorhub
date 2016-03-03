# AnchorHub User Guide {#up}

[Readme](README.md#up) | [Table of Contents](CONTENTS.md#up) | **AnchorHub User Guide** | [AnchorHub Definitions](DEFINITIONS.md#up) | [FAQ](FAQ.md#up) | [About AnchorHub](ABOUT.md#up) 

This guide goes over how to write your Markdown files in order to utilize AnchorHub, as well as how to use the command-line interface to AnchorHub.

1. [Defining anchors on header lines](#headers)
2. [Using those anchors in links](#links)
3. [The command line interface](#cli)
4. [Examples](#examples)

## Defining AnchorHub Tags {#tags}

Place identifiers with a leading '#' inside of `{ }` wrappers at end of header lines you'd like to reference. For example:

```markdown
# This is the header I'd like to create an anchor for {#head}
```

_Note: You can specify your own style of wrapper syntax if `{ }` braces don't suit your needs. [See below](#wrapper) for an example._

## Link Syntax {#links}

Write links to your specified anchors as if you had created an HTML element with an `id` or `name` parameter:

```markdown
In the middle of this sentence, I'd like to link back to [the header specified above](#head)
```

AnchorHub automatically automatically works for all files within a directory tree, so if you had a file named 'other.md' with '#ref' defined as an anchor, you can link to it from your original file without any additional effort:

```markdown
Let's link to that [other file's anchor!](other.md#ref)
```

_Note: If your input references AnchorHub tags in files that are in a different directory, make sure that you use the `-r` flag when processing your files. [See below](#recursive) for details._

## AnchorHub's Command Line Interface {#cli}

### Usage {#usage}

```shell
anchorhub [-h] [-v] [-X] [-e EXTENSIONS [EXTENSIONS ...]] [-w WRAPPER] input [output]
```

### Input {#input}

The only required argument to `anchorhub` is the desired input. The input can either be a single file or a directory.

```shell
$ anchorhub path/to/my/input

$ anchorhub myfile.md
```

### Output {#output}

The second argument, if provided, specifies the desired output directory. By default, AnchorHub will output to the directory `anchorhub-out` within the present working directory, creating it if necessary. Regardless of where the output is located, the structure of the output directory will match that of the input directory.

```shell
$ anchorhub input path/to/my/output
```


### Options {#options}

---

#### Help {#help}

**-h / --help:** Display the terminal help prompt for `anchorhub`

```shell
$ anchorhub -h
```

---

#### Display version information {#version}

**--version:** Display the installed version of `anchorhub`

```shell
$ anchorhub -v
```

---

#### Parse all subdirectories, recursively {#recursive}

**-r / -R:** Parse all files in the current directory, including all subdirectories (recursively)

Use this flag to parse all files in the input directory, including subdirectories. AnchorHub will not move outside of the input directory while parsing, so make sure that the input is the highest-level directory which contains all files you want to parse.

Links that point to AnchorHub tags in other files within the directory hierarchy will work as intended.

```
$ anchorhub input -r
```

---

#### Generate verbose output {#verbose}

**-v, --verbose:** When running AnchorHub, print verbose information to the console

When this flag is used, the following information is printed as AnchorHub parses:

* The input path
* The output path
* The list of files that will be parsed
* The list of files that contained AnchorHub tags
* A count of modifications made during parsing

```
$ anchorhub input -v

Root input directory:	input/
Outputting to:		anchorhub-out/

Parsing the following files:
  example.md
--------------------
1 total

Files with modifications:
  example.md
--------------------
1 total

Total ATX headers modified:		2
Total inline links modified:	2
Total modifications: 			4
```

---

#### Overwrite input files {#overwrite}

**-X / --overwrite:** Instead of outputting to a separate directory, overwrite the input files

```shell
$ anchorhub -X input
```

---

#### Specify which file extensions to parse {#extensions}

**-e / --extension EXTENSIONS [EXTENSIONS ...]:** Process files that end with the provided extensions

The default value is `".md .markdown"`. You can provide multiple extensions if you have files that use various extensions.

The following would cause anchorhub to look for files that end with '.md', '.markdown', '.MD', or '.txt'

```shell
$ anchorhub input -e .md .markdown .MD .txt
```

Since the `-e` flag takes an arbitrary number of parameters, make sure you declare it _after_ specifying the input (and output, if desired):

```
Don't do this!
$ anchorhub -e .md .markdown input output
```

---

#### Specify a wrapper syntax {#wrapper}

**-w / --wrapper:** Specify the wrapper syntax for defining anchors

The default value is `"{ }"`. Make sure you have a space between your opening and closing patterns and to wrap the whole thing in quotation marks:

As an example, the following would allow you to specify AnchorHub tags with the syntax `'[-->#tag<--]'`

```shell
$ anchorhub input -w "[--> <--]"
```

---

## Examples {#examples}

You can find a bunch of pre-written sample files in the [sample](sample) subdirectory. Below, I'll go over some of the examples and describe features of AnchorHub along the way.

---

### Single file {#ex1}

#### Input

example.md

```markdown
# This is the top of my document! {#top}
Going to have some more cool text explaining stuff.

Skip to features header with [this link!](#features).

## Here is my feature list! {#features}
* Gotta have some bullet points!
* Let's keep it up!
* This bullet point is here for the rule of three

[Link back to the top!](#top)
```

#### Command line

```
$ anchorhub example.md
```

#### Output

anchorhub-out/example.md

```markdown
# This is the top of my document! 
Going to have some more cool text explaining stuff.

Skip to features header with [this link!](#here-is-my-feature-list).

## Here is my feature list! 
* Gotta have some bullet points!
* Let's keep it up!
* This bullet point is here for the rule of three

[Link back to the top!](#this-is-the-top-of-my-document)
```

---

### Multi-file {#ex2}

When you input a directory to AnchorHub, it parses each file in that directory. Because of this, you can link to other documents in the same way you would as linking within a page. Each file has its own distinct set of anchors, so you can reuse the same tags on different pages. Here's a super simple demonstration below:

#### Input

file1.md

```markdown
# Some header for this file {#go-here}
[Link to another file's header](file2.md#awesome)
```

file2.md

```markdown
# The awesome header in file2.md {#awesome}
[Link back to file1.md](file1.md#go-here)
```

#### Command line

```
$ anchorhub .
```

#### Output

anchorhub-out/file1.md

```markdown
# Some header for this file 
[Link to another file's header](file2.md#the-awesome-header-in-file2md)
```

anchorhub-out/file2.md

```markdown
# The awesome header in file2.md 
[Link back to file1.md](file1.md#some-header-for-this-file)
```

---

[Back to top](#up)