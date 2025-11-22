"""Generate cloze-style suggestion hints for English words."""

import random


def generate_suggestion(word: str, reveal_count: int = None) -> str:
    """
    Generate a cloze-style suggestion hint for a word.

    Example: "absorb" -> "_ b _ _ r b" (shows 2-3 characters)

    Args:
        word: The English word to create a hint for
        reveal_count: Number of characters to reveal (default: 2-3 based on word length)

    Returns:
        A string with underscores and revealed characters
    """
    if not word:
        return ""

    word = word.lower().strip()
    length = len(word)

    if length <= 2:
        return word

    if reveal_count is None:
        if length <= 4:
            reveal_count = 2
        elif length <= 7:
            reveal_count = 2
        else:
            reveal_count = 3

    indices = list(range(length))
    reveal_indices = set(random.sample(indices, min(reveal_count, length)))

    result = []
    for i, char in enumerate(word):
        if i in reveal_indices:
            result.append(char)
        else:
            result.append("_")

    return " ".join(result)


def generate_suggestion_deterministic(word: str, reveal_count: int = None) -> str:
    """
    Generate a deterministic cloze-style suggestion hint.

    Reveals characters at evenly spaced positions for consistency.

    Args:
        word: The English word to create a hint for
        reveal_count: Number of characters to reveal (default: 2-3 based on word length)

    Returns:
        A string with underscores and revealed characters
    """
    if not word:
        return ""

    word = word.lower().strip()
    length = len(word)

    if length <= 2:
        return word

    if reveal_count is None:
        if length <= 4:
            reveal_count = 2
        elif length <= 7:
            reveal_count = 2
        else:
            reveal_count = 3

    reveal_count = min(reveal_count, length)
    step = length / (reveal_count + 1)
    reveal_indices = set(int(step * (i + 1)) for i in range(reveal_count))

    if length - 1 in reveal_indices:
        reveal_indices.discard(length - 1)
        reveal_indices.add(length - 2)

    result = []
    for i, char in enumerate(word):
        if i in reveal_indices:
            result.append(char)
        else:
            result.append("_")

    return " ".join(result)


if __name__ == "__main__":
    test_words = ["absorb", "abuse", "cat", "magnificent", "be", "a"]
    print("Random suggestion:")
    for word in test_words:
        print(f"  {word} -> {generate_suggestion(word)}")

    print("\nDeterministic suggestion:")
    for word in test_words:
        print(f"  {word} -> {generate_suggestion_deterministic(word)}")
