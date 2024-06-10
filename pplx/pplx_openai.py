from openai import OpenAI
import pprint

YOUR_API_KEY = ""

messages = [
    {
        "role": "system",
        "content": "Be precise and concise."
        #(
        #    "You are an artificial intelligence assistant and you need to "
        #    "engage in a helpful, detailed, polite conversation with a user."
        #),
    },
    {
        "role": "user",
        "content": (
            "How many stars are in the universe?"
        ),
    },
]

client = OpenAI(api_key=YOUR_API_KEY, base_url="https://api.perplexity.ai")

# chat completion without streaming
response = client.chat.completions.create(
    model="llama-3-sonar-large-32k-online",
    messages=messages,
)
# print(response)

pp = pprint.PrettyPrinter(indent=2, width=80, compact=False)
pp.pprint(response)

print("Content:")
print(response.choices[0].message.content)
print("Role:")
print(response.choices[0].message.role)
print("Finish Reason:")
print(response.choices[0].finish_reason)
print('\n')

# chat completion with streaming
response_stream = client.chat.completions.create(
    model="llama-3-sonar-large-32k-online",
    messages=messages,
    stream=True,
)

#for response in response_stream:
#    print(response)