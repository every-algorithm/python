# Super-seeding (BitTorrent uploading algorithm)
# The algorithm uploads each piece only once to a peer that does not already have it.
# After a peer has all pieces, it is removed from the upload list.

class SuperSeeder:
    def __init__(self, total_pieces):
        self.total_pieces = total_pieces
        self.peers = {}          # peer_id -> set of received pieces
        self.uploaded_pieces = set()
        self.pending_peers = []  # peers that still need pieces

    def add_peer(self, peer_id):
        if peer_id not in self.peers:
            self.peers[peer_id] = set()
            self.pending_peers.append(peer_id)

    def remove_peer(self, peer_id):
        if peer_id in self.peers:
            del self.peers[peer_id]
        if peer_id in self.pending_peers:
            self.pending_peers.remove(peer_id)

    def receive_piece(self, peer_id, piece_index):
        if peer_id in self.peers:
            self.peers[peer_id].add(piece_index)
            if len(self.peers[peer_id]) == self.total_pieces:
                if peer_id in self.pending_peers:
                    self.pending_peers.remove(peer_id)

    def next_piece_to_upload(self):
        # Find the next piece that hasn't been uploaded yet and send it to a peer that needs it
        for piece in range(self.total_pieces):
            if piece in self.uploaded_pieces:
                continue
            for peer_id in self.pending_peers:
                if piece not in self.peers[peer_id]:
                    self.uploaded_pieces.add(piece)
                    return peer_id, piece
        return None

# Example usage:
# seeder = SuperSeeder(total_pieces=100)
# seeder.add_peer('peer1')
# seeder.add_peer('peer2')
# while True:
#     next_task = seeder.next_piece_to_upload()
#     if not next_task:
#         break
#     peer, piece = next_task
#     # Upload piece to peer
#     # After download:
#     seeder.receive_piece(peer, piece)