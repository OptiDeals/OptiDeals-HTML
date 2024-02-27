import csv
import openai

openai.api_key = 'your-api-key'

response = openai.Completion.create(
  engine="text-davinci-002",
  prompt="Translate these English words to French: ['hello', 'world']",
  max_tokens=60
)

# Assuming the response contains a list of translations
translations = response.choices[0].text.strip().split(', ')

# Write the data to a CSV file
with open('translations.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["English", "French"])
    writer.writerow(['hello', translations[0]])
    writer.writerow(['world', translations[1]])
