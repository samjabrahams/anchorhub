# AnchorHub Preemptively Answered Questions

---

[Readme](README.md#up) | [Table of Contents](CONTENTS.md#up) | [AnchorHub User Guide](GUIDE.md#up) | [AnchorHub Definitions](DEFINITIONS.md#up) | **FAQ** | [About AnchorHub](ABOUT.md#about-anchorhub) 

---

## Why Use AnchorHub?

GitHub automatically produces anchor tags for headers in Markdown files- they are great for linking directly to various sections of documentation, either within one document or across many documents. It's a great feature to have, as Markdown doesn't have a way to specify `id` tags on its own. However, using them isn't always a seamless experience. Their problem is twofold:

1. They are cumbersome to type out when the headers long
2. It is difficult to figure out what the auto-generated anchor will be when the header uses non-alphanumeric characters or if there are multiple headers with the same text

Because of these problems, people writing documentation on GitHub either have to double check, re-write documentation, and re-push to GitHub (squashing commits along the way) to make sure that their links work properly, or just not bother creating links in general. Screw that!

AnchorHub allows you to create virtual anchor tags using concise syntax, which will then compile out to the longer, auto-generated style used by GitHub. Easy peasy!

## What About ReStructuredText Support?

This is my first dive into creating a Python package, and I discovered that, ironically, the preferred text format in the Python community is [ReStructuredText](http://docutils.sourceforge.net/rst.html)! Whoops. After I refactor some code and make certain pieces a bit more modular, I hope to add in .rst support.

## Can You Add Support for Non-GitHub Style Header Anchors?

Definitely! I am planning on defining a interface for people to write their own anchor-generation styles, but if there are particular anchor-generation styles (perhaps from other git-hosting sites) that you think would be beneficial to have as a built-in option, feel free to submit an issue or pull-request!

## Why Load Files Into Memory Instead of Just Reading from Stream?

The prototype implementation of AnchorHub did read from stream, but it proved to be too inflexible. In order to allow for more possibilities for checking various types of syntax, I decided that reading the entire file into memory and allowing individual parsing functions decide which lines they needed would be best. Since AnchorHub is designed for text files that are human readable, I assume that users won't pass multiple gigabyte files to it.

---

[Back to top](#anchorhub-preemptively-answered-questions)