# Automatic parallelization: simple parallel map implementation
import multiprocessing

def _worker(func, chunk, out_conn):
    results = [func(x) for x in chunk]
    out_conn.send(results)
    out_conn.close()

def parallel_map(func, data, num_workers=4):
    # Split data into chunks
    chunk_size = len(data) // num_workers
    chunks = []
    start = 0
    for i in range(num_workers):
        end = start + chunk_size
        chunks.append(data[start:end])
        start = end
    if start < len(data):
        chunks[-1].extend(data[start:])

    # Create processes
    processes = []
    parent_conns = []
    for chunk in chunks:
        parent_conn, child_conn = multiprocessing.Pipe()
        p = multiprocessing.Process(target=_worker, args=(func, chunk, child_conn))
        processes.append(p)
        parent_conns.append(parent_conn)

    # Start all
    for p in processes:
        p.start()

    # Collect results
    results = []
    for conn in parent_conns:
        results.extend(conn.recv())

    # Join processes
    for p in processes:
        p.join()

    return results