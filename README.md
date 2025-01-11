# LLMs-with-Autodesk-Dynamo-Python

<img src="https://raw.githubusercontent.com/DynamoDS/Dynamo/master/doc/distrib/Images/dynamo_logo_dark.png" width="300"/> <img src="https://www.nomic.ai/gpt4all/gpt4all_word.svg" width="300"/> <img src="https://chunte-hfba.static.hf.space/images/Brand%20Logos/hf-logo-with-white-title.png" width="300"/>

## Description

Discover a new level of efficiency and innovation with our latest workflow that seamlessly integrates (Large Language Models) LLMs, Using GPT4ALL and HuggingFace -a free and open-source AI python libraries and model- with Autodesk products. Our approach leverages the power of Python to bring advanced AI capabilities to your favorite design and engineering tools.

In our initial release, we've focused on Dynamo for Autodesk Revit, enabling users to harness the potential of AI-driven automation and intelligence within their Revit projects. 
With GPT4All running on your local machine, you can experience smarter workflows, faster decision-making, and enhanced project outcomes—all while ensuring your data stays secure as the model is saved directly to your system.

In our second attempt, we explored HuggingFace libraries. These can also be set up to run locally [Link](https://discuss.huggingface.co/t/using-huggingface-on-no-free-internet-access-server/11202/2). or calling out to the online model by Signing up to [Huggingface.co](https://huggingface.co/join) ,and using [User Access Token](https://huggingface.co/docs/hub/en/security-tokens)  

Explore the possibilities with LLMs and elevate your Autodesk experience to new heights. 

## Prerequisites

- **Revit 2023 or Civil 3D**
- **Dynamo 2+**
- **Cpython** - Script uses Cpython , will look to provide code in Ironpython 2.7 (if possible), and the new [Pythonnet3 ](https://dynamobim.org/pythonnet3-a-new-dynamo-python-to-fix-everything/)
- **GPT4All -** https://github.com/nomic-ai/gpt4all
- **Huggingface** - (optional) https://huggingface.co/
- **Smolagents** - (optional) [https://github.com/huggingface/smolagents](https://github.com/huggingface/smolagents) - An Autonomous Agent that can Search the Web to Create app (Experimental)
  
## Installation

### Open Revit and Dynamo

1. **Launch Revit 2023+, Civil 3D Dynamo Sandbox**.
2. **Open  a New project in Dynamo 2** within Revit and place a CPython node, to create the python embedded folders

### 2. Setup Dynamo CPython Custom Module

Use the following link -  for a detail guide on how to install custom python modules https://github.com/DynamoDS/Dynamo/wiki/Customizing-Dynamo's-Python-3-installation

1. **Download the `Getpip.py` file** from here -https://pip.pypa.io/en/stable/installation/#get-pip-py
2. **Place the file** in the specified Dynamo's cPython home. eg C:\Users\%USERNAME%\AppData\Local\python-3.9.12-embed-amd64\
3. **Run the file** to install pip.

### 3. Install GPT4All Module and Custom Modules

1. **Run the Dynamo script** to install required custom modules - [PY - InstallCustomPythonModules.dyn ](https://github.com/kneelster111/Gpt4all-Autodesk-Dynamo-Python/blob/main/PY%20-%20InstallCustomPythonModules.dyn)
2. **open python.Exe** from the Dynamo Python home folder this will open the python idle 
3. **Install the GPT4All Library**  inside the idle install GPT4All modules using pip:`pip install gpt4all`
4. **Install the HuggingFace Library**  inside the idle install GPT4All modules using pip:`pip install huggingface` (optional)
5. **Install the smolagents Library**  inside the idle install GPT4All modules using pip:`pip install smolagents`(optional)

### 5. Download Model Files and Use GPT4All in Python

1. **Download the `model.bim` files** from the source location. These are large file 3+ Gb. 
2. **Set up LLMs** using the llama.cpp and Nomic's C backends. These tools make LLMs more accessible and efficient.
3. **Example code**: **Python**


```
from gpt4all import GPT4All

model = GPT4All("Meta-Llama-3-8B-Instruct.Q4_0.gguf")  # downloads / loads a 4.66GB LLM
with model.chat_session():
    print(model.generate("How can I run LLMs efficiently on my laptop?", max_tokens=1024))`
```
4.  **HuggingFace LOGIN** - Optionally If you want to test the Hugging Face script, you will first need to Signup and log in to your Hugging Face account. After logging in, provide your access token in the python.exe script.

```
from huggingface import login
login("insert user token")
model = GPT4All("Meta-Llama-3-8B-Instruct.Q4_0.gguf")  # downloads / loads a 4.66GB LLM
with model.chat_session():
    print(model.generate("How can I run LLMs efficiently on my laptop?", max_tokens=1024))`
```

### 6. GPT4ALL Assistant Dynamo Files

1. Download the Sample files to test using the links below-  
## Sample Scripts
  1. Simple Dynamo Player Chat Bot. - [GPT4All_Chatbot_1_DynPlayer](https://github.com/kneelster111/Gpt4all-Autodesk-Dynamo-Python/blob/main/GPT4all_DynamoScripts/PY%20-%20GPT4All_Chatbot_1_DynPlayer_.dyn)
  2. Chat bot; with WinForms UI with Conversation History - [Sample Image ](https://github.com/kneelster111/Gpt4all-Autodesk-Dynamo-Python/blob/main/Images/ChaBot_UI_Simple1.png)
  3. Chat bot; CodeAgent With Read and write data - [Sample Image ](https://github.com/kneelster111/Gpt4all-Autodesk-Dynamo-Python/blob/main/Images/ChaBot_UI_Winforms_Complex1.png)
  4. Chat bot; MVVM with WPF UI for CodeAgent - [WIP](https://github.com/kneelster111/Gpt4all-Autodesk-Dynamo-Python/discussions/2#discussion-7806619)

## Sample Use

### Demo Video
Below is a demonstration of how to use the app:

[![Watch the video](https://img.youtube.com/vi/GRdxeCw3Ovg/0.jpg)](https://youtu.be/GRdxeCw3Ovg)

This video shows the app in action, using huggingface, including basic usage and features.

### Examples of Use Cases

  1. How to Find Revit Commands
  2. Create a Wall/Element
  3. Move an Element
  4. Create Dynamo Geometry

## Future Implementations and Ideas

1. Custom LocalDocs, Embeddings, and Fine-Tuning Model Data: Implementing custom local documents and embeddings using Nomic.aito enhance data integration and accessibility, while continuously refining and fine-tuning model data to improve accuracy and performance.
2. PyRevit Integration: Extending our capabilities by integrating PyRevit, offering seamless automation and customization within Revit.
3. Additional Dynamo Script Features: Expanding the functionality of Dynamo scripts with new features and improvements to streamline workflows.
4. User Feedback & Adaptive Learning: Leveraging user feedback to drive adaptive learning and ensure our system evolves based on real-world use.

## Contributing

We welcome contributions, involvement, and discussion from the open-source community! Feel free to fork the repository, improve the code, and submit merge requests. We also encourage opening discussions on the Discussions tab.
When contributing, please adhere to the following guidelines:
  Follow Common Coding standards, add relavant Comments.
  Use clear and descriptive commit messages that follow standard Commit Message Conventions.
  Ensure your contributions are well-documented and include relevant comments.

We appreciate your efforts and look forward to your contributions! Let's make this project even better together.

##Disclaimer and License

### License
This project is licensed under the Creative Commons Attribution-NonCommercial (CC BY-NC) license, allowing modification and redistribution for non-commercial purposes only, with attribution to the original author. The code is experimental and provided "as is" with no warranty. Use at your own risk. More info.

### Disclaimer
This code is experimental and may not be suitable for production environments. The author provides no guarantees regarding its reliability or performance. By using this code, you acknowledge and accept the risks involved, and you are solely responsible for any issues that arise from its use. The code is provided "as is" without any warranty, either express or implied.


