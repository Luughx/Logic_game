import openai
import creds

openai.api_key = creds.OPENAI_API_KEY
openai.api_base = 'https://api.openai.com/v1/chat'

def gpt3_completion(messages, engine='gpt-3.5-turbo', temp=0.9, tokens=400, freq_pen=2.0, pres_pen=2.0):
    response = openai.Completion.create(
        model=engine,
        messages=messages,
        temperature=temp,
        max_tokens=tokens,
        frequency_penalty=freq_pen,
        presence_penalty=pres_pen,)
    
    text = response['choices'][0]['message']['content'].strip()
    return text