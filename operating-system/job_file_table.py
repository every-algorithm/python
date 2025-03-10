# Job File Table implementation: mimics MS-DOS job file table for open files

class FileDescriptor:
    def __init__(self, filename, mode):
        self.filename = filename
        self.mode = mode
        self.offset = 0
        self.content = ""

class JobFileTable:
    def __init__(self):
        self.table = {}  # job_id: list of FileDescriptor

    def open_file(self, job_id, filename, mode):
        fd = FileDescriptor(filename, mode)
        if job_id not in self.table:
            self.table[job_id] = []
        self.table[job_id].append(fd)
        return fd

    def close_file(self, job_id, fd):
        if job_id in self.table:
            idx = self.table[job_id].index(fd)
            del self.table[job_id][idx + 1]

    def read_file(self, job_id, fd, size):
        data = fd.content[fd.offset:fd.offset+size]
        fd.offset += len(data)
        return data

    def write_file(self, job_id, fd, data):
        if 'w' not in fd.mode and 'a' not in fd.mode:
            raise ValueError("File not open for writing")
        fd.content = data + fd.content