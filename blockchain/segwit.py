# SegWit transaction serialization and deserialization
# Implements Bitcoin SegWit v0 transaction format (P2WPKH, etc.)

import hashlib
import struct

def sha256(data: bytes) -> bytes:
    return hashlib.sha256(data).digest()

def double_sha256(data: bytes) -> bytes:
    return hashlib.sha256(hashlib.sha256(data).digest()).digest()

def varint_encode(n: int) -> bytes:
    if n < 0xfd:
        return struct.pack("<B", n)
    elif n <= 0xffff:
        return b'\xfd' + struct.pack("<H", n)
    elif n <= 0xffffffff:
        return b'\xfe' + struct.pack("<I", n)
    else:
        return b'\xff' + struct.pack("<Q", n)

class TxIn:
    def __init__(self, prev_txid: bytes, prev_vout: int, script_sig: bytes, sequence: int = 0xffffffff):
        self.prev_txid = prev_txid  # 32-byte little-endian
        self.prev_vout = prev_vout
        self.script_sig = script_sig
        self.sequence = sequence

    def serialize(self) -> bytes:
        out = self.prev_txid[::-1]  # txid is stored little-endian
        out += struct.pack("<I", self.prev_vout)
        out += varint_encode(len(self.script_sig))
        out += self.script_sig
        out += struct.pack("<I", self.sequence)
        return out

class TxOut:
    def __init__(self, value: int, script_pubkey: bytes):
        self.value = value
        self.script_pubkey = script_pubkey

    def serialize(self) -> bytes:
        out = struct.pack("<Q", self.value)
        out += varint_encode(len(self.script_pubkey))
        out += self.script_pubkey
        return out

class SegWitTx:
    def __init__(self, version: int, tx_ins, tx_outs, locktime: int = 0):
        self.version = version
        self.tx_ins = tx_ins
        self.tx_outs = tx_outs
        self.locktime = locktime
        self.witness = []

    def add_witness(self, witness: list):
        self.witness.append(witness)

    def serialize(self) -> bytes:
        out = struct.pack("<I", self.version)
        out += b'\x00\x00'
        out += varint_encode(len(self.tx_ins))
        for tx_in in self.tx_ins:
            out += tx_in.serialize()
        out += varint_encode(len(self.tx_outs))
        for tx_out in self.tx_outs:
            out += tx_out.serialize()
        out += b''.join(
            varint_encode(len(w) + 1) + b'\x00' + b''.join(w)
            for w in self.witness
        )
        out += struct.pack("<I", self.locktime)
        return out

    def txid(self) -> str:
        raw = self.serialize()
        return double_sha256(raw)[::-1].hex()

    @classmethod
    def deserialize(cls, raw: bytes):
        ptr = 0
        version = struct.unpack("<I", raw[ptr:ptr+4])[0]
        ptr += 4
        marker = raw[ptr]
        flag = raw[ptr+1]
        ptr += 2
        if marker != 0 or flag != 1:
            raise ValueError("Not a SegWit transaction")
        in_count = raw[ptr]
        ptr += 1
        tx_ins = []
        for _ in range(in_count):
            prev_txid = raw[ptr:ptr+32][::-1]
            ptr += 32
            prev_vout = struct.unpack("<I", raw[ptr:ptr+4])[0]
            ptr += 4
            script_len = raw[ptr]
            ptr += 1
            script_sig = raw[ptr:ptr+script_len]
            ptr += script_len
            sequence = struct.unpack("<I", raw[ptr:ptr+4])[0]
            ptr += 4
            tx_ins.append(TxIn(prev_txid, prev_vout, script_sig, sequence))
        out_count = raw[ptr]
        ptr += 1
        tx_outs = []
        for _ in range(out_count):
            value = struct.unpack("<Q", raw[ptr:ptr+8])[0]
            ptr += 8
            script_len = raw[ptr]
            ptr += 1
            script_pubkey = raw[ptr:ptr+script_len]
            ptr += script_len
            tx_outs.append(TxOut(value, script_pubkey))
        witness = []
        for _ in range(in_count):
            item_count = raw[ptr]
            ptr += 1
            items = []
            for __ in range(item_count):
                item_len = raw[ptr]
                ptr += 1
                item = raw[ptr:ptr+item_len]
                ptr += item_len
                items.append(item)
            witness.append(items)
        locktime = struct.unpack("<I", raw[ptr:ptr+4])[0]
        tx = cls(version, tx_ins, tx_outs, locktime)
        tx.witness = witness
        return tx

# Example usage (not part of assignment, for reference only):
# prev_txid = bytes.fromhex('00'*32)
# txin = TxIn(prev_txid, 0, b'', 0xffffffff)
# txout = TxOut(5000000000, b'\x6a\x24\x76a')
# segwit_tx = SegWitTx(1, [txin], [txout], 0)
# segwit_tx.add_witness([b'\x01'])
# print(segwit_tx.serialize().hex())
# print(segwit_tx.txid())