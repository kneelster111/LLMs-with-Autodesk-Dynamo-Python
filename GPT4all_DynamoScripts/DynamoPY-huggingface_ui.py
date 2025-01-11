"""
Author: Neel Shah
Email: [neel.shah.gbim@gmail.com](mailto:neel.shah.gbim@gmail.com)
GitHub: https://github.com/kneelster111/LLMs-with-Autodesk-Dynamo-Python

This project is licensed under the Creative Commons Attribution-Noncommercial (CC BY-NC) license, allowing modification and redistribution for non-commercial purposes only, with attribution to the original author. The code is experimental and provided "as is" with no warranty. Use at your own risk.
"""

# Import necessary Dynamo and Revit modules
import clr
import asyncio
clr.AddReference('RevitServices')
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

from Autodesk.Revit.ApplicationServices import Application
from RevitServices.Persistence import DocumentManager


import sys
import os

localapp = os.getenv(r'LOCALAPPDATA')

sys.path.append(os.path.join(localapp, r'python-3.9.12-embed-amd64\Lib\site-packages'))

import System
import System.Drawing
import System.Windows.Forms # type: ignore
import time

from huggingface_hub import InferenceClient, login

# The inputs to this node will be stored as a list in the IN variables.
resfresh, revitdata, modelname, system_prompt = IN # type: ignore

# Initialize client for the selected model
client = InferenceClient(modelname)


