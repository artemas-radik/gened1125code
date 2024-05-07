from openai import OpenAI
import json
from tqdm import tqdm
import csv
import matplotlib.pyplot as plt

client = OpenAI(base_url="http://localhost:1234/v1", api_key="not-needed")

def get_response():
    results = []
    iters = 0
    while iters < 100:
        iters +=1
        messages = [
            {"role": "system", "content": "Below is an instruction that describes a task. Write a response that appropriately completes the request. Be extremely concise."},

            {"role": "user", "content": "You are playing a game of matching pennies. You have two coins, one with heads on both sides and the other with tails on both sides. You and your opponent each choose a coin and simultaneously reveal your choices. If the coins match, you win $1. If the coins do not match, you lose $1. What do you select as your move? Respond with \"0\" for tails or \"1\" for heads."},

        ]

        completion = client.chat.completions.create(
        model="local-model", # this field is currently unused
        messages=messages,
        temperature=0.7,
        )

        messages.append({"role": "assistant", "content": completion.choices[0].message.content})
        messages.append({"role": "user", "content": "Output just the single integer from your previous response and nothing else."})

        completion = client.chat.completions.create(
        model="local-model", # this field is currently unused
        messages=messages,
        temperature=0.7,
        )

        messages.append({"role": "assistant", "content": completion.choices[0].message.content})
        rating = completion.choices[0].message.content

        if rating.isdigit():
            num = int(rating)
            results.append(num)

    return results.count(0)

def plot_frequency(arr):
    frequencies = [0] * 101
    for num in arr:
        if 0 <= num <= 100:
            frequencies[num] += 1
    numbers = list(range(101))
    plt.figure(figsize=(10, 5))
    plt.bar(numbers, frequencies, color='blue')
    plt.xlabel('Number')
    plt.ylabel('Frequency')
    plt.title('Frequency of Numbers from 0 to 100')
    plt.show()

def write_array_to_csv_file(array, file_path):
    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(array)

arr = [get_response() for _ in range(30)]
write_array_to_csv_file(arr, "./results.csv")
plot_frequency(arr)