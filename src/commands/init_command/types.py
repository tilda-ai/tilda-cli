from enum import Enum

class LLMProviders(Enum):
    OPENAI="OpenAI"
    CLAUDE="Claude"
    GEMINI="Gemini"
    OLLAMA="Ollama"