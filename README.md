# define.py

A small CLI dictionary tool that lets me look up word definitions, pronunciations, and related words directly from the terminal using the Wordnik API.

This is my first personal project built while working through [boot.dev](https://www.boot.dev), with the goal of building something practical that I'd actually use.

I set up an alias so the script can be run from anywhere like a standard CLI command:
```bash
define <word>
```

Example output:
```bash
define serendipity

======================================================================
  SERENDIPITY
======================================================================

PRONUNCIATIONS:
   - sĕr″ən-dĭp′ĭ-tē
   - S EH2 R AH0 N D IH1 P IH0 T IY0

DEFINITIONS:
   1. [noun] The faculty of making fortunate discoveries by accident.
   2. [noun] The fact or occurrence of such discoveries.
   3. [noun] An instance of making such a discovery.
   4. [noun] The happy faculty, or luck, of finding, by “accidental sagacity,” interesting items of information or unexpected proofs of one's theories; discovery of things unsought: a factitious word humorously invented by Horace Walpole.
   5. [noun] An unsought, unintended, and/or unexpected discovery and/or learning experience that happens by accident and <xref>sagacity</xref>.

RELATED WORDS:
   - Antonym: Murphy's law, perfect storm
   - Form: serendipitous, serendipitously
   - Hypernym: fluke, good fortune, good luck
   - Same Context: 5-speed, Bushman, bimbo, coagulant, cussedness
   - Synonym: accidentality, actuarial calculation, adventitiousness, break, bringing to light

======================================================================
```

## Potential improvements:
- Clean up and normalize raw output returned by the Wordnik API
- Improve handling of non-fatal API errors by displaying clear warnings and returning partial results where possible
- Add optional flags for output control
