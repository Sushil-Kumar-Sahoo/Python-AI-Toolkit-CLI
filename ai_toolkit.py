import argparse
import os 
from dotenv import find_dotenv,load_dotenv
import sys
from google import genai
from google.genai import types


load_dotenv(find_dotenv(".env"))
def content_generation(client,content):
    try:
        print("Processing your prompt...")
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=content,
            config =types.GenerateContentConfig(
                automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True)
            )
        )
        return response
    except Exception as err:
        print(f"API Error: Failed to generate content. Details: {err}")
        sys.exit(1)
        
def display_response(response):
    print("\n" + "=" * 70)
    print("                         AI RESPONSE")
    print("=" * 70)
    print(response.text.strip())
    print("=" * 70 + "\n")

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




    