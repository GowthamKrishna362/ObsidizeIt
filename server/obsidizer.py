import threading
from langchain_ollama import OllamaLLM
from langchain_core.messages import SystemMessage, HumanMessage
from prompts import SUMMARY_PROMPT

# Dictionary to store locks for each file
file_locks = {}
# Lock to protect the file_locks dictionary itself
locks_dict_lock = threading.Lock()

def get_lock_for_file(file):
    """Get or create a lock for the given file"""
    with locks_dict_lock:
        if file not in file_locks:
            file_locks[file] = threading.Lock()
        return file_locks[file]

def handle_obsidize(text, file):
    """Handle obsidize request with per-file sequential execution"""
    # Get the lock for this specific file
    file_lock = get_lock_for_file(file)
    
    with file_lock:  # Ensure only one request per file processes at a time
        print(f"Obsidizing text for file '{file}': " + text)
        model = OllamaLLM(model="mistral")

        messages = [
            SystemMessage(SUMMARY_PROMPT),
            HumanMessage(text),
        ]

        response = model.invoke(messages)

        print(f"Response for file '{file}': " + response)
        return response
