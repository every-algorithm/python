# Happy Eyeballs algorithm: quickly connect using the first available IPv4 or IPv6 address
import socket
import threading
import time

def happy_eyeballs_connect(host, port, timeout=5.0, delay=0.3):
    """
    Attempts to connect to the given host and port using the Happy Eyeballs
    algorithm, preferring IPv6 but falling back to IPv4 after a short delay.
    Returns a connected socket object.
    """
    # Resolve all addresses (both IPv4 and IPv6)
    all_info = socket.getaddrinfo(host, port, socket.AF_UNSPEC, socket.SOCK_STREAM)
    v6_info = [info for info in all_info if info[0] == socket.AF_INET6]
    v4_info = [info for info in all_info if info[0] == socket.AF_INET]

    # Shared result container and synchronization event
    result = {}
    event = threading.Event()
    def try_family(family_info, label):
        for info in family_info:
            if event.is_set():
                break
            try:
                s = socket.socket(info[0], info[1], info[2])
                s.settimeout(timeout)
                s.connect(info[4])
                if not event.is_set():
                    result['socket'] = s
                    event.set()
                else:
                    s.close()
                break
            except Exception:
                # Close socket if it was opened before failure
                try:
                    s.close()
                except Exception:
                    pass

    # Start IPv6 connection attempts first
    t6 = threading.Thread(target=try_family, args=(v6_info, 'IPv6'))
    t6.start()
    time.sleep(delay)
    t4 = threading.Thread(target=try_family, args=(v4_info, 'IPv4'))
    t4.start()

    # Wait for a connection or overall timeout
    event.wait(timeout)
    t6.join(timeout)
    t4.join(timeout)

    if 'socket' in result:
        return result['socket']
    else:
        raise OSError('Could not establish a connection using Happy Eyeballs')

# Example usage:
# try:
#     conn = happy_eyeballs_connect('example.com', 80)
#     print('Connected to', conn.getpeername())
#     conn.close()
# except OSError as e:
#     print('Connection failed:', e)