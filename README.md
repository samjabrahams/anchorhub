![AnchorHub graphic](http://cdn.rawgit.com/samjabrahams/anchorhub/master/img/graphic.svg)

# AnchorHub

Easily utilize GitHub's automatically generated permalinks within and across Markdown documents. It's like having `id` tags for your Markdown!

## Features

* Easily link to sections of Markdown documents on GitHub
* Simple, customizable syntax that just works
* Works within the entire directory tree automatically

---

## Quick Illustration

```markdown
What you write:
# This is a header that I would like to make an id for {#head}
[This link points to that header!](#head)

What AnchorHub outputs:
# This is a header that I would like to make an id for
[This link points to that header!](#this-is-a-header-that-i-would-like-to-make-an-id-for)
```

## How to Use

1. Place identifiers at end of header lines you'd like to reference inside of a Markdown file
	* Default format is `{#id-goes-here}`
2. Create links as you would any other Markdown link, using created identifiers
	* Example: `[This is my link](#id-goes-here)`
3. Run `anchorhub` in the directory root you'd like to process
4. Enjoy not having to deal with GitHub's anchor generation yourself!

## Running AnchorHub

By default, `anchorhub.py` runs in the current directory, and outputs to `./anchorhub-out`. Currently, users have to explicitly type the directory they'd like to input/output to if they want to use different settings from these, but command-line argument support is one of the top priorities in development.

`anchorhub.py` does not process files in the output directory.

## Examples

### Single file

#### Input
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

#### Output

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

### Multi-file

#### Input

file1.md

```markdown
# Some header for this file {#go-here}
[Link to another file's header](dir/file2.md#awesome)
```

dir/file2.md

```markdown
# The awesome header in file2.md {#awesome}
[Link back to file1.md](../file1.md#go-here)
```

#### Output

file1.md

```markdown
# Some header for this file 
[Link to another file's header](dir/file2.md#the-awesome-header-in-file2md)
```

dir/file2.md

```markdown
# The awesome header in file2.md 
[Link back to file1.md](../file1.md#some-header-for-this-file)
```

## To-do list

* Support for reference-style Markdown links
* Command line argument support
* Verify cross-platform compatibility (currently only tested on OSX)
* Proper exception handling
* Support for ReStructuredText
* Support for arbitrary generated anchor styles (not just GitHub-style)
* Clean, refactor, reorganize
* More tests!

## License

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