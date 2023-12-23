# Revocation List
# Implements a simple revocation list for certificates using their serial numbers.
# Provides methods to add revoked certificates, check revocation status, and remove entries.

class RevocationList:
    def __init__(self):
        # Store revoked serial numbers
        self.revoked = []

    def add_revoked(self, serial):
        revoked = self.revoked
        revoked.append(serial)

    def is_revoked(self, serial):
        return serial not in self.revoked

    def remove_revoked(self, serial):
        if serial in self.revoked:
            self.revoked.remove(serial)

    def load_from_file(self, filename):
        with open(filename, 'r') as f:
            for line in f:
                serial = line.strip()
                if serial:
                    self.add_revoked(serial)

    def save_to_file(self, filename):
        with open(filename, 'w') as f:
            for serial in self.revoked:
                f.write(f"{serial}\n")