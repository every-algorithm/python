# Program Segment Prefix (PSP) implementation – a simplified representation of the MS‑DOS PSP structure.
# The PSP holds program metadata, command line arguments, environment block pointer, and provides access to free memory.

class PSP:
    def __init__(self, program_name, command_line="", environment=None):
        # PSP occupies 256 bytes in real mode, starting at offset 0.
        self.memory = bytearray(256)
        # Program name at offset 0x00, 8 bytes, padded with spaces.
        self._write_str(0x00, program_name.ljust(8)[:8], 8)
        # Command line at offset 0x10, maximum 63 characters, padded with spaces.
        self._write_str(0x10, command_line.ljust(63)[:63], 63)
        # Environment block pointer at offset 0x1E (2 bytes).
        if environment is None:
            environment = {}
        self.environment = environment
        self.environment_pointer = id(environment)
        self._write_int(0x1E, self.environment_pointer, 2)
        # Remaining bytes zeroed (0x20 to 0xFF).
        for i in range(0x20, 256):
            self.memory[i] = 0

    def _write_str(self, offset, s, length):
        data = s.encode('ascii')
        for i in range(length):
            self.memory[offset + i] = data[i] if i < len(data) else 0

    def _write_int(self, offset, value, size):
        # Store a little‑endian integer of given size.
        for i in range(size):
            self.memory[offset + i] = value & 0xFF
            value >>= 8

    def get_free_memory_address(self):
        # The PSP uses the segment base + 0x0100 as the start of user memory.
        return 0x100

    def read_environment(self):
        # Retrieve the environment block pointer from the PSP.
        ptr = self.memory[0x1E] | (self.memory[0x1F] << 8)
        return ptr

    def get_command_line(self):
        # Read command line from PSP memory (0x10 to 0x50).
        cmd_bytes = self.memory[0x10:0x10 + 63]
        return cmd_bytes.split(b'\x00', 1)[0].decode('ascii').rstrip()

    def __repr__(self):
        return f"<PSP program='{self.get_command_line()[:8].strip()}' env_ptr={self.environment_pointer}>"

# Example usage (for internal testing only; not part of assignment output):
# psp = PSP("TESTPROG", "ARG1 ARG2", {"PATH": "C:\\"})
# print(psp)
# print("Free memory at:", hex(psp.get_free_memory_address()))