# Logmark

## What is this?

Logmark converts directory-organized markdown files for use with Logseq by adding the parent directories of each file as [[page]] references in the files.



## Why?

This program eases transitioning to Logseq for those who have organized their notes in a hierarchical directory structure where the directories can serve as tags or topic references to the files they contain. It was created to move files from exported Joplin notes to Logseq using the notebooks as page references, but it will work with any similar collection of markdown files.

## Features

- reconstruct your notebook references in Logseq
- add a list of custom page references at the commandline
- avoid duplicating the filename as a heading if it is already used on the first line
- choose which heading level is used for the page title

## Usage

- `logmark.py --help`
#### Example:

If you have a markdown file:

_/home/user/notes/joplin-backup/webinars/journalism/investigative_journalism.md_

And you run:

`logmark.py -l 2 -i /home/user/notes/joplin-backup/ -o my-exported-notes/`

Then the _journalism.md_ file will be exported to `my-exported-notes/` and edited with a title and page references like so:

```markdown
## investigative_journalism
[[webinars]] [[journalism]]
original text...
```

_/home/user/notes/joplin-backup_ is ignored as a source of page references because it is assumed that the first source directory provided on the commandline is the root of the notes directory. Therefore, anything higher up will start referencing data not related to the target set of files. If you want the root to become a tag (in this example `joplin-backup`) then just move the root to an empty directory and stop your source path with that empty directory. This will mean that all markdown files will have the root added as a page reference.

## Requires

_only needed when run from source files_
- python 3.5+
- Python3 Tkinter
- PySimpleGui

## Current Issues and Limitations

- does not currently preserve/convert image links
- does not preserve/convert platform-specific tags
- logmark is intended for use with markdown files only
