import flet as ft
try:
    import flet_audio as fta
except ImportError:
    fta = None
import json
import os
import re
import difflib
import contextlib
import requests
import asyncio
import concurrent.futures
import shutil
import ctypes
import subprocess
import tempfile
import threading
from datetime import datetime, timedelta
from functools import lru_cache
from deep_translator import GoogleTranslator
import hashlib
from urllib.parse import urlsplit

os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")

# --- НАСТРОЙКИ ---
SECRET_PASSWORD = "12345"

BAD_WORD_HASHES = {
    "dcfaf820178eb48189005598a546dcedcf75b8310d005e3fb15e150fcd0af6bc",
    "c0cf250c87fec590111ee1c0f40f2e622350dbce032c280bf3f187eb0fe09d2d",
    "40bd04e96a5fb015c01fd24a94ac1b5c7628e39984f0fef0493e9e9273dcf4a9",
    "e48cb456627e5f612b3ca655ad768546b71fc873292659d126a1d9856ce2e1a9",
    "ef0aa890daadd79977dcd6075a631679d5675cab09454c60d083464cf9ff3a73",
    "4931d0627a8415be56c01441f819c8255d4d1061b67d9f6d5fe915dbd98c1758",
    "d370a0b99a3282d0cb260c9eec66f303bb191820831d4b5c09cde58d8a3cb9ec",
    "f4d98a5bf56521e0559f019eda548033d5226245014d8c5e5cf8fe88e0db2eb5",
    "1367cf8b7f17f2d0ee0a34c41dd5414e9fe91c19fdd7ef1f9a38813a143eecc2",
    "8764694b4431b236d9d09b60eaa50901d93a869769760ac4c4798a8ec0f1e5dd",
    "eadca7e4e99cd23157da13eddb1e5e7e0bd4da2b77c19e6f3b3e6cc46687203b",
    "111ea78ce0342cb666f793e4c28c1e535dcb6b5727e478007c29b55fc1d2ba4f",
    "afa2c7032d62d525f08041a5cb6ff92409a71e7a824e44c49ab14eac8968e84f",
    "f5717e1182b3ba3a13a10db21a0da2e7cf94f0fbfa96358e378e393000f69419",
    "00e3cf18b2ac5bb1254857ee21228bb91307a494fa78db0ece9248aeac7ab8b2",
    "45dabd4d947ec001e41dc59353e9eb2f578e2d58d06e78c2ef5ad600ef5c1365",
    "82c755d78d9f9a9a7561899159d1648ddc1494d2aa8b216f73f9a666d9900243",
    "f716097b3b4320fe946464abe518383baafc019c6f3a37f5e5e7853985b4e08b",
    "1ea9df976c0ace3e4484df5a6485ce6fcbf7fcc81444e84f002503928f9c66d4",
    "bae7dcf94277bf08924b825b4897d4d68449cb451b891a3c83a3ec68968c07ce",
    "29d290e0d8b3ccf14be8f2fce2956de6e8fcbf69b4c4f57dae1878a53888d1cd",
    "0c207ba11cf9f775769aff74a742541b6e7043a88fcc4d52aaf113d0ac1bb9e9",
    "935c74e209196c8693fc9494cfb5c16086cea104c74ac1e28efedeb4e350ede1",
    "b576b7d3f65ffb92ffef85d704b7058b98b4af3eed1b5bb9fe8109ec55526118",
    "e153c58012210a074695d6d1b2200b81c803095a5953e98fae5bedb933c2bf62",
    "1797cf7567224e992360e84fe180cc5f4d681366841e094a5ec5a59083681180",
    "12ffbd6b60370ed7af9a57dc44f457c7e7e4f1a4622077b6ceb6869738862154",
    "f3506f09b55877c80806f527620f5eec5f4fd6f4bbadf3646e036a99ed4e5a7b",
    "e7712d6f3240322686a2f61457b3209e37cc5e70c8aa038e2511e562afdd27ae",
    "0aa36e9a3e0a2c9b3786cb7323add916c2c83e9dba4b20718b72bc98d3f215a3",
    "012ba834746aad5a63d38122d840795c8f661bf82230d9da55bd205719cfa12c",
    "d5310e65eb208c6bbda06ca089545bd82ace97b873d437b20717789c94d9d5cc",
    "29d624c6602701b84452a9eace80410190a01bd68a42e000818ab61e9f4d5689",
    "1dd1ef22486b101c868887d7e52983c687fc2f292e75954b0493cd909c8d340c",
    "32b6165083ffb761182ab1b6aa3dd3cbcd0d46216081b09483fd7eaf0755dc47",
    "a8797bcd386ec8e65b835499b2e3cc097ccfb455c7575b8b3e208b7ee55372aa",
    "c0f723dbdf9c3d239dcec3f2c5bf0c02ffc4cd158252caa5bc94f0cb0fd4cbe3",
    "18aff34654dab0fe63eff65a754023ab3334c0f0dc23fa2e8e600d3ad7a6dc7b",
    "f9c07040053a305dbdd0816cff2fbd5865393e70dc6c3081ce52e714321da43c",
    "8c9828507329b857ea89a9f32fd013738f3f86f9bae9809f828dc90481058e30",
    "0b33277ef23ec5082a21e963991d2f60388e5d1af60dcfb438b059f8f6f20a88",
    "cc3fc010308519086b4018478895323340a00bd7189df2a9a819c94369e11fc8",
    "049dbd7f602960a049fc5edb17bb7250b63eebbe6813c1c1a3b6d134bd02cb3c",
    "905c2dded9e8c85d0d143628c42a6b13ce2a8aa72acf847c398f0aa32de88928",
    "02d26b78b29b895d830f4086677527094330053ea5e2cf5bc3e9283e59d5438a",
    "9f576bad7938b1db3d18c54600fcd4f53ff787f7af39fcf421a149320bccf143",
    "0a118e3eead6c99597930ac5519eaefb74d1bc6b4762a4242338868f643d271a",
    "61e0636738e6ecd6fc5cbbf2c51e4569b4876b17eecafb17aa11f79b300c0473",
    "a1866c95e0d4d7902755b93ef459b44054134f57a07778027103d80d3d555b5f",
    "886a3a1667dbf4c1cfc38eb4adf7fb631fd5cd9d55ef4fb5714a87fc87dc3905",
    "d74f097cf37d88a0ab4b687ad9bbf209bb953010d41e4ba2981aed56877b126e",
    "ad88a3b029546588f3a47574c2eab0435318bbf1f52eae186169023a10ccfca3",
    "d0e84e54c33750c9ae51b3f95722ae3534127682fb3a5e2e1f6fa2483c177155",
    "78290bf24108cc98d440dbf7a024483a0aa31cc9dfce84d44609efda026d5e9c",
    "13c34bdb1324e68d79c15f316d74f5adafcb5d120e4e21ed39719b74f4a892d3",
    "7c63f1c711497e4352e09b0b4a5b36298433c8f166071b3a07862f6456e17577",
    "b0991f800ad8e0b933c26cb1d8f381d2d540464860b49eb59747b05183096a47",
    "6529f82ef946d40a0504a5f8f04191aba902d6ffd41c923351de7d74ca414ba1",
    "bd5f16fd41c1b987588af460f9972b2ef4ff56d00d3785bb1809531ac569102c",
    "cb12828a19e3eca451f2325349f76f14d3b1d071e1d11d3faf014fff4a84fb5b",
    "9309757be5bee563ed79d20d64f931d0177fa0e5e52d2288554401094f0f9ceb",
    "08d0edd5dda185f0e6366aeece99a8ddf362bc8a7d4c9497b0ca01d7ccc54785",
    "29bb5066ad1f5e4dd02c37df94f51791a0235b8119aa33e6b5384a70578e42f0",
    "28ec67bfcd9e143b24e19d5f7255349d74ed9c9d0dba404cba91013f16fa661d",
    "1de8989752127df821be09ccab6d37533717c79391198dcb5d22d1f0c67c4a13",
    "191820fffafabdf72160cf2f3cbc43a77dabd7739e6b98ce5bcda438cb52d77a",
    "c161f3c870767286eec2cba32a5b0f5e789e7c13f07301539778e449b7eaee57",
    "6eb812c9bf7e4607f76b40e3c5b62ecebfb13d9009060a50d2bb5509aa2f1780",
    "b52bb9c06d2d403a3d16af0e65b3904aacad83d057520c53e5fd916b34529df9",
    "bcfaa6e7479f8e08d60712dc9c3f8a22c6f13c84c24843d6d70af8f4cabbb047",
    "e0e7cdd3ac335fd14a88f1f1741680de90d7a6f33eb3b7b1b3387d595a7c99fd",
    "7dd16dc9909ba1ac75bc136fa3a7d065fcc02ce6a565f2a383a9e3b95fec21bd",
    "1898568c8b0267d38906e49dea0ec1b072114a001bec372151ee49d2fc3fffc5",
    "80c99be59899c419397eeb96a8741abcfd1a72e7fac56b826dd8e57b854baac3",
    "ad27d3966e0626643aec3818aa8bee10bb7c4a5191948eff2d1368e89c844119",
    "73141e3fee22786d099d391420d40aae4b4b0219c6b492cce04901213e4a5d08",
    "b020092d98337ba0b8a000aff60eaff35b33003425ccd43c144dfad3afcd162d",
    "70d59b0d1ffdcdc2389d54915ce4c052b12681f8db57d0d18fc4bd170dd6e2de",
    "cb62d77e4100cd1b8e096021e186e8ee3f9e4f3f873931dc1008a6cddaf186f8",
    "d05661c81df53f54e9973d8ccdbb0666cd91925d89b24abfad58a1073d3f0a2e",
    "2d3bc04310fd9aa707da1ef2a7bd606e1c00f8923eb77908a4be2aa0b0759188",
    "bbd2bb847de939bde9c753a865258eb6a64c51ab0b12003899a31e14bab4f4e7",
    "6876f57b90dc6339e55e2eecafcc0eac3c066555ebe09d735f15f143049fae21",
    "ced7ddb187d4b334459430fad4dee5fa04c8cf21b278e6601331c076acfeb659",
    "2ec71a16763f00dcf8d83d4eb3c62b5f5980074b007ae73ef7bed83ed63c106f",
    "bad34fa4a49ec3d98aaf2e09a496e80e3b8a636c69237e284621acc1c589a51e",
    "42ba05a7e5e4944d20b2427cf4ade8bbe2fad6836a77ee95a0313737be98c9aa",
    "6383c2d03c7205e8f79017411627e937f6ee8b7df8b6f475f09081367023c2c0",
    "dd8d14d884b97a71561f74ec07fd3d462e39004039606ca5df634cf938493988",
    "4a1933ad3930cebe423e14c8c2d7a70cbd83532edb098e0631a473bd7c2370ab",
    "2897ebd05130453f11746a0dd258ddf206da56da9e5bb46228992c245c60da67",
    "a8fbcf188376bf67aa8be2eb0e853ac646f078fbf34da419bee8ed7bc8fb9d51",
    "1f74d79e4d06397a7c5252f67018b8f15d44b2ba56517cd1cf1983fa2bc401af",
    "bf43c982463e3b681cc29b9e39b50dc60632018b041673a87e66bb8c0bce6993",
    "2829d5bc41555394879cb46411b51d9fb21326229cfd9ce1c0b8f1e837b3f16d",
    "2ef87fe7249e246e386dd0b24f77b324c912a5318c1f855d8ba458ffd8be6ca6",
}

