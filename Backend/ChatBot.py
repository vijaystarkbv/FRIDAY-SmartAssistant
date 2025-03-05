from groq import Groq
from json import load, dump
import datetime
from dotenv import dotenv_values

# environmet from API
env_vars = dotenv_values(".env")

# retriving some specific variables
Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")
GroqAPIKey = env_vars.get("GroqAPIKey")

# initializeing the groq clint
clint = Groq(api_key=GroqAPIKey)

message = []

System = f"""Hello, I am {Username}, You are a very accurate and advanced AI chatbot named {Assistantname} which also has real-time up-to-date information from the internet.
*** Do not tell time until I ask, do not talk too much, just answer the question.***
*** Reply in only English, even if the question is in Hindi, reply in English.***
*** Do not provide notes in the output, just answer the question and never mention your training data. ***
"""

# system interface for it
SystemChatBot = [
    {"role": "system", "content": System}
]

# loading chat log from JSON file
try:
    with open(r"Data\ChatLog.json", "r") as f:
        message = load(f)
except FileNotFoundError:
    with open(r"Data\ChatLog.json", "w") as f:
        dump([], f)

# making the function for real time date and time info
def RealtimeInformation():
    current_date_time = datetime.datetime.now() # gets the current date and time
    day = current_date_time.strftime("%A")
    date = current_date_time.strftime("%d")
    month = current_date_time.strftime("%B")
    year = current_date_time.strftime("%Y")
    hour = current_date_time.strftime("%H")
    minute = current_date_time.strftime("%M")
    second = current_date_time.strftime("%S")


    # format the info into string
    data = f"please use this real-time informationif needed,\n"
    data += f"day: {day}\nDate: {date}\nMonth: {month}\nYear: {year}\n"
    data += f"Time: {hour} hours :{minute} minutes:{second} second.\n"
    return data

# function to modify chatbot's response
def AnswerModifier(Answer):
    lines = Answer.split('\n')
    non_empty_lines = [ line for line in lines if line.strip()]
    modified_answer = '\n'.join(non_empty_lines)
    return modified_answer

# main chatbot function to handle user queries
def ChatBot(Query):
    """This function sends the user's query to the chatbot and returns the AI's response."""

    try:
        #loading the existing chat
        with open(r"Data\ChatLog.json", "r") as f:
            message = load(f)

            message.append({"role": "user", "content": f"{Query}"})

            # making request for API response
            completion = clint.chat.completions.create(
             model="llama3-70b-8192",  
             messages=SystemChatBot + [{"role": "system", "content": RealtimeInformation()}] + message,  # message instead of messages
             max_tokens=1024,
             temperature=0.7,
             top_p=1,
             stream=True,
             stop=None
            )

    

            Answer = ""  # to store AI's response

            for chunk in completion:
              if chunk.choices[0].delta.content:
               Answer += chunk.choices[0].delta.content

            Answer = Answer.replace("</s>", "")

            # Append the AI's response to the loaded 'message' variable
            message.append({"role": "assistant", "content": Answer})

            # Saving the updated chatlog in the JSON file
            with open(r"Data\ChatLog.json", "w") as f:
               dump(message, f, indent=4)

            # Return the modified answer
            return AnswerModifier(Answer=Answer)


    except Exception as e:
        #handle errors my printing the exception
        print(f"Error:{e}")
        with open(r"Data\ChatLog.json", "w") as f:
            dump([], f, indent=4)
        return ChatBot(Query) # retry the query after resetting the log

#main porgram entry point
if __name__ == "__main__":
    while True:
        user_input = input("Enter Your Question:")    
        print(ChatBot(user_input))
