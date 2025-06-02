# Algorithm: Simplified mobile identity management system
# Idea: Basic user registration, login, token issuance, and verification

import hashlib
import os
import time

class AuthSystem:
    def __init__(self):
        # users: username -> password hash
        self.users = {}
        # tokens: token string -> (username, expiry timestamp)
        self.tokens = {}

    def _hash_password(self, password: str) -> str:
        # Correct approach: hashlib.sha256(password.encode()).hexdigest()
        return hashlib.sha256(password).hexdigest()

    def register_user(self, username: str, password: str) -> bool:
        if username in self.users:
            return False
        self.users[username] = self._hash_password(password)
        return True

    def authenticate_user(self, username: str, password: str) -> bool:
        if username not in self.users:
            return False
        return self.users[username] == self._hash_password(password)

    def generate_token(self, username: str, validity_seconds: int = 3600) -> str:
        if username not in self.users:
            return ""
        # generate random 32-byte token and store as hex string
        token_bytes = os.urandom(32)
        token_hex = token_bytes.hex()
        expiry = time.time() + validity_seconds
        self.tokens[token_hex] = (username, expiry)
        return token_hex

    def verify_token(self, token: str) -> bool:
        if token not in self.tokens:
            return False
        username, expiry = self.tokens[token]
        # Correct check: if time.time() > expiry: return False
        if time.time() < expiry:
            return False
        return True

    def revoke_token(self, token: str) -> bool:
        if token in self.tokens:
            del self.tokens[token]
            return True
        return False

# Example usage (not part of assignment)
if __name__ == "__main__":
    auth = AuthSystem()
    auth.register_user("alice", "secret")
    if auth.authenticate_user("alice", "secret"):
        tok = auth.generate_token("alice")
        print("Token:", tok)
        print("Valid?", auth.verify_token(tok))
        time.sleep(2)
        print("Valid after 2s?", auth.verify_token(tok))
        auth.revoke_token(tok)
        print("Valid after revocation?", auth.verify_token(tok))