AUDIO_CACHE_DIR = os.path.join(tempfile.gettempdir(), "perevodchik_audio_cache")
MCI_AUDIO_ALIAS = "perevodchik_audio"
_mci_lock = threading.Lock()


def _get_audio_cache_path(url: str) -> str:
    ext = os.path.splitext(urlsplit(url).path)[1].lower()
    if ext not in {".mp3", ".wav", ".ogg"}:
        ext = ".mp3"
    return os.path.join(
        AUDIO_CACHE_DIR,
        f"{hashlib.sha256(url.encode('utf-8')).hexdigest()}{ext}",
    )


def _download_audio_to_cache(url: str) -> str:
    os.makedirs(AUDIO_CACHE_DIR, exist_ok=True)
    audio_path = _get_audio_cache_path(url)
    if os.path.exists(audio_path) and os.path.getsize(audio_path) > 0:
        return audio_path

    last_error = None
    temp_path = f"{audio_path}.part"

    for _ in range(3):
        try:
            response = requests.get(
                url,
                timeout=(10, 60),
                stream=True,
                headers={"User-Agent": "Mozilla/5.0"},
            )
            response.raise_for_status()

            with open(temp_path, "wb") as audio_file:
                for chunk in response.iter_content(chunk_size=65536):
                    if chunk:
                        audio_file.write(chunk)

            os.replace(temp_path, audio_path)
            return audio_path
        except Exception as ex:
            last_error = ex
            if os.path.exists(temp_path):
                try:
                    os.remove(temp_path)
                except OSError:
                    pass

    raise last_error


