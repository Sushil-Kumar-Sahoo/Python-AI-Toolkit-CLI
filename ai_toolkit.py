import argparse
import os 
from dotenv import find_dotenv,load_dotenv
from google import genai

load_dotenv(find_dotenv(".env"))
def create_chat_session(client):
    chat = client.chats.create(
        model="gemini-3.6-flash"
    )
    return chat

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--text",help="Write your text here...")
    parser.add_argument("--task",help="What do you want to (summarize,translate,sentiment)")  
    
    args = parser.parse_args()
    text = args.text
    task = args.task
    
    if task is not None and text is not None:
        api_key = os.getenv("API_KEY")
        client = genai.Client(api_key=api_key)
        chat = create_chat_session(client)
        
        task_clean = task.lower()
        
        if task_clean == "summarize":
            prompt = f"Summarize the following text into key bullet points,capturing only the essential facts and action items \n\n{text}"
            response = chat.send_message(prompt)
            print(response.text)
            
        elif task_clean == "translate":
            prompt = f"Translate the following text to  hindi:\n\n{text}"
            response = chat.send_message(prompt)
            print(response.text)            
        
        elif task_clean == "sentiment" :
            prompt = f"Analyze the sentiment of the following text (Positive, Negative, or Neutral):\n\n{text}"
            response = chat.send_message(prompt)
            print(response.text)            
            
        else:
            print(f"Sorry, Entered task name invalid{task} !") 
    else:
        enter = task if task is not None else text
        print(enter)  

    