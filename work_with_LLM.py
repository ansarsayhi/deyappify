import openai
import sys
from process_lectures import transcriptions
from process_pdfs import texts



def get_replies():

    prompts = []
    for transcription in transcriptions:
        prompts.append(transcription+"\n"+(extra_prompt:=sys.argv[1]))
    for text in texts:
        prompts.append(text+"\n"+extra_prompt)
        
    openai.api_key = (your_api:= sys.argv[0])
    

    replies = []
    for prompt in prompts:
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[{'role': 'user', 'content': prompt}]
        )
        replies.append(response['choices'][0]['message']['content'])
    return replies

def write_replies(replies):
    with open('deyappify_output.txt', 'w') as file:
        for reply in replies:
            file.write(reply + '\n')

if __name__ == "__main__":
    replies = get_replies
    write_replies(replies)