def _mci_send(command: str) -> None:
    error_code = ctypes.windll.winmm.mciSendStringW(command, None, 0, None)
    if error_code == 0:
        return

    error_buffer = ctypes.create_unicode_buffer(256)
    ctypes.windll.winmm.mciGetErrorStringW(error_code, error_buffer, len(error_buffer))
    raise RuntimeError(error_buffer.value or f"MCI error {error_code}")


def _play_audio_inside_app(url: str) -> None:
    audio_path = _download_audio_to_cache(url)

    if os.name == "nt":
        with _mci_lock:
            try:
                _mci_send(f"close {MCI_AUDIO_ALIAS}")
            except Exception:
                pass

            _mci_send(f'open "{audio_path}" type mpegvideo alias {MCI_AUDIO_ALIAS}')
            _mci_send(f"play {MCI_AUDIO_ALIAS} from 0")
        return

    try:
        import pygame
    except ImportError as ex:
        raise RuntimeError("Ни Windows MCI, ни pygame недоступны.") from ex

    if not pygame.mixer.get_init():
        pygame.mixer.init()

    pygame.mixer.music.stop()
    pygame.mixer.music.load(audio_path)
    pygame.mixer.music.play()


def _speak_text_inside_app(text: str) -> None:
    if os.name != "nt":
        raise RuntimeError("Офлайн-озвучка через Windows Speech доступна только на Windows.")

    safe_text = text.replace("'", "''")
    script = f"""
Add-Type -AssemblyName System.Speech
$synth = New-Object System.Speech.Synthesis.SpeechSynthesizer
$voice = $synth.GetInstalledVoices() |
    ForEach-Object {{ $_.VoiceInfo }} |
    Where-Object {{ $_.Culture.Name -like 'en-*' }} |
    Select-Object -First 1
if ($voice) {{ $synth.SelectVoice($voice.Name) }}
$synth.Speak('{safe_text}')
"""
    subprocess.run(
        [
            r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe",
            "-NoProfile",
            "-Command",
            script,
        ],
        check=True,
        timeout=15,
    )


async def prefetch_audio(url: str | None) -> None:
    if not url:
        return

    try:
        await asyncio.to_thread(_download_audio_to_cache, url)
        print(f"[audio] prefetched: {url}")
    except Exception as ex:
        print(f"[audio] prefetch failed: {ex}")


async def _resolve_audio_service_src(page: ft.Page, url: str | None) -> str | None:
    if not url:
        return None

    if not page.platform or not page.platform.is_mobile():
        return url

    try:
        print("[audio] caching mobile audio")
        cached_audio = await asyncio.to_thread(_download_audio_to_cache, url)
        print(f"[audio] using cached mobile audio: {cached_audio}")
        return cached_audio
    except Exception as ex:
        print(f"[audio] mobile cache failed: {ex}")
        return url

def _hash_word(word: str) -> str:
    return hashlib.sha256(word.lower().strip().encode("utf-8")).hexdigest()

def contains_bad_words(text: str) -> bool:
    """
    Проверяет, содержит ли текст запрещённые слова
    """
    words = text.lower().split()
    for w in words:
        if _hash_word(w) in BAD_WORD_HASHES:
            return True
    return False

def clean_translation(text: str) -> str:
    """
    Заменяет перевод, если найден мат
    """
    if contains_bad_words(text):
        return "⚠️ Перевод скрыт из-за нецензурной лексики"
    return text

def contains_bad_words(text: str) -> bool:
    words = re.findall(r"[a-zA-Zа-яА-ЯёЁ]+", text.lower())
    for w in words:
        if _hash_word(w) in BAD_WORD_HASHES:
            return True
    return False

# --- ФАЙЛЫ ---
DATA_FILE = os.path.join(os.path.expanduser("~"), "my_glossary.json")
BACKUP_DIR = os.path.join(os.path.expanduser("~"), "my_glossary_backups")

HISTORY_FILE = os.path.join(os.path.expanduser("~"), "my_glossary_history.json")
HISTORY_LIMIT = 100

FAVORITES_FILE = os.path.join(os.path.expanduser("~"), "my_glossary_favorites.json")

TRAIN_FILE = os.path.join(os.path.expanduser("~"), "my_glossary_training.json")