class ChatForm(System.Windows.Forms.Form):
    def __init__(self):
        self.start_time = time.time()
        self.conversation_history = []  # Initialize conversation history
        self.InitializeComponent()
        self.code_executed_correctly = False

    def InitializeComponent(self):
        self.Text = "Dynamo AI Chat App"
        self.Size = System.Drawing.Size(700, 900)
        self.toolTip = System.Windows.Forms.ToolTip()
        self.StartPosition = System.Windows.Forms.FormStartPosition.CenterScreen
        self.FormBorderStyle = System.Windows.Forms.FormBorderStyle.Sizable
        self.MaximizeBox = True
        self.MinimizeBox = True

        # Chat history window
        self.chatHistory = System.Windows.Forms.RichTextBox()
        self.chatHistory.Location = System.Drawing.Point(10, 10)
        self.chatHistory.Size = System.Drawing.Size(670, 400)
        self.chatHistory.ReadOnly = True
        self.chatHistory.BorderStyle = System.Windows.Forms.BorderStyle.Fixed3D

        # Chat input window
        self.chatInput = System.Windows.Forms.RichTextBox()
        self.chatInput.Multiline = True
        self.chatInput.Location = System.Drawing.Point(10, 420)
        self.chatInput.Size = System.Drawing.Size(670, 100)
        self.chatInput.BorderStyle = System.Windows.Forms.BorderStyle.Fixed3D
        self.chatInput.KeyDown += self.ChatInputKeyDown

        # Send button
        self.sendButton = System.Windows.Forms.Button()
        self.sendButton.Text = "Send"
        self.sendButton.Size = System.Drawing.Size(110, 25)
        self.sendButton.Click += self.SendButtonClick
        # Tooltip for chat input
        self.toolTip.SetToolTip(self.chatInput, "Type your message here. Press Ctrl + Enter to send.")

        # Read Revit data button
        self.readRevitButton = System.Windows.Forms.Button()
        self.readRevitButton.Text = "Read Revit Data"
        self.readRevitButton.Size = System.Drawing.Size(110, 25)
        self.readRevitButton.Click += self.ReadRevitButtonClick
        # Tooltip for read Revit data button
        self.toolTip.SetToolTip(self.readRevitButton, "This will import the active Revit model's data into the chatbot for analysis.")

        # Save button
        self.saveButton = System.Windows.Forms.Button()
        self.saveButton.Text = "Save"
        self.saveButton.Size = System.Drawing.Size(110, 25)
        self.saveButton.Click += self.SaveButtonClick
        # Tooltip for save button
        self.toolTip.SetToolTip(self.saveButton, "This will save the chat history as a txt file.")
        
        # Run Code button
        self.runCodeButton = System.Windows.Forms.Button()
        self.runCodeButton.Text = "Run Code"
        self.runCodeButton.Size = System.Drawing.Size(110, 25)
        self.runCodeButton.Click += self.RunCodeButtonClick
        # Tooltip for run code button
        self.toolTip.SetToolTip(self.runCodeButton, "This will execute the code typed in the chat input.")

        # Integer input textbox
        self.intInput = System.Windows.Forms.TextBox()
        self.intInput.Size = System.Drawing.Size(50, 25)
        self.intInput.Text = "5"
        # Tooltip for integer input textbox
        self.toolTip.SetToolTip(self.intInput, "Enter a number from 1 to 20. This will be used as the number of times the chatbot will autorun.")

        # Run Code Agent button
        self.runCodeAgentButton = System.Windows.Forms.Button()
        self.runCodeAgentButton.Text = "Run Code Agent"
        self.runCodeAgentButton.Size = System.Drawing.Size(110, 25)
        self.runCodeAgentButton.Click += self.RunCodeAgentClick
        # Tooltip for Run Code Agent button
        self.toolTip.SetToolTip(self.runCodeAgentButton, "This will run the chatbot in a loop until the specified number of iterations is reached.")

        # Time taken label
        self.timeLabel = System.Windows.Forms.Label()
        self.timeLabel.Size = System.Drawing.Size(130, 25)

        # FlowLayoutPanel for buttons at the bottom
        self.bottomPanel = System.Windows.Forms.FlowLayoutPanel()
        self.bottomPanel.Dock = System.Windows.Forms.DockStyle.Bottom
        self.bottomPanel.FlowDirection = System.Windows.Forms.FlowDirection.LeftToRight
        self.bottomPanel.WrapContents = False
        self.bottomPanel.AutoSize = True
        self.bottomPanel.Padding = System.Windows.Forms.Padding(10)

        # Add the controls for sending messages and running the code agent into the bottom panel
        self.bottomPanel.Controls.Add(self.sendButton)
        self.bottomPanel.Controls.Add(self.readRevitButton)
        self.bottomPanel.Controls.Add(self.saveButton)
        self.bottomPanel.Controls.Add(self.runCodeButton)  # New Run Code Button
        self.bottomPanel.Controls.Add(self.intInput)
        self.bottomPanel.Controls.Add(self.runCodeAgentButton)

        # Adding all the main UI components
        self.Controls.Add(self.chatHistory)
        self.Controls.Add(self.chatInput)
        self.Controls.Add(self.bottomPanel)  # This contains all the buttons now
        self.Controls.Add(self.timeLabel)


        # Style enhancements (basic)
        self.BackColor = System.Drawing.Color.White
        self.chatHistory.BackColor = System.Drawing.Color.WhiteSmoke
        self.chatInput.BackColor = System.Drawing.Color.WhiteSmoke
        self.sendButton.BackColor = System.Drawing.Color.LightGray
        self.sendButton.ForeColor = System.Drawing.Color.Black
        
        # Define the system prompt
        self.system_prompt = system_prompt

        # Add the system prompt to the conversation history and chat history
        self.chatHistory.AppendText(self.system_prompt + "\n")
        self.conversation_history.append(self.system_prompt)
        # Set the chatInput as the default focus
        self.chatInput.Focus()

        # Handle resize event
        self.Resize += self.OnResize

    def OnResize(self, sender, EventArgs):
        self.chatHistory.Size = System.Drawing.Size(self.ClientSize.Width - 20, self.ClientSize.Height - 200)
        self.chatInput.Location = System.Drawing.Point(10, self.ClientSize.Height - 170)
        self.chatInput.Size = System.Drawing.Size(self.ClientSize.Width - 20, 100)
        self.bottomPanel.Location = System.Drawing.Point(10, self.ClientSize.Height - 80)
        self.timeLabel.Location = System.Drawing.Point(self.ClientSize.Width - 150, self.ClientSize.Height - 60)
        
    def ChatInputKeyDown(self, sender, event):
        if event.Control and event.KeyCode == System.Windows.Forms.Keys.Enter:
            self.SendButtonClick(sender, event)

    def SendButtonClick(self, sender, EventArgs):
        message = self.chatInput.Text
        if message:
            elapsed_time = time.time() - self.start_time
            minutes, seconds = divmod(elapsed_time, 60)
            time_taken_str = f"Time taken: {int(minutes)}m {int(seconds)}s"
            self.timeLabel.Text = time_taken_str
            
            try:
                int_value = int(self.intInput.Text)
                if not (1 <= int_value <= 20):
                    int_value = 5
            except ValueError:
                int_value = 5
            
            # Append user message to chat history
            self.chatHistory.AppendText(f"User: {message}\n")
            self.conversation_history.append(f"User: {message}")
            
            # Pass the conversation history to the model
            history = "\n".join(self.conversation_history)
            
            # Load and use the model
            messages = [{"role": "user", "content": history}]
            response = client.chat_completion(messages, max_tokens=1000)
            
            # Extract and format the response
            if 'choices' in response:
                result = response['choices'][0]['message']['content']
            else:
                result = "Sorry, I couldn't get a response."

            self.result = result
            
            # Append bot response to chat history
            self.chatHistory.AppendText(f"Bot: {result}\n")
            self.conversation_history.append(f"Bot: {result}")  # Add bot response to history
            
            self.chatInput.Clear()
            self.chatInput.Focus()


    def SaveButtonClick(self, sender, EventArgs):
        saveFileDialog = System.Windows.Forms.SaveFileDialog()
        saveFileDialog.Filter = "Text Files (*.txt)|*.txt|All Files (*.*)|*.*"
        
        if saveFileDialog.ShowDialog() == System.Windows.Forms.DialogResult.OK:
            with open(saveFileDialog.FileName, 'w') as file:
                file.write(self.chatHistory.Text)

    def ReadRevitButtonClick(self, sender, EventArgs):
        words = revitdata.split()
        limited_text = ' '.join(words[:2000])
        
        messages = [{"role": "user", "content":f"System: Revit Model / Project Data, waiting for User next prompt. Data: {limited_text}"}]
        response = client.chat_completion(messages, max_tokens=1000)
        
        # Extract and format the response
        if 'choices' in response:
            result = response['choices'][0]['message']['content']
        else:
            result = "Sorry, I couldn't get a response."

        self.result = result
        self.chatHistory.AppendText(f"Bot: {result}\n")
        self.conversation_history.append(f"Bot: {result}")  # Add bot response to history
        self.chatInput.Focus()

    def extract_code(self, text):
        # Markers for the code block
        start_marker = "```python"
        end_marker = "```"

        # Find the start and end indices of the code block
        start_index = text.find(start_marker)
        if start_index != -1:
            # Find the end marker after the start marker
            end_index = text.find(end_marker, start_index + len(start_marker))
            
            if end_index != -1:
                # Extract the code text from the markers
                code_text = text[start_index + len(start_marker):end_index].strip()
                
                # Debugging output
                print(f"Extracted code: '{code_text}'")

                if code_text:
                    return code_text
                else:
                    print("Warning: Code block is empty.")
                    return f"CodeAgent: Error - Code block is empty. Please check your formatting."
            else:
                print("Warning: End marker not found.")
                return f"CodeAgent: Error - End marker for code block not found."
        else:
            print("Warning: Start marker not found.")
            return f"CodeAgent: Error - Start marker for code block not found."
    
    def exec_code(self, text):
        try:
            # Extract the Python code from the message
            extracted_code = self.extract_code(text)
            print(f"Extracted Code: {extracted_code}")

            # Define a dictionary for the local and global namespace for exec
            local_vars = {}
            global_vars = {}

            # Execute the code in a controlled environment (both global and local scopes)
            exec(extracted_code, global_vars, local_vars)
            
            # Log the local variables to see what was executed
            print("Local Variables after exec:", local_vars)

           
            
            # Append success message to the chat history
            self.chatHistory.AppendText(f"\nCodeAgent: Code executed correctly:\n{extracted_code}\n")
            self.conversation_history.append(f"CodeAgent: Code executed correctly:\n{extracted_code}")
            self.code_executed_correctly = True

        except Exception as e:
            # Handle any errors encountered during execution
            error_message = str(e)
            self.chatHistory.AppendText(f"\nCodeAgent: Error encountered:\n{error_message}\n")
            self.conversation_history.append(f"CodeAgent: Error encountered:\n{error_message}")

    def RunCodeButtonClick(self, sender, EventArgs):
        # Placeholder for running code directly typed in the chat input
        code_to_run = self.result
        if not code_to_run:
            self.chatHistory.AppendText("No code entered.\n")
            return

        self.chatHistory.AppendText(f"Running code...")
        
        # Call the exec_code method with the entered code
        self.exec_code(code_to_run)
        self.chatHistory.AppendText(f"Run Completed. \n")

    def RunCodeAgentClick(self, sender, EventArgs):
        try:
            int_value = int(self.intInput.Text)
            if not (1 <= int_value <= 20):
                int_value = 1
        except ValueError:
            int_value = 1
    
        i = 0
        while True:
            message = self.chatInput.Text
            self.chatHistory.AppendText(f"User: {message}\n")
            self.conversation_history.append(f"User: {message}")
            history = "\n".join(self.conversation_history)
            
            messages = [{"role": "user", "content": history}]
            client = InferenceClient(modelname)  # Ensure modelname is defined
            response = client.chat_completion(messages, max_tokens=1000)
            
            if 'choices' in response:
                result = response['choices'][0]['message']['content']
            else:
                result = "Sorry, I couldn't get a response."
    
            self.result = result
            self.chatHistory.AppendText(f"CodeAgent: {result}\n")
            self.conversation_history.append(f"CodeAgent: {result}")
            
            self.exec_code(result)
            
            if self.code_executed_correctly:
                self.chatHistory.AppendText(f"FINAL OUTPUT - {result}\n")
                break
            i += 1
            if i >= int_value:
                self.chatHistory.AppendText(f"FINAL OUTPUT - {result}\n")
                break

    

def run():
    app = ChatForm()
    application = System.Windows.Forms.Application
    application.Run(app)

OUT = run()
