import hashlib
from pathlib import Path

BASE_DIR = Path(__file__).parent
BAD_WORDS_FILE = BASE_DIR / "bad_words.txt"

def hash_word(word: str) -> str:
    return hashlib.sha256(word.lower().strip().encode("utf-8")).hexdigest()

hashes = set()

with open(BAD_WORDS_FILE, encoding="utf-8") as f:
    for line in f:
        w = line.strip()
        if w:
            hashes.add(hash_word(w))

print("Скопируй это в код:\n")
for h in hashes:
    print(f'"{h}",')
