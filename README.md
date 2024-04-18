# String Manipulation Nodes

The following are 3 nodes for translation text generation in [InvokeAI](https://github.com/invoke-ai/InvokeAI). There are 2 nodes here for translating text strings to English. One uses the [python translators library](https://pypi.org/project/translators/#description), which requires making remote API calls to translation services such as Google or Bing. The other uses [Ollama](https://ollama.com/), allowing users to host their own LLMs locally to provide a similiar service. The current prompt for translation can be found and edited in str2eng_local, but has been tested and shown to work generally well with the llama2 model. For more refined control over the prompt, in addition to other text generation uses, a seperate Ollama node with full prompt and temperature control also exist. To use the Ollama nodes, Ollama must be installed and registered to PATH. In addition, the [ollama](https://github.com/ollama/ollama-python) and [langchain-community](https://pypi.org/project/langchain-community/) python libraries must be installed. Luckily, the input fields of these nodes should provide hints if there are any issues.

## Translation Nodes
These nodes both take, as inputs, a string in any language. They are both intended to autodetect the input language. For both the remote and local versions, different services/models may perform better depending on the input language.

### String To English
![image](https://github.com/cgi-joe/string2eng-nodes/assets/8460254/d9640c95-f647-44bf-bf1d-4e9604b4474e)

Uses external API calls to servies like google and bing. 

```
pip install --upgrade translators
```

For more information, check out [python translators library](https://pypi.org/project/translators/#description).

### String to English (Local LLM)
![image](https://github.com/cgi-joe/string2eng-nodes/assets/8460254/3d6c0727-6bf0-4a27-b3a8-0163eb67c9ea)

Uses Ollama to translate locally, without the need for web API calls. Follow the instructions on [Ollama](https://ollama.com/)'s website for your operating system. Make sure you add Ollama to path. Additionally you will need to install the [ollama](https://github.com/ollama/ollama-python) and [langchain-community](https://pypi.org/project/langchain-community/) python libraries.

```
pip install --upgrade ollama
pip install --upgrade langchain-community
```

You will need at least one LLM downloaded to use the node. llama2 is reccomended, which can be downloaded with:
```
ollama pull llama2
```

Essentially, the input of this node is added to a prompt which instructs the LLM to provide the translation and only the translation as a response. This prompt can be modified in the string2eng_local.py file. However, you can also gain full control of the LLM by using the Ollama node below. 

## Ollama Node
![image](https://github.com/cgi-joe/string2eng-nodes/assets/8460254/d738e57f-0d65-440a-bc69-2f4826eda037)

The installation instructions are identical to String to English (Local LLM) above.

This node essentially offers everything the String to English (Local LLM) node does and more by offering a more complete control to the LLM's prompting. 
