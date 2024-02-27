import csv
import openai
from openai import OpenAI
API_KEY = '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'

client = OpenAI(api_key = API_KEY)


response = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {
      "role": "system",
      "content": "You are a helpful assistant."
    },
    {
      "role": "user",
      "content": "Translate these English words to French: ['hello', 'world']"
    }
  ],
  temperature=1,
  max_tokens=256,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0
)

# Assuming the response contains a list of translations
translations = response['choices'][0]['message']['content'].strip().split(', ')

# Write the data to a CSV file
with open('translations.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["English", "French"])
    writer.writerow(['hello', translations[0]])
    writer.writerow(['world', translations[1]])
