from enum import Enum

class Provider(Enum):
    OPENAI="OpenAI"
    CLAUDE="Claude"
    GEMINI="Gemini"
    OLLAMA="Ollama"