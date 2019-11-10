"""
Interface to the Anki data store.
"""

import os
import sys
import time
from typing import List, Tuple, Any


class AnkiDB:
    """
    Connect to the Anki database.

    :param anki: Anki Python module---from the Anki source
    :param db_location: Absolute path to SQLite database
    """
    def __init__(self, anki: Any, db_location: str):
        self.anki: Any = anki
        self.db_location: str = db_location
        self.collection: Any = self._get_collection()
        self.DEFAULT_MODEL: str = 'Cloze'

    def insert_cards(self, cards: List[str], deck: str) -> None:
        """Insert cards of a specific model into a particular deck.

        :param cards: List of cards (HTML interspersed with e.g. cloze tags)
        :param deck:  Deck
        :param model: Model (basic, cloze, etc.)
        :raises ValueError: [...]
        """
        deck = self.collection.decks.byName(deck)
        if deck is None:
            raise ValueError("Deck doesn't exist")

        for card in cards:
            note = self._create_card(self.DEFAULT_MODEL)
            note.model()['did'] = deck['id'] # Make card's deck be `deck`
            note.fields[0] = card            # fields=[content, tags]
            self.collection.addNote(note)
            # Card IDs are timestamps (integer milliseconds). Avoid collisions
            # by staggering insertion time
            time.sleep(0.002)
        
        self._remove_duplicates()
        self.collection.save() # Commit to database

    def insert_image(self, image_path: str) -> str:
        """Insert an image into the media database."""
        mm = self.anki.media.MediaManager(self.collection, None)
        name = mm.addFile(image_path)
        self.collection.save()
        return name

    def _remove_duplicates(self) -> None:
        """Remove duplicate cards."""
        # Field name for Cloze card (note: only works with cloze)
        field_name = "Text"

        # Tuple contains: (duplicate_text, List[card_ids])
        duplicates: List[Tuple[str, List[int]]] = self.collection.findDupes(field_name)
        for dupe in duplicates:
            # Remove all but the least-recently inserted card. (Card IDs are 
            # monotonically increasing integers.)
            card_ids: List[int] = dupe[1]
            card_ids.sort()
            self.collection.remNotes(card_ids[1:]) # Select all but the first

    def _create_card(self, model: str) -> Any:
        """Create an empty card of a particular card model."""
        return self.anki.notes.Note(self.collection, self._get_card_model(model))

    def _get_card_model(self, model: str) -> Any:
        """Return the Anki model; e.g. cloze, basic, etc."""
        return self.collection.models.byName(model)

    def _get_collection(self) -> Any:
        """Return the Anki collection. The abstraction over the SQLite database."""
        return self.anki.Collection(self.db_location, log=True)
