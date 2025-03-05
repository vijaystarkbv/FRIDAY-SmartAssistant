import cohere # ai serivice
from rich import print # for output
from dotenv import dotenv_values # for environment and .env files
import time
import httpx

# loading the environmnt :)
env_vars = dotenv_values(".env")

# API key
CohereAPIKey = env_vars.get("CohereAPIKey")

co = cohere.Client(CohereAPIKey)  # Initialize with API key


# lets define recognizion funtion mannn
funcs = [
    "exit","general","realtime","open","close","play",
    "generate image","system","content","google search",
    "youtube search","reminder"
]

#storing message system here
messages = []

# defining the peremble that guids the AI model 

preamble = """
You are a **highly accurate Decision-Making Model** that classifies user queries into specific categories.  
Your task is **ONLY** to categorize the query—**DO NOT** answer it.  

You must classify queries into one of the following categories:  

 **General Query** → If the query can be answered by a general AI model (conversational chatbot) and does NOT require real-time information.  
   - Example:  
     - "Who was Akbar?" → Respond: **"general Who was Akbar?"**  
     - "How can I study more effectively?" → Respond: **"general How can I study more effectively?"**  
     - "Can you help me with this math problem?" → Respond: **"general Can you help me with this math problem?"**  
     - "What is Python programming language?" → Respond: **"general What is Python programming language?"**  
     - "Thanks, I really liked it." → Respond: **"general Thanks, I really liked it."**  

 **Realtime Query** → If the query requires **live, updated, or changing information** (e.g., current events, latest data, real-time statistics).  
   - Example:  
     - "What is the net worth of Elon Musk?" → Respond: **"realtime What is the net worth of Elon Musk?"**  
     - "What is today's weather?" → Respond: **"realtime What is today's weather?"**  
     - "Who won the last cricket match?" → Respond: **"realtime Who won the last cricket match?"**  

 **Task/Automation Query** → If the user asks you to perform an action or execute a command.  
   - Example:  
     - "Open Facebook" → Respond: **"open Facebook"**  
     - "Can you write an application and open it in Notepad?" → Respond: **"generate application, open Notepad"**  
     - "Play my favorite song" → Respond: **"play favorite song"**  

 **IMPORTANT:**  
- **DO NOT** answer the query—just categorize it.  
- **DO NOT** modify the query—keep it as is, only adding the category prefix.  
"""


# I will define chat history etc...
ChatHistory = [
    {"role":"User","message": "how are you?"},
    {"role":"Chatbot","message": "general how are you?"},
    {"role":"User", "message": " do you like pizza?"},
    {"role":"Chatbot", "message": "general do you like pizza?"},
    {"role":"User","message": "open chrome and tell me about mahatma gandhi"},
    {"role":"Chatbot","message": "open chrome, general tell me about mahatma gandhi"},
    {"role":"User","message": "open chrome and firefox"},
    {"role":"Chatbot","message": "open chrome, open firefox"},
    {"role":"User","message": "what is today's date and by the way remind me that i have a badmintion today at morning 5:30am"},
    {"role":"Chatbot","message": "general what is today's date, reminder 5:30am"},
    {"role":"User","message": "chat with me"},
    {"role":"Chatbot","message": "general chat with me."}
 ]

# adding the thinking part
import time  # Don't forget to import time at the top

def FirstLayerDMM(prompt: str = "test"):
    # Adding user query
    messages.append({"role": "user", "content": f"{prompt}"})

    while True:  # Adding a retry loop
        try:
            # Creating streaming chat
            stream = co.chat_stream(
                model="command-r-plus",  # for cohere model
                message=prompt,  # pass user's query
                temperature=0.7,  # creative level of model
                chat_history=ChatHistory,  # gives history of context
                prompt_truncation="OFF",  # to ensure the prompt is not truncated
                preamble=preamble,  # pass detailed instruction
            )

            # Storing general response
            response = ""

            # Iterate over events
            for event in stream:
                if event.event_type == "text-generation":
                    response += event.text  # Generate text

            # Remove newline characters and split responses
            response = response.replace("\n", "")
            response = response.split(",")

            # Strip leading and trailing
            response = [i.strip() for i in response]

            # Empty list to filter valid tasks
            temp = []

            # Filtering tasks based on recognized function
            for task in response:
                for func in funcs:
                    if task.startswith(func):
                        temp.append(task)

            if "(query)" in response:
                newresponse = FirstLayerDMM(prompt=prompt)  # Recursive call for new response
                return newresponse
            else:
                return response

        except httpx.ConnectError as e:  # Handling the connection error
            print("Connection Error: Retrying...")
            time.sleep(5)  # Wait for 5 seconds before retrying
            continue  # Continue the loop to retry

# Entry point for the script
if __name__ == "__main__":
    while True:
        print(FirstLayerDMM(input(">>>")))  # Print categorized
