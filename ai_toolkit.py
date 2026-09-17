import argparse
import os 
from dotenv import find_dotenv,load_dotenv
import sys
from google import genai
from google.genai import types
import itertools
import sys
import time
import threading

def spinner_task(stop_event, message="Processing your prompt"):
    # Cycle infinitely through spinner frames
    spinner_frames = itertools.cycle(["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"])

    while not stop_event.is_set():
        # \r moves cursor to start of line; \033[K clears the line
        frame = next(spinner_frames)
        sys.stdout.write(f"\r{frame} {message}...")
        sys.stdout.flush()
        time.sleep(0.1)

    # Clean up line after finishing
    sys.stdout.write("\r\033[K")
    sys.stdout.flush()

load_dotenv(find_dotenv(".env"))
def content_generation(client,content):
    RETRYABLE_ERRORS = {408, 429, 500, 502, 503, 504}
    MAX_RETRIES = 3 
    
    stop_event = threading.Event()
    spinner_thread = threading.Thread(target=spinner_task,args=(stop_event,"Executing your given task"))
    spinner_thread.start()
    
    try:
        for attempt in range(MAX_RETRIES):
            try:
                response = client.models.generate_content(
                    model="gemini-3.6-flash",
                    contents=content,
                    config =types.GenerateContentConfig(
                        automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True)
                    )
                )
                return response
            except Exception as err:
                error_msg = str(err)
                status_code = None
                
                for code in RETRYABLE_ERRORS:
                    if str(code) in error_msg:
                        status_code = code
                        break
                
                if status_code is None:
                    stop_event.set()
                    spinner_thread.join()                    
                    print(f"Sorry something goes wrong \nTry again after some time: \nError : {error_msg} !")
                    sys.exit(1)
                
                if attempt == MAX_RETRIES-1:
                    stop_event.set()
                    spinner_thread.join()
                    print(f"Something goes wrong from server side \nError : {error_msg} !")
                    print(f"After {MAX_RETRIES} attempts !")
                    sys.exit(1)
                
                wait_time = 2 ** attempt
                
                print(f"\nAPI error : {status_code} \nRetrying in {wait_time}s...")
                time.sleep(wait_time)
                
    finally:
        stop_event.set()
        spinner_thread.join()
        
def display_response(response):
    print("\n" + "=" * 160)
    print(" "*70,"Gemini RESPONSE")
    print("=" * 160)
    print(response.text.strip())
    print("=" * 160 + "\n")

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--task",required=True,help="What do you want me to do ? ",choices=["summarize","translate","sentiment"])
    parser.add_argument("--lang",default="english",help="Type any language you want to translate your typed text.")  
    parser.add_argument("--text",required=True,help="Type your text here...")
    
    args = parser.parse_args()
    text = str(args.text)
    task = str(args.task)
    task_lang = str(args.lang)
    
    
    api_key = os.getenv("API_KEY")
    if not api_key:
        print("Error: API_KEY is missing from your .env file.")
        sys.exit(1)
        
    client = genai.Client(api_key=api_key)
    
    # cleaning texts and validating
    task_clean = task.lower()
    
    text = text.strip()
    if len(text) < 1 :
        print("your text field looks like empty")
        sys.exit(1)
    
    match task_clean:
        case "summarize":
            prompt = f"Summarize the following text into key bullet points,capturing only the essential facts and action items \n\n{text}"
            response = content_generation(client,prompt)
            display_response(response)
            
        case "translate":
            prompt = f"""Output ONLY the translated text without conversational intro phrases. 
                        Translate the following text into {task_lang}::\n\n{text}"""
            response = content_generation(client,prompt)
            display_response(response)

        
        case "sentiment" :
            prompt = f"Respond ONLY with one word: POSITIVE, NEGATIVE, or NEUTRAL. Do not include extra commentary.:\n\n{text}"
            response = content_generation(client,prompt)
            display_response(response)




    