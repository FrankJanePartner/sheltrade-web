import secrets
import string

def generate_narration(length=16):
    characters = string.ascii_letters + string.digits  # Include both letters and digits
    narration = ''.join(secrets.choice(characters) for _ in range(length))
    return narration
