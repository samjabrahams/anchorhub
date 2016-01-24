# About AnchorHub {#top}

## Beginnings {#beginnings}

This project sprung from working on the [TensorFlow](https://github.com/tensorflow/tensorflow) documentation. A few scripts from that effort were turned into the core file-processing methods in AnchorHub.

## Goals {#goals}

AnchorHub was made following a few goals, which helped guide design decisions:

### Make using AnchorHub as simple as possible {#simplify}

This includes both the command line interface and the syntax needed inside of Markdown files to make it work. Ideally, they can learn the syntax in minutes, `pip install` the software, and run it without having to learn lots of command line arguments.

This also means doing everything possible to have the software work "as-expected", as well as automatically processing entire directory trees.

### Minimize "side-grading" the experience of users {#improve}

Making sure that any features included were strictly additive was a big goal. Re-implementing things you could already do with Markdown was unneccesary for this type of project.

Additionally, I didn't want to make a processor that made a person feel like they had to learn an entirely new language. My goal was to make the syntax seem as natural to Markdown as any other part of the specification, and thus make picking it up feel "right". 

### Let the user make their own syntax decisions if possible {#empower}

This is the goal that was probably pushed below others during the programming of the initial codebase. However, the plan is to make several portions of the code more modular, such as the style of auto-generated anchors (currently only supports GitHub style). As things become more modular, I'll add in interfaces to allow for more customization.

One decision I'm still wrestling with is whether the requirement of having a '#' pound sign as part of any specified wrappers should be hard coded (at present they ARE required). To me, having the pound sign makes the syntax more semantic, and it makes it easier to copy and paste links. On the other hand, it is an extra keystroke for every anchor specified. I turn to the community to see what you think! 

## About the Author {#about}

My name is Sam Abrahams, and I created AnchorHub in January 2016. I run a blog called [MemDump](http://www.memdump.co) and work as an animator and programmer in Los Angeles, CA.

This is my first published Python code, so please let me know what best practices I messed up and how to improve my code!

[Back to top](#top)