# --- FAVORITES ---
def load_favorites() -> set[str]:
    if not os.path.exists(FAVORITES_FILE):
        return set()
    try:
        with open(FAVORITES_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return set(x.lower() for x in data if isinstance(x, str))
    except:
        pass
    return set()


def save_favorites(favs: set[str]):
    try:
        with open(FAVORITES_FILE, "w", encoding="utf-8") as f:
            json.dump(sorted(list(favs)), f, ensure_ascii=False, indent=2)
    except Exception as e:
        print("Ошибка сохранения избранного:", e)


# --- HISTORY ---
def load_history() -> list[str]:
    if not os.path.exists(HISTORY_FILE):
        return []
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except:
        return []


def save_history(history: list[str]):
    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print("Ошибка сохранения истории:", e)


def add_to_history(history: list[str], word: str) -> list[str]:
    w = (word or "").strip().lower()
    if not w:
        return history
    history = [x for x in history if x != w]
    history.insert(0, w)
    return history[:HISTORY_LIMIT]


# --- TRAINING DATA ---
def load_training() -> dict:
    if not os.path.exists(TRAIN_FILE):
        return {}
    try:
        with open(TRAIN_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, dict) else {}
    except:
        return {}


def save_training(training: dict):
    try:
        with open(TRAIN_FILE, "w", encoding="utf-8") as f:
            json.dump(training, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print("Ошибка сохранения тренировки:", e)


# --- LOCAL DATA ---
def load_local_data() -> dict:
    if not os.path.exists(DATA_FILE):
        return {}
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}


def save_local_data(data: dict):
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Ошибка сохранения словаря: {e}")


# --- BACKUP ---
def ensure_backup_dir():
    os.makedirs(BACKUP_DIR, exist_ok=True)


def create_backup():
    ensure_backup_dir()
    if not os.path.exists(DATA_FILE):
        return None
    ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_path = os.path.join(BACKUP_DIR, f"my_glossary_backup_{ts}.json")
    shutil.copy2(DATA_FILE, backup_path)
    return backup_path


def get_latest_backup_path():
    if not os.path.isdir(BACKUP_DIR):
        return None
    files = [f for f in os.listdir(BACKUP_DIR) if f.lower().endswith(".json")]
    if not files:
        return None
    files.sort(reverse=True)
    return os.path.join(BACKUP_DIR, files[0])


def restore_latest_backup():
    latest = get_latest_backup_path()
    if not latest:
        return None
    shutil.copy2(latest, DATA_FILE)
    return latest


# --- TRANSLATION ---
def is_russian(text: str) -> bool:
    return bool(re.search('[а-яА-Я]', text))


def is_lazy_translation(word: str, translation: str) -> bool:
    trans = translation.lower().strip()
    if len(trans.split()) == 1:
        if difflib.SequenceMatcher(None, word.lower(), trans).ratio() > 0.6:
            return True
    return False


@lru_cache(maxsize=500)
def translate_text(text: str, original_word: str) -> str:
    try:
        translator = GoogleTranslator(source='auto', target='ru')
        res = translator.translate(text)
        if res and is_russian(res):
            if not contains_bad_words(res) and not is_lazy_translation(original_word, res):
                return res
    except:
        pass
    return ""


def smart_merge(text1: str, text2: str) -> str:
    t1 = text1.strip().rstrip('.')
    t2 = text2.strip().rstrip('.')
    w1 = t1.split()
    w2 = t2.split()
    common_tail = []
    while w1 and w2 and w1[-1].lower() == w2[-1].lower():
        common_tail.insert(0, w1.pop())
        w2.pop()
    if not common_tail:
        return f"{t1.capitalize()} / {t2.capitalize()}"
    head1 = " ".join(w1).capitalize()
    head2 = " ".join(w2).capitalize()
    tail = " ".join(common_tail)
    if head1 and head2:
        return f"{head1} / {head2} {tail}"
    return f"{(head1 or head2)} {tail}".strip().capitalize()


def _process_single_definition(d: dict, pos: str, word: str):
    eng_def = d.get("definition", "")
    clean = re.sub(r'^\s*\(.*?\)\s*', '', eng_def)
    clean = re.sub(r'^(a|an|the)\s+', '', clean, flags=re.IGNORECASE)
    rus_def = translate_text(clean, word)
    if rus_def:
        return {"rus": rus_def.strip().rstrip('.'), "ex": d.get("example", ""), "pos": pos}
    return None


def heavy_search_task(word: str, local_data: dict):
    final_results = []
    audio_url = None
    try:
        if word in local_data:
            for item in local_data[word]:
                final_results.append({"rus": item["rus"], "ex": item["ex"], "pos": "МОЁ", "is_local": True})

        url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
        resp = requests.get(url, timeout=10)

        if resp.status_code == 200:
            data_json = resp.json()

            # --- AUDIO (pronunciation) ---
            try:
                for entry in data_json:
                    for ph in entry.get("phonetics", []):
                        a = (ph.get("audio") or "").strip()
                        if not a:
                            continue
                        if a.startswith("//"):
                            a = "https:" + a
                        if not a.startswith("http"):
                            continue
                        audio_url = a
                        raise StopIteration
            except StopIteration:
                pass
            except:
                pass

            raw_online = []
            with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
                futures = []
                for entry in data_json:
                    for meaning in entry.get("meanings", []):
                        pos = (meaning.get("partOfSpeech", "общее") or "общее").upper()
                        for d in meaning.get("definitions", []):
                            futures.append(executor.submit(_process_single_definition, d, pos, word))
                for future in concurrent.futures.as_completed(futures):
                    res = future.result()
                    if res:
                        raw_online.append(res)

            for res in raw_online:
                merged = False
                for existing in [x for x in final_results if not x.get("is_local")]:
                    if difflib.SequenceMatcher(None, res["rus"].lower(), existing["rus"].lower()).ratio() > 0.35:
                        existing["rus"] = smart_merge(existing["rus"], res["rus"])
                        merged = True
                        break
                if not merged:
                    res["rus"] = res["rus"].capitalize()
                    final_results.append(res)
    except:
        pass

    return {"results": final_results, "audio_url": audio_url}


# --- UI ---
async def main(page: ft.Page):
    page.window.icon = os.path.join(os.path.dirname(__file__), "icon.ico")
    page.title = "Переводчик"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 10
    page.scroll = ft.ScrollMode.ADAPTIVE

    local_data = load_local_data()
    history = load_history()
    favorites = load_favorites()
    training = load_training()
    pending_action = {"type": None, "data": None}
    audio_service = None

    if fta is not None:
        try:
            audio_service = fta.Audio(src="", autoplay=False, volume=1.0)
            print("[audio] flet-audio service initialized")
        except Exception:
            audio_service = None

    def now_ts() -> int:
        return int(datetime.now().timestamp())

    def today_key() -> str:
        return datetime.now().strftime("%Y-%m-%d")

    def ensure_training_meta():
        if "_meta" not in training or not isinstance(training.get("_meta"), dict):
            training["_meta"] = {}
        meta = training["_meta"]
        meta.setdefault("daily", {})
        meta.setdefault("last_use", 0)
        return meta

    def bump_stats(known: bool):
        meta = ensure_training_meta()
        k = today_key()
        daily = meta["daily"]
        if k not in daily or not isinstance(daily.get(k), dict):
            daily[k] = {"known": 0, "dont": 0}
        if known:
            daily[k]["known"] += 1
        else:
            daily[k]["dont"] += 1
        meta["last_use"] = now_ts()

    def build_training_pool() -> list[str]:
        pool = set(local_data.keys()) | set(favorites)
        pool = {w.strip().lower() for w in pool if isinstance(w, str) and w.strip()}
        return sorted(pool)

    def get_card_stats(word: str) -> dict:
        st = training.get(word)
        if not isinstance(st, dict):
            st = {"interval": 0, "ease": 2.0, "next_due": 0}
            training[word] = st
        st.setdefault("interval", 0)
        st.setdefault("ease", 2.0)
        st.setdefault("next_due", 0)
        return st

    def pick_next_card(pool: list[str]) -> str | None:
        t = now_ts()
        due = []
        future = []
        for w in pool:
            st = get_card_stats(w)
            if int(st.get("next_due", 0)) <= t:
                due.append(w)
            else:
                future.append((int(st.get("next_due", 0)), w))
        if due:
            import random
            return random.choice(due)
        if future:
            future.sort(key=lambda x: x[0])
            return future[0][1]
        return None

    def get_best_translation_for_word(word: str) -> str:
        if word in local_data and local_data[word]:
            first = local_data[word][0].get("rus", "")
            if first:
                return first
        try:
            tr = GoogleTranslator(source="en", target="ru").translate(word)
            return tr.strip() if tr else ""
        except:
            return ""

    def schedule_known(word: str):
        st = get_card_stats(word)
        ease = float(st.get("ease", 2.0))
        interval = int(st.get("interval", 0))
        ease = min(2.7, ease + 0.10)
        interval = 1 if interval <= 0 else int(max(1, round(interval * ease)))
        st["ease"] = ease
        st["interval"] = interval
        st["next_due"] = now_ts() + interval * 24 * 3600

    def schedule_dontknow(word: str):
        st = get_card_stats(word)
        ease = float(st.get("ease", 2.0))
        ease = max(1.3, ease - 0.20)
        st["ease"] = ease
        st["interval"] = 1
        st["next_due"] = now_ts() + 1 * 24 * 3600

    def current_word() -> str:
        return search_field.value.strip().lower()

    # ---------------------------------------------
    # ЭЛЕМЕНТЫ UI (Словарь)
    # ---------------------------------------------
    search_field = ft.TextField(label="Введите слово...", border_radius=10, expand=True, text_size=16)
    results_column = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True, spacing=10)
    progress_bar = ft.ProgressBar(visible=False, color=ft.Colors.BLUE_400)
    search_btn = ft.IconButton(icon=ft.Icons.SEARCH, icon_size=30, tooltip="Поиск")

    current_audio_url = {"url": None}

    # ---------------------------------------------
    # ДИАЛОГИ (пароль / редактор)
    # ---------------------------------------------
    dlg_pass = ft.TextField(label="Пароль", password=True, can_reveal_password=True, autofocus=True)
    dlg_word = ft.TextField(label="Слово (англ.)")
    dlg_def = ft.TextField(label="Перевод (рус.)")
    dlg_ex = ft.TextField(label="Пример (англ.)")

    async def close_auth(e):
        auth_dialog.open = False
        dlg_pass.value = ""
        page.update()

    async def check_password(e):
        if dlg_pass.value == SECRET_PASSWORD:
            dlg_pass.value = ""
            dlg_pass.error_text = None
            auth_dialog.open = False
            page.update()

            action = pending_action["type"]
            data = pending_action["data"]

            if action == "add":
                dlg_word.value = ""
                dlg_def.value = ""
                dlg_ex.value = ""
                dlg_word.read_only = False
                add_dialog.open = True
                page.update()

            elif action == "edit":
                word = data["word"]
                index = data["index"]
                item = local_data[word][index]

                dlg_word.value = word
                dlg_word.read_only = True
                dlg_def.value = item["rus"]
                dlg_ex.value = item["ex"]
                add_dialog.data = index
                add_dialog.open = True
                page.update()

            elif action == "delete":
                word = data["word"]
                index = data["index"]
                if word in local_data and 0 <= index < len(local_data[word]):
                    del local_data[word][index]
                    if not local_data[word]:
                        del local_data[word]
                    save_local_data(local_data)
                    await show_all_words(None)
        else:
            dlg_pass.error_text = "Неверный пароль!"
            page.update()

    auth_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Проверка доступа"),
        content=ft.Column([ft.Text("Введите пароль:"), dlg_pass], tight=True, width=300),
        actions=[ft.TextButton("Отмена", on_click=close_auth), ft.TextButton("Войти", on_click=check_password)],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    dlg_pass.on_submit = check_password

    async def close_add_dialog(e):
        add_dialog.open = False
        page.update()

    async def save_word_data(e):
        w = dlg_word.value.strip().lower()
        d = dlg_def.value.strip()
        ex = dlg_ex.value.strip()

        if not w or not d:
            dlg_word.error_text = "Обязательно" if not w else None
            dlg_def.error_text = "Обязательно" if not d else None
            page.update()
            return

        if w not in local_data:
            local_data[w] = []

        if pending_action["type"] == "edit":
            index = add_dialog.data
            if 0 <= index < len(local_data[w]):
                local_data[w][index] = {"rus": d.capitalize(), "ex": ex}
            else:
                local_data[w].append({"rus": d.capitalize(), "ex": ex})
        else:
            local_data[w].append({"rus": d.capitalize(), "ex": ex})

        save_local_data(local_data)
        add_dialog.open = False
        page.update()

        if pending_action["type"] == "edit":
            await show_all_words(None)
        else:
            search_field.value = w
            await run_search_async(None)

    add_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Редактор слова"),
        content=ft.Column([dlg_word, dlg_def, dlg_ex], tight=True, width=300),
        actions=[ft.TextButton("Отмена", on_click=close_add_dialog), ft.TextButton("Сохранить", on_click=save_word_data)],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    page.overlay.append(auth_dialog)
    page.overlay.append(add_dialog)

    # ---------------------------------------------
    # ДИАЛОГ: ИСТОРИЯ
    # ---------------------------------------------
    history_column = ft.Column(spacing=6, scroll=ft.ScrollMode.AUTO, height=420)

    async def close_history_dialog(e):
        history_dialog.open = False
        page.update()

    async def clear_history(e):
        nonlocal history
        history = []
        save_history(history)
        history_column.controls = [ft.Text("История очищена.", color=ft.Colors.GREY_400)]
        page.update()

    async def use_history_click(e):
        word = (e.control.data or "").strip().lower()
        if not word:
            return
        search_field.value = word
        page.update()
        await run_search_async(None)

    async def open_history_dialog(e=None):
        history_column.controls.clear()
        if not history:
            history_column.controls.append(ft.Text("История пуста.", color=ft.Colors.GREY_400))
        else:
            for w in history:
                history_column.controls.append(
                    ft.ListTile(
                        title=ft.Text(w),
                        leading=ft.Icon(ft.Icons.SEARCH),
                        data=w,
                        on_click=use_history_click,
                    )
                )
        history_dialog.open = True
        page.update()

    history_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("История запросов"),
        content=history_column,
        actions=[ft.TextButton("Очистить", on_click=clear_history), ft.TextButton("Закрыть", on_click=close_history_dialog)],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    page.overlay.append(history_dialog)

    # ---------------------------------------------
    # ДИАЛОГ: ИЗБРАННОЕ
    # ---------------------------------------------
    favorites_column = ft.Column(spacing=6, scroll=ft.ScrollMode.AUTO, height=420)

    async def close_favorites_dialog(e):
        favorites_dialog.open = False
        page.update()

    async def clear_favorites(e):
        nonlocal favorites
        favorites = set()
        save_favorites(favorites)
        favorites_column.controls = [ft.Text("Избранное очищено.", color=ft.Colors.GREY_400)]
        refresh_stats_view()
        refresh_menu_states()
        page.update()

    async def use_favorite_click(e):
        word = (e.control.data or "").strip().lower()
        if not word:
            return
        search_field.value = word
        page.update()
        await run_search_async(None)

    async def remove_favorite_click(e):
        nonlocal favorites
        word = (e.control.data or "").strip().lower()
        if word in favorites:
            favorites.remove(word)
            save_favorites(favorites)
        await open_favorites_dialog(None)
        refresh_stats_view()
        refresh_menu_states()
        page.update()

    async def open_favorites_dialog(e=None):
        favorites_column.controls.clear()
        favs_sorted = sorted(list(favorites))
        if not favs_sorted:
            favorites_column.controls.append(ft.Text("Избранных слов нет.", color=ft.Colors.GREY_400))
        else:
            for w in favs_sorted:
                favorites_column.controls.append(
                    ft.ListTile(
                        title=ft.Text(w),
                        leading=ft.Icon(ft.Icons.STAR, color=ft.Colors.AMBER),
                        trailing=ft.IconButton(
                            icon=ft.Icons.DELETE,
                            tooltip="Убрать из избранного",
                            data=w,
                            on_click=remove_favorite_click,
                        ),
                        data=w,
                        on_click=use_favorite_click,
                    )
                )
        favorites_dialog.open = True
        page.update()

    favorites_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Избранные слова ⭐"),
        content=favorites_column,
        actions=[ft.TextButton("Очистить", on_click=clear_favorites), ft.TextButton("Закрыть", on_click=close_favorites_dialog)],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    page.overlay.append(favorites_dialog)

    # ---------------------------------------------
    # ОБРАБОТЧИКИ: добавление/редактирование/удаление
    # ---------------------------------------------
    async def request_auth(action_type, data=None):
        pending_action["type"] = action_type
        pending_action["data"] = data
        auth_dialog.open = True
        page.update()

    async def handle_fab_click(e=None):
        await request_auth("add")

    async def handle_edit_click(e):
        await request_auth("edit", e.control.data)

    async def handle_delete_click(e):
        await request_auth("delete", e.control.data)

    # ---------------------------------------------
    # БЭКАП / ВОССТАНОВЛЕНИЕ
    # ---------------------------------------------
    async def handle_backup_click(e=None):
        try:
            path = create_backup()
            if not path:
                page.snack_bar = ft.SnackBar(ft.Text("Нет файла для бэкапа (my_glossary.json не найден)."))
            else:
                page.snack_bar = ft.SnackBar(ft.Text(f"Бэкап создан: {path}"))
            page.snack_bar.open = True
            page.update()
        except Exception as ex:
            page.snack_bar = ft.SnackBar(ft.Text(f"Ошибка бэкапа: {ex}"))
            page.snack_bar.open = True
            page.update()

    async def handle_restore_click(e=None):
        try:
            restored_from = restore_latest_backup()
            if not restored_from:
                page.snack_bar = ft.SnackBar(ft.Text("Бэкапы не найдены."))
                page.snack_bar.open = True
                page.update()
                return

            nonlocal local_data
            local_data = load_local_data()

            page.snack_bar = ft.SnackBar(ft.Text(f"Восстановлено из: {restored_from}"))
            page.snack_bar.open = True
            page.update()

            await show_all_words(None)
        except Exception as ex:
            page.snack_bar = ft.SnackBar(ft.Text(f"Ошибка восстановления: {ex}"))
            page.snack_bar.open = True
            page.update()

    # ---------------------------------------------
    # ОЗВУЧКА
    # ---------------------------------------------
    async def handle_speak_click(e=None):
        url = current_audio_url.get("url")
        word = current_word()
        print(f"[audio] click, url={url!r}")
        if not url and not word:
            page.snack_bar = ft.SnackBar(ft.Text("Озвучка недоступна для этого слова."))
            page.snack_bar.open = True
            page.update()
            return

        try:
            if os.name == "nt":
                cached_audio = _get_audio_cache_path(url) if url else None
                if cached_audio and os.path.exists(cached_audio) and os.path.getsize(cached_audio) > 0:
                    print("[audio] trying Windows MCI backend")
                    await asyncio.to_thread(_play_audio_inside_app, url)
                    print("[audio] Windows MCI playback started")
                    return

                if word:
                    print("[audio] using offline Windows TTS")
                    await asyncio.to_thread(_speak_text_inside_app, word)
                    print("[audio] offline Windows TTS completed")
                    return

            playable_src = await _resolve_audio_service_src(page, url)

            if audio_service is not None and playable_src:
                with contextlib.suppress(Exception):
                    await audio_service.release()
                audio_service.src = playable_src
                audio_service.update()
                await asyncio.sleep(0.1)
                print(f"[audio] trying flet-audio backend with src={playable_src!r}")
                await asyncio.wait_for(audio_service.play(), timeout=5)
                print("[audio] flet-audio play() sent")
                return
        except Exception as ex:
            audio_error = ex
            print(f"[audio] flet-audio error: {ex}")
        else:
            audio_error = None

        try:
            if url:
                print("[audio] trying fallback backend")
                await asyncio.to_thread(_play_audio_inside_app, url)
                print("[audio] fallback playback started")
                return

            if word and os.name == "nt":
                print("[audio] trying final offline Windows TTS fallback")
                await asyncio.to_thread(_speak_text_inside_app, word)
                print("[audio] final offline Windows TTS completed")
                return
        except Exception as ex:
            details = str(ex)
            if audio_error is not None:
                details = f"{audio_error}; запасной плеер: {ex}"
            print(f"[audio] playback failed: {details}")
            page.snack_bar = ft.SnackBar(ft.Text(f"Не удалось воспроизвести аудио: {details}"))
            page.snack_bar.open = True
            page.update()

    def start_speak_click(e=None):
        page.run_task(handle_speak_click, e)

    # ---------------------------------------------
    # ИЗБРАННОЕ: только для ИСКОМОГО слова
    # ---------------------------------------------
    async def toggle_favorite_searched_word(e=None):
        nonlocal favorites
        w = current_word()
        if not w:
            return
        if w in favorites:
            favorites.remove(w)
        else:
            favorites.add(w)
        save_favorites(favorites)
        refresh_stats_view()
        refresh_menu_states()
        page.update()

    # ---------------------------------------------
    # СПИСОК МОИХ СЛОВ
    # ---------------------------------------------
    async def show_all_words(e=None):
        search_field.value = ""
        results_column.controls.clear()

        if not local_data:
            results_column.controls.append(ft.Text("Словарь пуст.", size=18, color=ft.Colors.GREY))
            refresh_stats_view()
            refresh_menu_states()
            page.update()
            return

        sorted_words = sorted(local_data.keys())
        total_items = sum(len(v) for v in local_data.values())

        all_cards = [ft.Text(f"Мой словарь ({total_items} записей)", size=20, weight="bold")]

        for word in sorted_words:
            for i, item in enumerate(local_data[word]):
                content = ft.Column([
                    ft.Row([
                        ft.Text(word.capitalize(), size=22, weight="bold", color=ft.Colors.GREEN_300, expand=True),
                        ft.IconButton(
                            icon=ft.Icons.EDIT,
                            icon_color=ft.Colors.BLUE_200,
                            tooltip="Редактировать",
                            data={"word": word, "index": i},
                            on_click=handle_edit_click,
                        ),
                        ft.IconButton(
                            icon=ft.Icons.DELETE,
                            icon_color=ft.Colors.RED_200,
                            tooltip="Удалить",
                            data={"word": word, "index": i},
                            on_click=handle_delete_click,
                        ),
                    ]),
                    ft.Text(item["rus"], size=18, weight="w500"),
                ])

                if item["ex"]:
                    content.controls.append(ft.Divider(height=10, color=ft.Colors.GREY_800))
                    content.controls.append(ft.Text(f"\"{item['ex']}\"", italic=True, color=ft.Colors.GREY_400, size=14))

                all_cards.append(ft.Container(
                    content=content,
                    padding=15,
                    bgcolor=ft.Colors.GREEN_900,
                    border=ft.Border.all(1, ft.Colors.GREEN_400),
                    border_radius=12,
                    margin=ft.margin.only(bottom=5),
                ))

        results_column.controls = all_cards
        refresh_stats_view()
        refresh_menu_states()
        page.update()

    # ---------------------------------------------
    # ПОИСК
    # ---------------------------------------------
    async def run_search_async(e=None):
        word = current_word()
        if not word:
            return

        meta = ensure_training_meta()
        meta["last_use"] = now_ts()
        save_training(training)

        nonlocal history
        history = add_to_history(history, word)
        save_history(history)

        search_btn.disabled = True
        progress_bar.visible = True
        results_column.controls.clear()
        page.update()

        payload = await asyncio.to_thread(heavy_search_task, word, local_data)
        final_results = payload.get("results", [])
        current_audio_url["url"] = payload.get("audio_url")
        if current_audio_url["url"]:
            page.run_task(prefetch_audio, current_audio_url["url"])

        cards = []
        if not final_results:
            cards.append(ft.Text("Ничего не найдено", size=16, color=ft.Colors.GREY))

        for res in final_results:
            is_local = res.get("is_local", False)
            border = ft.Colors.GREEN_400 if is_local else ft.Colors.BLUE_700
            bg = ft.Colors.GREEN_900 if is_local else "#1f1f1f"

            content = ft.Column([
                ft.Row([
                    ft.Container(
                        content=ft.Text(res["pos"], size=10, weight="bold"),
                        bgcolor=border,
                        padding=ft.Padding.symmetric(horizontal=6, vertical=2),
                        border_radius=4,
                    )
                ], alignment=ft.MainAxisAlignment.END),
                ft.Text(res["rus"], size=18, weight="w500"),
            ])

            if res["ex"]:
                content.controls.append(ft.Text(f"\"{res['ex']}\"", italic=True, color=ft.Colors.GREY_400, size=14))

            cards.append(ft.Container(
                content=content,
                padding=15,
                bgcolor=bg,
                border=ft.Border.all(1, border if is_local else ft.Colors.TRANSPARENT),
                border_radius=12,
                animate=ft.Animation(duration=300, curve=ft.AnimationCurve.EASE_OUT),
            ))

        results_column.controls = cards
        search_btn.disabled = False
        progress_bar.visible = False
        refresh_stats_view()
        refresh_menu_states()
        page.update()

    search_field.on_submit = run_search_async
    search_btn.on_click = run_search_async

    # ---------------------------------------------
    # ТРЕНИРОВКА (флеш-карточки)
    # ---------------------------------------------
    train_title = ft.Text("Тренировка", size=22, weight="bold")
    train_info = ft.Text("Вспомни перевод, нажми «Проверить», затем оцени себя.", color=ft.Colors.GREY_400)

    card_word = ft.Text("", size=34, weight="bold")
    card_answer = ft.Text("", size=24, visible=False)

    btn_check = ft.ElevatedButton("Проверить")
    btn_know = ft.ElevatedButton("👍 Знал", disabled=True)
    btn_dont = ft.ElevatedButton("❌ Не знал", disabled=True)
    btn_next = ft.OutlinedButton("Следующая")

    current_card = {"word": None, "pool": []}

    async def training_load_next(e=None):
        current_card["pool"] = build_training_pool()
        w = pick_next_card(current_card["pool"])

        current_card["word"] = w
        card_answer.visible = False
        btn_know.disabled = True
        btn_dont.disabled = True

        if not w:
            card_word.value = "Нет карточек 😕"
            card_answer.value = "Добавь слова в «Мой словарь» или добавь поисковое слово в ⭐ избранное."
            card_answer.visible = True
            btn_check.disabled = True
            btn_next.disabled = True
            page.update()
            return

        card_word.value = w
        card_answer.value = ""
        btn_check.disabled = False
        btn_next.disabled = False
        page.update()

    async def training_show_answer(e=None):
        w = current_card["word"]
        if not w:
            return
        ans = get_best_translation_for_word(w)
        card_answer.value = ans if ans else "Перевод не найден"
        card_answer.visible = True
        btn_know.disabled = False
        btn_dont.disabled = False

        meta = ensure_training_meta()
        meta["last_use"] = now_ts()
        save_training(training)

        refresh_stats_view()
        page.update()

    async def training_mark_known(e=None):
        w = current_card["word"]
        if not w:
            return
        schedule_known(w)
        bump_stats(True)
        save_training(training)
        refresh_stats_view()
        await training_load_next()

    async def training_mark_dontknow(e=None):
        w = current_card["word"]
        if not w:
            return
        schedule_dontknow(w)
        bump_stats(False)
        save_training(training)
        refresh_stats_view()
        await training_load_next()

    btn_check.on_click = training_show_answer
    btn_know.on_click = training_mark_known
    btn_dont.on_click = training_mark_dontknow
    btn_next.on_click = training_load_next

    training_view = ft.Column(
        [
            train_title,
            train_info,
            ft.Container(height=10),
            ft.Container(
                content=ft.Column([card_word, ft.Divider(), card_answer], spacing=10),
                padding=20,
                border_radius=16,
                bgcolor="#1f1f1f",
                border=ft.Border.all(1, ft.Colors.GREY_800),
            ),
            ft.Row([btn_check, btn_know, btn_dont, btn_next], wrap=True),
        ],
        spacing=12,
        expand=True,
    )

    # ---------------------------------------------
    # СТАТИСТИКА
    # ---------------------------------------------
    stat_total = ft.Text("📚 Всего слов: 0", size=20, weight="bold")
    stat_today = ft.Text("✅ Сегодня выучено: 0", size=18)
    stat_rate = ft.Text("🎯 Процент запоминания: 0%", size=18)
    stat_last = ft.Text("📅 Последнее использование: —", size=18, color=ft.Colors.GREY_400)

    def human_day(ts: int) -> str:
        if not ts:
            return "—"
        d = datetime.fromtimestamp(ts).date()
        today = datetime.now().date()
        if d == today:
            return "сегодня"
        if (today - d).days == 1:
            return "вчера"
        return d.strftime("%d.%m.%Y")

    def get_daily_counts(day: str):
        meta = ensure_training_meta()
        daily = meta.get("daily", {})
        x = daily.get(day, {"known": 0, "dont": 0})
        return int(x.get("known", 0)), int(x.get("dont", 0))

    def get_counts_last_days(n: int):
        total_known = 0
        total_dont = 0
        for i in range(n):
            day = (datetime.now().date() - timedelta(days=i)).strftime("%Y-%m-%d")
            k, d = get_daily_counts(day)
            total_known += k
            total_dont += d
        return total_known, total_dont

    def refresh_stats_view():
        pool = build_training_pool()
        total_words = len(pool)

        k_today, d_today = get_daily_counts(today_key())
        total_today = k_today + d_today

        if total_today > 0:
            rate = int(round(100 * (k_today / total_today)))
        else:
            k7, d7 = get_counts_last_days(7)
            total7 = k7 + d7
            rate = int(round(100 * (k7 / total7))) if total7 > 0 else 0

        meta = ensure_training_meta()
        last_use = int(meta.get("last_use", 0))

        stat_total.value = f"📚 Всего слов: {total_words}"
        stat_today.value = f"✅ Сегодня выучено: {k_today}"
        stat_rate.value = f"🎯 Процент запоминания: {rate}%"
        stat_last.value = f"📅 Последнее использование: {human_day(last_use)}"

    stats_view = ft.Column(
        [
            ft.Text("📈 Статистика", size=22, weight="bold"),
            ft.Container(height=8),
            ft.Container(
                content=ft.Column([stat_total, stat_today, stat_rate, stat_last], spacing=10),
                padding=20,
                border_radius=16,
                bgcolor="#1f1f1f",
                border=ft.Border.all(1, ft.Colors.GREY_800),
            ),
            ft.OutlinedButton("Обновить", on_click=lambda e: (refresh_stats_view(), page.update())),
        ],
        spacing=12,
        expand=True,
    )

    # ---------------------------------------------
    # МЕНЮ (все функции в выпадающем меню)
    # ---------------------------------------------
    def menu_divider():
        return ft.PopupMenuItem(
            content=ft.Container(height=1, width=200, bgcolor=ft.Colors.GREY_700),
            disabled=True
        )

    mi_fav_toggle = ft.PopupMenuItem(content="Добавить в избранное", icon=ft.Icons.STAR_OUTLINE, on_click=toggle_favorite_searched_word)
    mi_fav_list = ft.PopupMenuItem(content="Открыть избранные", icon=ft.Icons.STAR, on_click=open_favorites_dialog)

    mi_speak = ft.PopupMenuItem(content="Озвучить слово", icon=ft.Icons.VOLUME_UP, on_click=start_speak_click)

    mi_view_all = ft.PopupMenuItem(content="Мой словарь", icon=ft.Icons.LIST_ALT, on_click=show_all_words)
    mi_history = ft.PopupMenuItem(content="История запросов", icon=ft.Icons.HISTORY, on_click=open_history_dialog)

    mi_backup = ft.PopupMenuItem(content="Создать бэкап", icon=ft.Icons.CLOUD_UPLOAD, on_click=handle_backup_click)
    mi_restore = ft.PopupMenuItem(content="Восстановить бэкап", icon=ft.Icons.CLOUD_DOWNLOAD, on_click=handle_restore_click)

    actions_menu = ft.PopupMenuButton(
        icon=ft.Icons.MENU,
        tooltip="Меню",
        items=[
            mi_fav_toggle,
            mi_fav_list,
            menu_divider(),
            mi_speak,
            menu_divider(),
            mi_view_all,
            mi_history,
            menu_divider(),
            mi_backup,
            mi_restore,
        ],
    )

    def refresh_menu_states():
        w = current_word()
        has_word = bool(w)
        is_fav = has_word and (w in favorites)

        mi_fav_toggle.disabled = not has_word
        mi_fav_toggle.icon = ft.Icons.STAR if is_fav else ft.Icons.STAR_OUTLINE
        mi_fav_toggle.icon_color = ft.Colors.AMBER if is_fav else ft.Colors.GREY_500
        mi_fav_toggle.content = "Убрать из избранного" if is_fav else "Добавить в избранное"

        mi_speak.disabled = not bool(current_audio_url.get("url"))

        # ⭐ “звезда в меню становится золотой”
        if is_fav:
            actions_menu.icon = ft.Icons.STAR
            actions_menu.icon_color = ft.Colors.AMBER
        else:
            actions_menu.icon = ft.Icons.MENU
            actions_menu.icon_color = None

    def on_search_change(e):
        refresh_menu_states()
        page.update()

    search_field.on_change = on_search_change

    # ---------------------------------------------
    # ВКЛАДКА "СЛОВАРЬ"
    # ---------------------------------------------
    dictionary_view = ft.Column(
        [
            ft.Row([ft.Text("Переводчик", size=24, weight="bold")], alignment=ft.MainAxisAlignment.CENTER),
            ft.Container(height=10),
            ft.Row([search_field, search_btn, actions_menu], alignment=ft.MainAxisAlignment.CENTER),
            progress_bar,
            results_column,
        ],
        expand=True,
    )

    # ---------------------------------------------
    # TABS (совместимо с Flet 0.80.x)
    # ---------------------------------------------
    tabs = ft.Tabs(
        length=3,
        selected_index=0,
        expand=True,
        content=ft.Column(
            expand=True,
            controls=[
                ft.TabBar(
                    tabs=[
                        ft.Tab(label="Словарь"),
                        ft.Tab(label="Тренировка"),
                        ft.Tab(label="📈 Статистика"),
                    ]
                ),
                ft.TabBarView(
                    expand=True,
                    controls=[
                        dictionary_view,
                        training_view,
                        stats_view,
                    ],
                ),
            ],
        ),
    )

    page.floating_action_button = ft.FloatingActionButton(
        icon=ft.Icons.ADD,
        bgcolor=ft.Colors.GREEN_400,
        on_click=handle_fab_click,
        tooltip="Добавить слово"
    )

    page.add(tabs)

    refresh_stats_view()
    refresh_menu_states()
    page.update()

    await training_load_next()


if __name__ == "__main__":
    ft.run(main)

