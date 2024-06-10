import requests

API_ENDPOINT = "https://api.perplexity.ai/chat/completions"
API_KEY = ""

def get_answer_from_perplexity(message):
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {API_KEY}"
    }
    
    payload = {
        "model": "llama-3-sonar-large-32k-online",
        "messages": [
            {
                "role": "system",
                "content": "Be precise and concise."
            },
            {
                "role": "user",
                "content": message
            }
        ]
    }
    
    response = requests.post(API_ENDPOINT, headers=headers, json=payload)
    
    if response.status_code == 200:
        response_json = response.json()
        if 'choices' in response_json and len(response_json['choices']) > 0:
            answer = response_json['choices'][0]['message']['content']
            return answer
        else:
            return "Error: No answer found in the response."
    else:
        return f"Error: {response.status_code} - {response.text}"

if __name__ == "__main__":
    message = input("Enter your message: ")
    answer = get_answer_from_perplexity(message)
    print("Answer:", answer)
