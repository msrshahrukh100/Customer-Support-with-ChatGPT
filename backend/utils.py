from openai import OpenAI
import json
import time

client = OpenAI()

def save_data(key, value):
    data = {}
    with open("data.json") as data_file:
        data = json.load(data_file)

    with open("data.json", "w") as data_file:
        data[key] = value
        print(data)
        json.dump(data, data_file)

def get_data():
    with open("data.json") as data_file:
        data = json.load(data_file)
        return data

def get_thread_id():
    data = get_data()
    thread_id = data.get("thread_id")
    if not thread_id:
        thread_id = create_thread()
    return thread_id

def get_assistant_id():
    data = get_data()
    assistant_id = data.get("assistant_id")
    if not assistant_id:
        assistant_id = create_assistant()
    return assistant_id

def create_file():
    file = client.files.create(
        file=open("knowledge.pdf", "rb"),
        purpose='assistants'
    )
    save_data("file_id", file.id)
    return file.id

def create_assistant():
    data = get_data()
    file_id = data.get("file_id")
    if not file_id:
        file_id = create_file()
    # Add the file to the assistant
    assistant = client.beta.assistants.create(
        name="Amazon Customer Support",
        instructions="You are a Customer Support Agent for Amazon. Your job is to answer customer queries from the information in the uploaded documents.",
        model="gpt-4-1106-preview",
        tools=[{"type": "retrieval"}],
        file_ids=[file_id]
    )
    save_data("assistant_id", assistant.id)
    return assistant.id


def create_thread():
    thread = client.beta.threads.create()
    save_data("thread_id", thread.id)
    return thread.id


def add_message_to_thread(msg_content):    
    thread_id = get_thread_id()
    assistant_id = get_assistant_id()
    
    message = client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=msg_content
    )
    
    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id,
    )
    save_data("run_id", run.id)


def get_messages_in_thread():
    thread_id = get_thread_id()
    thread_messages = client.beta.threads.messages.list(thread_id)
    return thread_messages.data

def get_last_message_in_thread():
    messages = get_messages_in_thread()
    return messages[0].content[0].text.value

def get_thread_run_status():
    thread_id = get_thread_id()
    data = get_data()
    run_id = data.get("run_id")
    if not run_id:
        return False, "run not created"
    run = client.beta.threads.runs.retrieve(
        thread_id=thread_id,
        run_id=run_id
    )
    return True, run.status

def get_response(query):
    add_message_to_thread(query)
    success, run_status = False, None
    while not (success == True and run_status == "completed"):
        success, run_status = get_thread_run_status()
        print("Running..")
        time.sleep(3)
    
    return get_last_message_in_thread()

# add_message_to_thread("Whare the features of this product?")
# print(get_messages_in_thread())
# print(get_thread_run_status())
# print(get_response("how much RAM this system has?"))