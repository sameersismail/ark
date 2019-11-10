# Ark

Easily create and insert cards into Anki.

Parses an [Org-mode file](https://en.wikipedia.org/wiki/Org-mode) and extracts sections
tagged with `anki`, inside of which cards are separated with `---`. The cards
are formatted using Markdown. Only Cloze-based cards are supported; the deletions
are enclosed with `~~`. Example:

````
* Heading
** Sub-heading

#+begin_src anki
A is ~~A~~
---
A program:

```
fn main() -> Result<T, E> {
    ~~Ok(())~~
}
```
#+end_src
````

For more examples see `test/data/*`.

## Installation

1. Install Python package:

    ```
    $ git clone <repo>
    $ cd <repo>
    $ make install
    ```

2. Create configuration file, e.g.:

    ```sh
    $ cat ~/.config/ark/ark.json 
    {
        "anki_db": "/<user>/Documents/Anki2/User 1/collection.anki2"
    }
    ```

## Usage

```
usage: ark [-h] [-d] <deck> <file> [<file> ...]

positional arguments:
  <deck>      Deck of choice
  <file>      Files to parse

optional arguments:
  -h, --help  Show this help message and exit
  -d, --dry   Don't touch the database; just print parsed results
```

