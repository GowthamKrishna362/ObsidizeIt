from langchain_ollama import OllamaLLM
from langchain_core.messages import SystemMessage, HumanMessage
from prompts import SUMMARY_PROMPT
from utils import get_lock_for_file, append_to_file

def handle_obsidize(text, file):
    file_lock = get_lock_for_file(file)
    with file_lock:
        print(f"Obsidizing text for file '{file}': " + text)
        model = OllamaLLM(model="mistral")
        messages = [
            SystemMessage(SUMMARY_PROMPT),
            HumanMessage(text),
        ]
        response = model.invoke(messages)
        print(f"Response for file '{file}': " + response)
        append_to_file(file, response)
        return response



