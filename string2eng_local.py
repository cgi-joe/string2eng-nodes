# Copyright (c) 2024 Joseph E. Kubler

from typing import Literal
from invokeai.app.invocations.baseinvocation import (
    BaseInvocation,
    BaseInvocationOutput,
    InvocationContext,
    invocation,
    invocation_output,
)
from invokeai.app.invocations.fields import (
    InputField,
    OutputField,
    UIComponent,
)

DEFAULT_PROMPT = ""
OLLAMA_AVAILABLE = False
LANGCHAIN_COMMUNITY_AVAILABLE = False
MODELS_AVAILABLE = False
OLLAMA_MODELS = ("None Installed",)

try:
    import ollama
    OLLAMA_AVAILABLE = True
except ImportError:
    DEFAULT_PROMPT = "To use this node, please run 'pip install ollama'"

if OLLAMA_AVAILABLE:
    try:
        from langchain_community.llms import Ollama
        LANGCHAIN_COMMUNITY_AVAILABLE = True
    except ImportError:
        DEFAULT_PROMPT = "To use this node, please run 'pip install langchain-community'"

if OLLAMA_AVAILABLE and LANGCHAIN_COMMUNITY_AVAILABLE:
    try:
        llms = ollama.list()
        OLLAMA_MODELS = tuple(model['name'] for model in llms['models'])
        if len(OLLAMA_MODELS) > 0:
            MODELS_AVAILABLE = True
        else:
            OLLAMA_MODELS = ("None Installed",)
            DEFAULT_PROMPT = "To use this node, please run 'ollama pull llama2'"
    except Exception as e:
        OLLAMA_MODELS = ("None Installed",)
        DEFAULT_PROMPT = "To use this node, please run 'ollama pull llama2'"

@invocation_output("Str2EngLocalOutput")
class Str2EngLocalOutput(BaseInvocationOutput):
    """Translated string output"""
    value: str = OutputField(default=None, description="The translated prompt string")

@invocation(
    "StringToEnglishLocalInvocation",
    title="String to English (Local LLM)",
    tags=["prompt", "translate", "ollama"],
    category="prompt",
    version="1.0.0",
)
class Str2EngLocalInvocation(BaseInvocation):
    """Use the local Ollama model to translate text into English prompts"""

    # Inputs
    value: str = InputField(default=DEFAULT_PROMPT, description="Prompt in any language", ui_component=UIComponent.Textarea)
    model: Literal[OLLAMA_MODELS] = InputField(default=OLLAMA_MODELS[0], description="The Ollama model to use")

    def invoke(self, context: InvocationContext) -> Str2EngLocalOutput:
        if not MODELS_AVAILABLE:
            return Str2EngLocalOutput(prompt="")

        llm = Ollama(model=self.model, temperature=0)
        prompt = "Translate the following text, which will appear after a colon, into English. Do not respond with anything but the translation. Do not specify this is a translation. Only provide the translated text. Text:"
        user_input = self.value
        response = llm.invoke(prompt + user_input)
        return Str2EngLocalOutput(value=response.strip())