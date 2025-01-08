# Gpt4all-Autodesk-Dynamo-Python
## Description

Discover a new level of efficiency and innovation with our latest workflow that seamlessly integrates GPT4All, a free and open-source AI chatbot and model, with Autodesk products. Our groundbreaking approach leverages the power of Python to bring advanced AI capabilities to your favorite design and engineering tools.

In our initial release, we've focused on Dynamo for Autodesk Revit, enabling users to harness the potential of AI-driven automation and intelligence within their Revit projects. With GPT4All running on your local machine, you can experience smarter workflows, faster decision-making, and enhanced project outcomes—all while ensuring your data stays secure as the model is saved directly to your system.

Explore the possibilities with GPT4All and elevate your Autodesk experience to new heights. Visit Nomic AI to learn more.


## Prerequisites

- **Revit 2023 or Civil 3D**
- **Dynamo 2+**
- **GPT4All -** https://github.com/nomic-ai/gpt4all
  
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

1. **Run the Dynamo script** to install required custom modules - PY - InstallCustomPythonModules.dyn https://github.com/kneelster111/Gpt4all-Autodesk-Dynamo-Python/blob/main/PY%20-%20InstallCustomPythonModules.dyn
2. open python. Exe from the Dynamo Python home folder this will open the python idle 
3. **Install the GPT4All module**  inside the idle install GPT4All modules using pip:`pip install gpt4all`

### 5. Download Model Files and Use GPT4All in Python

1. **Download the `model.bim` files** from the source location. These are large file 3+ Gb. 
2. **Set up LLMs** using the llama.cpp and Nomic's C backends. These tools make LLMs more accessible and efficient.
3. **Example code**: **Python**

`from gpt4all import GPT4All

model = GPT4All("Meta-Llama-3-8B-Instruct.Q4_0.gguf")  # downloads / loads a 4.66GB LLM
with model.chat_session():
    print(model.generate("How can I run LLMs efficiently on my laptop?", max_tokens=1024))`

### 6. GPT4ALL Assistant Dynamo File

1. Download the file using the link below, 

## Usage


## ## Examples Uses

How to use and Where to find Revit Commands 

Create a Wall/ Element
Move an Element
Create Dynamo Geometry

## Future Implementations and Ideas

Custom LocalDocs, Embeddings, and Fine-Tuning Model Data: Implementing custom local documents and embeddings using Nomic.aito enhance data integration and accessibility, while continuously refining and fine-tuning model data to improve accuracy and performance.
PyRevit Integration: Extending our capabilities by integrating PyRevit, offering seamless automation and customization within Revit.
Additional Dynamo Script Features: Expanding the functionality of Dynamo scripts with new features and improvements to streamline workflows.
User Feedback & Adaptive Learning: Leveraging user feedback to drive adaptive learning and ensure our system evolves based on real-world use.

## Contributing

We welcome contributions, involvement, and discussion from the open-source community! Feel free to fork the repository, improve the code, and submit merge requests. We also encourage opening discussions on the Discussions tab.
When contributing, please adhere to the following guidelines:
  Follow the coding standards specified in our Coding Standards Guide.
  Use clear and descriptive commit messages that follow our Commit Message Conventions.
  Ensure your contributions are well-documented and include relevant comments.

We appreciate your efforts and look forward to your contributions! Let's make this project even better together.
