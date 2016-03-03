# Terminology/Definitions {#up}

[Readme](README.md) | [Table of Contents](CONTENTS.md) | [AnchorHub User Guide](GUIDE.md) | **AnchorHub Definitions** | [FAQ](FAQ.md) | [About AnchorHub](ABOUT.md) 

## AnchorHub tags {#tags}

Or 'tags' for short. These are the user-defined text strings that are surrounded by a 'wrapper' (curly braces {} by default)

For example, in this line:

```markdown
# Such a cool header here! {#cool}
```

'#cool' is the AnchorHub tag. Note that every AnchorHub tag _must_ start with a `#` hash inside of the defined wrapper.

## Auto-generated anchors {#anchors}

or 'anchors' for short. These are text strings that are converted from the existing file to be used as anchor links in rendered HTML. Each AnchorHub tag is associated with an auto-generated anchor

Let's use GitHub's auto-generated anchors as an example. GitHub takes header lines specified in Markdown, and creates anchors for them automatically:

```markdown
Header:
# This is my header!

Auto-generated anchor:
this-is-my-header
```

Because the header has an anchor generated for it by GitHub, the owner of that Markdown file can directly link to that header in their links by explicitly typing out the auto-generated anchor:

```markdown
[This link points to the above header!](#this-is-my-header)
```

Other websites may use different anchor generation methods, but AnchorHub only supports GitHub style anchors at this time.

## Wrappers {#wrappers}

A 'wrapper' is the set of two strings that is used to demarcate an AnchorHub tag. By default, the wrapper format is an opening curly brace `{` to mark the start of a tag, and a closing curly brace `}` to mark the end of a tag.

Users can specify their own wrapper styles by using the `-w` flag on the `anchorhub` CLI, and then writing a string with the format `OPEN_PATTERN<SPACE>CLOSE_PATTERN`. For example, to specify using angle brackets, you'd write the following:

```shell
$ anchorhub -w "< >" input_directory
```

---

[Back to top](#up)