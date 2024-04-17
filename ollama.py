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

@invocation_output("OllamaResponseOutput")
class OllamaResponseOutput(BaseInvocationOutput):
    """Ollama response output"""
    Response: str = OutputField(default=None, description="The response from the Ollama model")

@invocation(
    "OllamaInvocation",
    title="Ollama Invocation",
    tags=["prompt", "ollama"],
    category="prompt",
    version="1.0.0",
)
class OllamaInvocation(BaseInvocation):
    """Use the local Ollama model to generate responses based on a prompt and temperature"""
    # Inputs
    prompt: str = InputField(default=DEFAULT_PROMPT, description="Prompt for the Ollama model", ui_component=UIComponent.Textarea)
    temperature: float = InputField(default=0.7, description="The temperature to use for the Ollama model")
    model: Literal[OLLAMA_MODELS] = InputField(default=OLLAMA_MODELS[0], description="The Ollama model to use")

    def invoke(self, context: InvocationContext) -> OllamaResponseOutput:
        if not MODELS_AVAILABLE:
            return OllamaResponseOutput(value="")

        llm = Ollama(model=self.model, temperature=self.temperature)
        response = llm.invoke(self.prompt)
        return OllamaResponseOutput(value=response.strip())