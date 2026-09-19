import argparse
import itertools
import os
import sys
import threading
import time

from dotenv import find_dotenv, load_dotenv
from google import genai
from google.genai import types


class Spinner:
    def __init__(self, message="Processing your prompt"):
        self.message = message
        self.stop_event = threading.Event()
        self.thread = None

    def _run(self):
        spinner_frames = itertools.cycle(
            ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        )

        while not self.stop_event.is_set():
            frame = next(spinner_frames)
            sys.stdout.write(f"\r{frame} {self.message}...")
            sys.stdout.flush()
            time.sleep(0.1)

    def start(self):
        self.stop_event.clear()
        self.thread = threading.Thread(target=self._run)
        self.thread.start()

    def stop(self):
        self.stop_event.set()

        if self.thread:
            self.thread.join()

        sys.stdout.write("\r\033[K")
        sys.stdout.flush()


class GeminiClient:
    RETRYABLE_ERRORS = {408, 429, 500, 502, 503, 504}
    MAX_RETRIES = 3

    def __init__(self, api_key):
        if not api_key:
            raise ValueError("API_KEY is missing from your .env file.")

        self.client = genai.Client(api_key=api_key)

    def generate(self, content):
        spinner = Spinner("Executing your given task")
        spinner.start()

        try:
            for attempt in range(self.MAX_RETRIES):
                try:
                    response = self.client.models.generate_content(
                        model="gemini-3.6-flash",
                        contents=content,
                        config=types.GenerateContentConfig(
                            automatic_function_calling=types.AutomaticFunctionCallingConfig(
                                disable=True
                            )
                        )
                    )
                    return response

                except Exception as error:
                    error_message = str(error)
                    status_code = self._get_status_code(error_message)

                    if status_code is None:
                        raise RuntimeError(
                            f"API request failed: {error_message}"
                        )

                    if attempt == self.MAX_RETRIES - 1:
                        raise RuntimeError(
                            f"Server error after {self.MAX_RETRIES} attempts: "
                            f"{error_message}"
                        )

                    wait_time = 2 ** attempt
                    print(f"\nAPI error: {status_code}")
                    print(f"Retrying in {wait_time}s...")
                    time.sleep(wait_time)

        finally:
            spinner.stop()

    def _get_status_code(self, error_message):
        for code in self.RETRYABLE_ERRORS:
            if str(code) in error_message:
                return code
        return None


class PromptBuilder:
    @staticmethod
    def summarize(text):
        return (
            "Summarize the following text into key bullet points, "
            "capturing only the essential facts and action items.\n\n"
            f"{text}"
        )

    @staticmethod
    def translate(text, language):
        return (
            "Output ONLY the translated text without "
            "conversational intro phrases.\n"
            f"Translate the following text into {language}:\n\n"
            f"{text}"
        )

    @staticmethod
    def sentiment(text):
        return (
            "Respond ONLY with one word: POSITIVE, NEGATIVE, or NEUTRAL. "
            "Do not include extra commentary.\n\n"
            f"{text}"
        )

    @classmethod
    def build(cls, task, text, language="english"):
        if task == "summarize":
            return cls.summarize(text)
        elif task == "translate":
            return cls.translate(text, language)
        elif task == "sentiment":
            return cls.sentiment(text)
        else:
            raise ValueError(f"Unsupported task: {task}")


class ResponseDisplay:
    @staticmethod
    def display(response):
        print("\n" + "=" * 100)
        print("Gemini RESPONSE".center(100))
        print("=" * 100)
        print(response.text.strip())
        print("=" * 100 + "\n")


class CLIHandler:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description="Python AI Toolkit"
        )

        self.parser.add_argument(
            "--task",
            required=True,
            choices=["summarize", "translate", "sentiment"],
            help="What do you want me to do?"
        )

        self.parser.add_argument(
            "--lang",
            default="english",
            help="Target language for translation."
        )

        self.parser.add_argument(
            "--text",
            required=True,
            help="Text you want to process."
        )

    def parse(self):
        args = self.parser.parse_args()

        task = args.task.lower()
        text = args.text.strip()
        language = args.lang.strip()

        if not text:
            self.parser.error("The --text field cannot be empty.")

        return task, text, language


class AIToolkit:
    def __init__(self):
        load_dotenv(find_dotenv(".env"))

        api_key = os.getenv("API_KEY")

        self.ai = GeminiClient(api_key)
        self.cli = CLIHandler()

    def run(self):
        task, text, language = self.cli.parse()

        prompt = PromptBuilder.build(
            task=task,
            text=text,
            language=language
        )

        response = self.ai.generate(prompt)
        ResponseDisplay.display(response)


def main():
    try:
        app = AIToolkit()
        app.run()
    except KeyboardInterrupt:
        print("\nProgram stopped by user.")
    except Exception as error:
        print(f"\nError: {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()