import tkinter as tk
from tkinter import scrolledtext
from datetime import datetime
import random
import re

# ---------- Bot Logic ----------
BOT_NAME = "RuleBot"

responses = {
    "hello": ["Hello Tulasi! 👋", "Hi there! Ready to chat?"],
    "hi": ["Hi Tulasi! How can I help you?", "Hello! What would you like to talk about?"],
    "hey": ["Hey Tulasi! 😊", "Hey there!"],
    "how are you": ["I'm doing great, thank you!", "Feeling helpful today!"],
    "your name": [f"I am {BOT_NAME}, your friendly chatbot."],
    "thanks": ["You're welcome!", "Anytime!"],
    "thank you": ["Happy to help!", "Glad I could assist!"],
    "bye": ["Goodbye Tulasi! Have a wonderful day!", "See you soon!"],
    "about ai": ["Artificial Intelligence helps computers solve problems and learn from data.", "AI can answer questions, automate tasks, and help people learn."],
    "python": ["Python is used for AI, web apps, data science, automation, and more.", "Python is a great language for beginners and experts alike."],
}

jokes = [
    "Why do programmers love Python? Because it's easy to read! 😂",
    "Debugging: removing the needles from the haystack.",
    "Why was the computer cold? It left Windows open!"
]

motivations = [
    "Believe in yourself! 💪",
    "Practice makes perfect.",
    "Never stop learning.",
    "Small progress is still progress."
]

help_message = (
    "Type one of these commands:\n"
    "hello, hi, hey\n"
    "how are you\n"
    "date, time\n"
    "joke, motivate me\n"
    "python, about ai\n"
    "calculate 10+20\n"
    "exit\n"
)


def safe_calculate(expression):
    cleaned = expression.replace(" ", "")
    if not re.fullmatch(r"[0-9+\-*/(). ]+", cleaned):
        raise ValueError("Unsafe expression")
    return str(eval(cleaned, {"__builtins__": None}, {}))


def get_bot_reply(user_input):
    text = user_input.strip().lower()
    if not text:
        return None

    if text in responses:
        return random.choice(responses[text])

    if text == "help":
        return help_message

    if text == "date":
        return datetime.now().strftime("Today's date: %d-%m-%Y")

    if text == "time":
        return datetime.now().strftime("Current time: %I:%M:%S %p")

    if text == "joke":
        return random.choice(jokes)

    if text == "motivate me":
        return random.choice(motivations)

    if text.startswith("calculate ") or text.startswith("calc "):
        expr = text.split(None, 1)[1]
        try:
            return f"Answer = {safe_calculate(expr)}"
        except Exception:
            return "I can only calculate simple numeric expressions like 10+20."

    if "weather" in text:
        return "I don't have live weather data, but I hope it's sunny where you are! ☀"

    if "name" in text and "your" in text:
        return f"I am {BOT_NAME}, your friendly AI chatbot."

    return "Sorry, I don't understand that yet. Type 'help' to see commands."


# ---------- GUI ----------

root = tk.Tk()
root.title("Basic AI Chatbot")
root.geometry("700x520")
root.resizable(False, False)

header = tk.Label(
    root,
    text=f"🤖 {BOT_NAME} - Basic AI Chatbot",
    font=("Arial", 18, "bold"),
    fg="#2c3e50",
)
header.pack(pady=10)

chat = scrolledtext.ScrolledText(root, width=80, height=20, font=("Consolas", 11))
chat.pack(padx=10)
chat.configure(state="normal")
chat.insert(tk.END, "Bot : Welcome Tulasi!\n")
chat.insert(tk.END, "Bot : Type 'help' to see what I can do.\n\n")
chat.configure(state="disabled")

control_frame = tk.Frame(root)
control_frame.pack(fill="x", pady=10, padx=10)

entry = tk.Entry(control_frame, font=("Arial", 13))
entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
entry.focus()


def append_message(sender, message):
    chat.configure(state="normal")
    chat.insert(tk.END, f"{sender} : {message}\n\n")
    chat.see(tk.END)
    chat.configure(state="disabled")


def send_message(event=None):
    user_text = entry.get().strip()
    if not user_text:
        return
    append_message("You", user_text)
    entry.delete(0, tk.END)
    if user_text.lower() == "exit":
        append_message("Bot", "Goodbye Tulasi! 👋")
        root.after(500, root.destroy)
        return
    reply = get_bot_reply(user_text)
    if reply:
        append_message("Bot", reply)


send_btn = tk.Button(
    control_frame,
    text="Send",
    command=send_message,
    bg="#4CAF50",
    fg="white",
    font=("Arial", 11, "bold"),
    width=10,
)
send_btn.pack(side="left", padx=(0, 5))

clear_btn = tk.Button(
    control_frame,
    text="Clear",
    command=lambda: chat.configure(state="normal") or chat.delete("1.0", tk.END) or chat.configure(state="disabled"),
    font=("Arial", 11),
    width=10,
)
clear_btn.pack(side="left", padx=(0, 5))

exit_btn = tk.Button(
    control_frame,
    text="Exit",
    command=root.destroy,
    bg="#e74c3c",
    fg="white",
    font=("Arial", 11, "bold"),
    width=10,
)
exit_btn.pack(side="left")

entry.bind("<Return>", send_message)
root.mainloop()