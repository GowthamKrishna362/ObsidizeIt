import threading
file_locks = {}
locks_dict_lock = threading.Lock()

def get_lock_for_file(file):
    with locks_dict_lock:
        if file not in file_locks:
            file_locks[file] = threading.Lock()
        return file_locks[file]


def append_to_file(file, text):
    print(f"Appending to file '{file}': " + text)
    with open(file, 'a') as f:
        f.write(text)