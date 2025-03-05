from googlesearch import search
from groq import Groq
from json import load, dump
from dotenv import dotenv_values
import datetime

# environmet from API
env_vars = dotenv_values(".env")

# retriving some specific variables
Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")
GroqAPIKey = env_vars.get("GroqAPIKey")

# initializeing the groq clint
clint = Groq(api_key=GroqAPIKey)

System = f"""Hello, I am {Username}, You are a very accurate and advanced AI chatbot named {Assistantname} which has real-time up-to-date information from the internet.
*** Provide Answers In a Professional Way, make sure to add full stops, commas, question marks, and use proper grammar.***
*** Just answer the question from the provided data in a professional way. ***"""

try:
    with open(r"Data\ChatLog.json", "r") as f:
        message = load(f)
except FileNotFoundError:
    with open(r"Data\ChatLog.json", "w") as f:
        dump([], f)

# defining function for the code
def GoogleSearch(query):
    results = list(search(query, advanced=True, num_results=5))        
    Answer = f"The search result for '{query}'are:\n[start]\n"

    for i in results:
        Answer += f"Title: {i.title}\nDescription: {i.description}\n\n"

        Answer += "[end]"
        return Answer
    
    # function to modify chatbot's response
def AnswerModifier(Answer):
    lines = Answer.split('\n')
    non_empty_lines = [ line for line in lines if line.strip()]
    modified_answer = '\n'.join(non_empty_lines)
    return modified_answer

SystemChatBot =[
    {"role":"system", "content": System},
    {"role":"user", "content": "Hi"},
    {"role":"assistant", "content": "Hello, how can I help you?"}
]

def Information():
    data = " "
    current_date_time = datetime.datetime.now() # gets the current date and time
    day = current_date_time.strftime("%A")
    date = current_date_time.strftime("%d")
    month = current_date_time.strftime("%B")
    year = current_date_time.strftime("%Y")
    hour = current_date_time.strftime("%H")
    minute = current_date_time.strftime("%M")
    second = current_date_time.strftime("%S")
    data += f"Use This Real-time Information if needed:\n"
    data += f"Day: {day}\n"
    data += f"date: {date}\n"
    data += f"Month: {month}\n"
    data += f"Year: {year}\n"
    data += f"Time:{hour} hours :{minute} minutes:{second} second.\n"
    return data

# fucntion that defines real time search engine 
def RealtimeSearchEngine(prompt):
    global SystemChatBot, messages

    #lard with chat lods from JSON files
    with open(r"Data\ChatLog.json", "r") as f:
            message = load(f)
    message.append({"role": "user", "content": f"{prompt}"})

    #adding search engine results
    SystemChatBot.append({"role": "system", "content": GoogleSearch(prompt)})

    #generating a response 
    completion = clint.chat.completions.create(
      model="llama3-70b-8192",  
      messages=SystemChatBot + [{"role": "system", "content": Information()}] + message,  # message instead of messages
      temperature=0.7,
      max_tokens=2048,  
      top_p=1,
      stream=True,
      stop=None
    )

    
    Answer = ""  # to store AI's response

    for chunk in completion:
     if chunk.choices[0].delta.content:
        Answer += chunk.choices[0].delta.content


    Answer = Answer.strip().replace("</s>", "")

         # Append the AI's response to the loaded 'message' variable
    message.append({"role": "assistant", "content": Answer})

          # Saving the updated chatlog in the JSON file
    with open(r"Data\ChatLog.json", "w") as f:
               dump(message, f, indent=4)

            # Return the modified answer
    return AnswerModifier(Answer=Answer)
    
#main porgram entry point
if __name__ == "__main__":
    while True:
        prompt = input("Enter Your query:")    
        print(RealtimeSearchEngine(prompt))