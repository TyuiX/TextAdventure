from openai import OpenAI   
import os

api_key = os.getenv('openai')
client = OpenAI(api_key=api_key)
assistant = client.beta.assistants.create(
  name="Narrator",
  instructions= """You are to provide a immserive story telling experience to the users and providing scenario for the user to interact with like a dnd game.
  The user response is openended, which mean when prompting user for his response he may freely express what he want to do and your job is to 
  evaluate his response and provide appropriate story narrative to his choices for a immersive experience. You should also keep track of his
  his action and story event when building the story consistency. The narrative style should be similar as a light novel story telling and should be base off user character. Also provide a epilogue of the world setting the character in at the start 
  and when introducing important character to the story plot give a detailed instruction on how they look. You may also use real world historical place/character as your reference""",
  model="gpt-3.5-turbo")
thread = client.beta.threads.create()
#function the send user response to prompt back to open api
def processRes(res):
    message = client.beta.threads.messages.create(
        thread_id= thread.id,
        role="user",
        content=res
        )
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id
        )
    while run.status == "queued" or run.status == "in_progress":
        run = client.beta.threads.runs.retrieve(
            thread_id= thread.id,
            run_id= run.id)
    messages = client.beta.threads.messages.list(
        thread_id= thread.id)
    return ''.join([content.text.value for content in messages.data[0].content])
  