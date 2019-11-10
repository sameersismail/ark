# Ark

Easily create and insert cards into Anki.

## Installation

1. Install Python package

    ```
    $ git clone <repo>
    $ cd <repo>
    $ make install
    ```

2. Create configuration file, e.g.:

    ```sh
    $ cat ~/.config/ark/ark.json 
    {
        "anki_db": "/<user>/docs/Anki2/User 1/collection.anki2"
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

