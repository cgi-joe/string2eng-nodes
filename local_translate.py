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
)

def get_models_and_prompt():
    try:
        import ollama
        try:
            from langchain_community.llms import Ollama
            try:
                llms = ollama.list()
                models = tuple(model['name'] for model in llms['models'])
                if len(models) > 0:
                    return models, "", True
                else:
                    return ("None Installed",), "To use this node, please run 'ollama pull llama2'", False
            except Exception as e:
                print(f"Error listing Ollama models: {e}")
                return ("None Installed",), "To use this node, please run 'ollama pull llama2'", False
        except ImportError:
            return ("None Installed",), "To use this node, please run 'pip install langchain-community'", False
    except ImportError:
        return ("None Installed",), "To use this node, please run 'pip install ollama'", False

OLLAMA_MODELS, DEFAULT_PROMPT, MODELS_AVAILABLE = get_models_and_prompt()

@invocation_output("LocalTranslateOutput")
class LocalTranslateOutput(BaseInvocationOutput):
    """Translated string output"""
    prompt: str = OutputField(default=None, description="The translated prompt string")

@invocation(
    "LocalTranslateInvocation",
    title="Local Translate",
    tags=["prompt", "translate", "ollama"],
    category="prompt",
    version="1.0.0",
)
class LocalTranslateInvocation(BaseInvocation):
    """Use the local Ollama model to translate text into English prompts"""

    # Inputs
    text: str = InputField(default=DEFAULT_PROMPT, description="Prompt in any language")
    model: Literal[OLLAMA_MODELS] = InputField(default=OLLAMA_MODELS[0], description="The Ollama model to use")

    def invoke(self, context: InvocationContext) -> LocalTranslateOutput:
        if not MODELS_AVAILABLE:
            return LocalTranslateOutput(prompt="")

        from langchain_community.llms import Ollama
        llm = Ollama(model=self.model, temperature=0)
        prompt = "Translate the following text, which will appear after a colon, into English. Do not respond with anything but the translation. Do not specify this is a translation. Only provide the translated text. Text:"
        user_input = self.text
        response = llm.invoke(prompt + user_input)[1:]
        return LocalTranslateOutput(prompt=response)