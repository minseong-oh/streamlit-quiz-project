# 간이 로그인
import hashlib
import json
from pathlib import Path

USERS_FILE = Path(__file__).resolve().parent.parent / "users.json"


def _hash(password):
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def _load_users():
    if not USERS_FILE.exists():
        return {}
    with USERS_FILE.open(encoding="utf-8") as f:
        return json.load(f)


def _save_users(users):
    with USERS_FILE.open("w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)


def verify(username, password):
    users = _load_users()
    user = users.get(username)
    if not user:
        return False
    return user.get("password") == _hash(password)


def register(username, password, nickname):
    username = username.strip()
    if not username or not password:
        return False, "아이디와 비밀번호를 모두 입력해주세요."
    if len(password) < 4:
        return False, "비밀번호는 4자 이상으로 설정해주세요."
    users = _load_users()
    if username in users:
        return False, "이미 존재하는 아이디예요."
    users[username] = {
        "password": _hash(password),
        "nickname": nickname.strip() or username,
    }
    _save_users(users)
    return True, "가입 완료! 이제 로그인해주세요."


def get_nickname(username):
    users = _load_users()
    return users.get(username, {}).get("nickname", username)
