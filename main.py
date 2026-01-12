import os
from dotenv import load_dotenv
from argparse import ArgumentParser
import requests

load_dotenv()
WORDNIK_API_KEY = os.environ.get("WORDNIK_API_KEY")
WORDNIK_API_URL = "https://api.wordnik.com/v4/word.json"
TIMEOUT_SECONDS = 10


def wordnik_get(path, params):
    if not WORDNIK_API_KEY:
        return None, {
            "fatal": True,
            "status": None,
            "reason": "Missing WORDNIK_API_KEY",
        }

    url = f"{WORDNIK_API_URL}{path}"
    query_params = dict(params)
    query_params["api_key"] = WORDNIK_API_KEY

    try:
        response = requests.get(url, params=query_params, timeout=TIMEOUT_SECONDS)
    except requests.RequestException as e:
        return None, {"fatal": True, "status": None, "reason": str(e)}

    if response.status_code in (401, 403):
        return None, {
            "fatal": True,
            "status": response.status_code,
            "reason": "Unauthorized - check your API key",
        }

    if not response.ok:
        return None, {
            "fatal": False,
            "status": response.status_code,
            "reason": response.reason,
        }

    try:
        data = response.json()

        # If the user enters a word that does not exist, Wordnik returns an array of empty objects.
        # When that happens, we want to treat it as "no data found", and return a None object.
        all_empty = True
        for json_object in data:
            for _, val in json_object.items():
                if val and val != []:
                    all_empty = False
                    break
        if all_empty:
            return None, {"fatal": False, "status": 404, "reason": "No data found"}

        return data, None
    except ValueError:
        return None, {
            "fatal": False,
            "status": response.status_code,
            "reason": "Invalid JSON response",
        }


def get_definitions(word):
    return wordnik_get(
        f"/{word}/definitions",
        {
            "useCanonical": "true",
            "limit": 5,
        },
    )


def get_pronunciations(word):
    return wordnik_get(
        f"/{word}/pronunciations",
        {
            "useCanonical": "true",
            "limit": 5,
        },
    )


def get_related_words(word):
    return wordnik_get(
        f"/{word}/relatedWords",
        {
            "useCanonical": "true",
            "limitPerRelationshipType": 5,
        },
    )


def format_word_info(word, pronunciations, definitions, related_words):
    lines = []
    lines.append("=" * 70)
    lines.append(f"  {word.upper()}")
    lines.append("=" * 70)

    if pronunciations:
        lines.append("\nPRONUNCIATIONS:")
        for pron in pronunciations:
            raw = pron.get("raw", pron.get("rawType", "N/A"))
            lines.append(f"   - {raw}")

    if definitions:
        lines.append("\nDEFINITIONS:")
        for i, defn in enumerate(definitions, 1):
            part_of_speech = defn.get("partOfSpeech", "N/A")
            text = defn.get("text", "N/A")

            if part_of_speech:
                lines.append(f"   {i}. [{part_of_speech}] {text}")
            else:
                lines.append(f"  {i}. {text}")

    if related_words:
        lines.append("\nRELATED WORDS:")
        for relation in related_words:
            rel_type = relation.get("relationshipType", "related")
            words = relation.get("words", [])

            if words:
                rel_type_formatted = rel_type.replace("-", " ").title()
                words_str = ", ".join(words)
                lines.append(f"   - {rel_type_formatted}: {words_str}")

    if not definitions and not pronunciations and not related_words:
        lines.append("\n No information found for this word.")

    lines.append("")
    lines.append("=" * 70)

    return "\n".join(lines)


def main():
    parser = ArgumentParser(description="Get definitions from Wordnik API")
    parser.add_argument("word", type=str, help="The word to define")
    args = parser.parse_args()

    word = args.word.strip().lower()
    if not word:
        parser.print_help()
        raise SystemExit(1)

    pronunciations, pronunciations_err = get_pronunciations(word)
    definitions, definitions_err = get_definitions(word)
    related_words, related_words_err = get_related_words(word)

    for err in [definitions_err, pronunciations_err, related_words_err]:
        if err and err.get("fatal"):
            print("Fatal error: ", err.get("reason"))
            raise SystemExit(1)

    output = format_word_info(
        word,
        pronunciations,
        definitions,
        related_words,
    )
    print(output)


if __name__ == "__main__":
    main()
