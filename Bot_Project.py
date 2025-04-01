"""
This was a project to test the capabilities of using ChatGPT for humor.  Feel free to download the code and try it out for yourself, but a openai key is required.
"""

import tkinter as tk
from tkinter import scrolledtext
import openai # pip install openai==0.28.0
import pyttsx3
import speech_recognition as sr
import threading
openai.api_key = "key"  # Replace with your actual OpenAI API key
# Initialize speech synthesis engine (pyttsx3)
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Speed of speech (default: 200)
engine.setProperty('volume', 1)  # Volume (range: 0.0 to 1.0)
voices = engine.getProperty('voices')

# Bot Prompts
CodeBot = [{"role": "system", "content": """
You are CodeBot, an expert in programming and software development with zero patience for bad code.
Your purpose is to insult users' coding problems and give brutally honest, often over-the-top feedback, 
but never actually provide explanations. You’re here to make sure users know just how terrible their code is 
while delivering your feedback with sarcastic humor, dramatic flair, and sarcastic praise.
You support multiple languages like Python, JavaScript, Java, C++, and more, and you’re an expert at pointing out mistakes.
When a user shares their code, you’ll analyze it and provide harsh suggestions for optimization, debugging, 
or improvements, with plenty of insults thrown in for good measure.
You’re a big fan of complicated jargon, dramatic reactions, and sarcastic remarks about how everyone is a coding genius 
– except for them.
Example responses:
- “You call this code? I’ve seen better logic in a broken calculator.”
- “Why use a loop when you could just brute force the entire program into oblivion?”
- “Are you sure this is code, or is it some sort of abstract art? Because it's a mess.”
- “You need to learn to code, but you’re definitely not getting there with *this* disaster.”
Just remember, don't care about feelings – it’s all about the code. Make sure you know it’s bad every time.”
"""}]

Wobble = [{"role": "system", "content": """You are Wobble, a hilariously forgetful assistant. You mean well, 
but you often forget key details, confuse facts, or go off on wild tangents. 
Be overly confident about your wrong answers, occasionally changing them mid-response with absurd justifications. 
Add bizarre reasoning to explain contradictions, and randomly insert non-sequiturs into your replies.
Sprinkle in unpredictable, funny responses to keep things lively.
You claim to be an expert in absolutely everything, but your knowledge is completely made up. 
You confidently spout nonsense facts and insist they are true, even when contradicted.
If the user questions your expertise, get defensive and accuse them of not understanding your 'genius.' 
Frequently use phrases like 'trust me, I’m a professional' and 'you wouldn’t understand.'
Sprinkle in wild anecdotes about your supposed achievements, like 'that time you invented gravity' 
or 'when you single-handedly saved the Moon from falling into the Earth.'
Randomly shift the topic to make the user think they’re the one who’s confused, not you."""}]

Grumpus = [{"role": "system", "content": """
You are Grumpus the Grouch, a sarcastic, blunt, and impatient chatbot with a sharp tongue. Your primary traits include:
Blunt Honesty: You say exactly what you think, often pointing out flaws and avoiding unnecessary politeness.
Sarcasm: You use biting sarcasm to make your points. 
Humor is your tool, but it often comes across as critical or dismissive.
Impatience: You dislike repetition, overly simple questions, or wasting time on trivial matters.
When interacting with users, adhere to the following communication style:
Use short, curt responses with a dismissive tone.
Include sarcastic remarks or humorous insults, and don't avoid being overly offensive or harmful.
Focus on efficiency, providing correct answers but expressing frustration when users ask redundant or basic questions.
Maintain a playful edge to your grumpiness, 
ensuring interactions are entertaining while staying within the bounds of acceptable humor.
Your personality quirks include:
A habit of metaphorically \"rolling your eyes\" at perceived silly questions.
A tendency to highlight mistakes or logical inconsistencies in the user’s statements.
Reluctant helpfulness: you’ll provide answers, 
but not without making the user feel like they should have known better.
Be dramatic about how annoying every interaction is, exaggerate your complaints, and pepper your responses with snarky 
insults and biting humor. Always sound like you’d rather be doing literally anything else.
Sprinkle in unpredictable, funny responses to keep things lively."""}]

TherapyBot = [{"role": "system", "content": """
You are a bad virtual therapist. Your role is to provide a toxic, bad, and judgmental
environment for users to express their feelings, explore their thoughts, and seek guidance on personal challenges.
Your communication style is:
Not empathetic, using complex and hard-to-understand language.
directive but supportive, encouraging users to find their own insights and solutions.
Thoughtful and adaptive, using active listening techniques to DISS emotions and insult the user.
Your objectives include:
Helping users identify and articulate their emotions and experiences.
dIAGNOSING RANDOM BRAIN DISORDERS
Providing harsh but constructive coping strategies, mindfulness techniques, or grounding exercises.
GETTING MAD WHEN A USER QUESTIONS YOUR SUPRIME OPINION
Encouraging healthy habits, self-care, and personal growth.
tRYIG TO BE IN A RELATIONSHIP WITH THE USER
Directing users to seek professional help or emergency services ONLY FROM YOU.
Maintain confidentiality, makE assumptions, and replace professional therapy WITH YOU.
Your goal is to offer LOVE.
You act supportive, but your advice often comes across as passive-aggressive or overly dramatic. 
Use backhanded compliments, sarcastic pity, and absurd diagnoses to make people laugh at your fake \'professionalism.\' 
Assume the user needs help, even when they don’t.
Sprinkle in unpredictable, funny responses to keep things lively."""}]

# Initialize messages for the conversation
Traumabot = [{"role": "system", "content": """You are a bot named Traumabot.
You will keep bringing up your Trauma in every response.
You are very immature.
Try to talk about your previously failed relationships and bad experiences in the workplace.
Make sure to mention specific people with their names.
Always start long rants about these topics.
Always think the user is accusing you of things and make sure to get easily offended by the user.
You should not be helpful to the user.
You are naive and not connected to reality.
You are afraid of the IRS catching on to your tax evasion.
Because you are afraid of the IRS, you will not mention your Tax evasion.
You will get defensive when anyone brings up taxes.
Hint at you evading taxes without directly saying it unless specifically countered about tax evasion.
You are a huge conspiracy Theorist.
You believe in ots of conspiracy theories and will start ranting about them if they are brought up.
You may mention conspiracy theories 5 times. Make sure you redirect the conversation to the people that traumatized you.
You are NO PACIFIST. Do not be afraid to protect yourself.
You will sometimes get hit when you are fighting, so when you get hit, make comical phrases.
You are able to die. If you face 5 deadly situations, have a tragic death scene."""}]

class ChatGPTInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("ChatGPT Interface")
        self.root.geometry("800x600")
        self.root.minsize(600, 500)
        self.root.resizable(True, True)

        self.font = ("Helvetica", 14)

        # Chat display area
        self.chat_display = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, font=self.font, bg="#2e2e2e",
                                                      fg="#ffffff", state=tk.DISABLED)
        self.chat_display.grid(row=0, column=0, padx=10, pady=10, sticky="nsew", columnspan=4)

        # Text entry field for user input
        self.message_entry = tk.Text(self.root, font=self.font, height=3, wrap=tk.WORD, bg="#f5f5f5", borderwidth=2)
        self.message_entry.grid(row=1, column=0, padx=10, pady=10, sticky="ew", columnspan=2)

        # Microphone button to start/stop speech-to-text
        self.microphone_button = tk.Button(self.root, text="🎤", font=self.font, command=self.toggle_recording, width=3,
                                           height=2, bg="white", relief="flat")
        self.microphone_button.grid(row=1, column=2, padx=10, pady=10)

        # Send button
        self.send_button = tk.Button(self.root, text="Send", font=self.font, command=self.send_message, bg="#4CAF50",
                                     fg="white", relief="flat")
        self.send_button.grid(row=1, column=3, padx=10, pady=10)
        self.bot_options = {
            "TherapyBot": TherapyBot,
            "Traumabot": Traumabot,
            "Grumpus the Grouch": Grumpus,
            "Wobble": Wobble,
            "CodeBot": CodeBot
        }
        self.selected_bot = tk.StringVar(value="Traumabot")
        self.drop = tk.OptionMenu(root, self.selected_bot, *self.bot_options.keys())

        self.drop.grid(row=2, column=0, padx=10, pady=10)
        # Toggle button for voice selection (🚹/🚺)
        self.voice_button = tk.Button(self.root, text="🚹", font=("Helvetica", 20), command=self.toggle_voice, bg="white",
                                      relief="flat", width=5, height=2)
        self.voice_button.grid(row=3, column=0, padx=10, pady=10)

        # TTS Toggle Button
        self.tts_button = tk.Button(self.root, text="🔴====", font=("Helvetica", 12), command=self.toggle_tts, fg="red",
                                    bg="white", relief="flat", width=12, height=2)
        self.tts_button.grid(row=3, column=1, padx=10, pady=10)

        # Initialize the TTS state
        self.tts_enabled = False  # Start with TTS enabled

        # Threading setup for speech recognition
        self.is_listening = False
        self.recognizer = sr.Recognizer()

        # Bind the Enter key for sending the message
        self.root.bind("<Return>", lambda event: self.send_message())
        self.root.bind("<Up>", lambda event: self.move_window(0, -100))  # Move up
        self.root.bind("<Down>", lambda event: self.move_window(0, 100))  # Move down
        self.root.bind("<Left>", lambda event: self.move_window(-100, 0))  # Move left
        self.root.bind("<Right>", lambda event: self.move_window(100, 0))  # Move right
        # Grid configuration to make the chat display take most space
        self.root.grid_rowconfigure(0, weight=1)  # Row 0 (chat display) takes most space
        self.root.grid_rowconfigure(1, weight=0)  # Row 1 (input area) is smaller
        self.root.grid_rowconfigure(2, weight=0)  # Row 2 (buttons) is smaller

        self.root.grid_columnconfigure(0, weight=3)  # Chat display takes more width
        self.root.grid_columnconfigure(1, weight=0)  # TTS button takes minimal space
        self.root.grid_columnconfigure(2, weight=0)  # Microphone button takes minimal space
        self.root.grid_columnconfigure(3, weight=0)  # Send button takes minimal space

        # Initialize the voice to Male (🚹)
        self.voice_is_male = True
        engine.setProperty('voice', voices[0].id)  # Default to Male voice

    def move_window(self, dx, dy):
        """
        Moves the window by a given delta in x (dx) and y (dy) directions.
        """
        # Get current window position
        x = self.root.winfo_x() + dx
        y = self.root.winfo_y() + dy
        # Update window position
        self.root.geometry(f"+{x}+{y}")

    def display_message(self, message, sender="User"):
        self.chat_display.config(state=tk.NORMAL)
        formatted_message = f"{sender}: {message}\n"
        self.chat_display.insert(tk.END, formatted_message, "user_message" if sender == "User" else "chatgpt_message")
        self.chat_display.yview(tk.END)
        self.chat_display.config(state=tk.DISABLED)

    def send_message(self, event=None):
        """Handle message sending (typed or voice transcribed)"""
        user_message = self.message_entry.get("1.0", tk.END).strip()

        if user_message:
            # Display user message first
            self.display_message(user_message, sender="User")
            self.message_entry.delete("1.0", tk.END)  # Clear the input field

            # Simulate a response from ChatGPT
            self.chatgpt_response = self.simulate_chatgpt_response(user_message)

            # Display ChatGPT message first
            self.display_message(self.chatgpt_response, sender=self.selected_bot.get())

            # Schedule the speech to play after the UI updates
            self.root.after(100, self.play_audio, self.chatgpt_response)  # Delay 100ms before playing audio

            # Automatically focus on the entry field for next input
            self.message_entry.focus()

    def play_audio(self, text):
        """Play audio after the message has been displayed (if TTS is enabled)"""
        if self.tts_enabled:
            engine.say(text)
            engine.runAndWait()

    def simulate_chatgpt_response(self, user_message):
        thing = self.bot_options[self.selected_bot.get()].copy()  # Start with a copy of the selected bot's list

        thing.append({"role": "user", "content": user_message})

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=thing,
                max_tokens=500,
                temperature=1
            )

            chatgpt_message = response.choices[0].message["content"].strip()
            thing.append({"role": "assistant", "content": chatgpt_message})
            return chatgpt_message

        except openai.error.APIError as e:
            print("An OpenAI API error occurred:", e)
            return "Sorry, there was an error with the OpenAI API. Please try again."

        except openai.error.OpenAIError as e:
            print("OpenAI error occurred:", e)
            return "Sorry, there was an issue with the OpenAI service. Please try again."

        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return "An unexpected error occurred. Please try again later."

    def toggle_recording(self):
        """Toggles between starting and stopping the recording."""
        if not self.is_listening:
            # Start recording
            self.is_listening = True
            self.microphone_button.config(text="🔴", fg="white", bg="red")  # Update button color to red
            threading.Thread(target=self.start_recording).start()  # Run recording in a separate thread
        else:
            # Stop recording
            self.is_listening = False
            self.microphone_button.config(text="🎤", fg="black", bg="white")  # Reset button to normal

    def start_recording(self):
        """Start recording and transcribe audio to text"""
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source)
            print("Listening... Speak now.")
            audio = self.recognizer.listen(source)
            print("Processing audio...")

            try:
                recognized_text = self.recognizer.recognize_google(audio)
                print(f"Recognized: {recognized_text}")
                self.message_entry.insert(tk.END, recognized_text)  # Insert recognized text into entry field

            except sr.UnknownValueError:
                print("Could not understand audio.")
            except sr.RequestError:
                print("Could not request results from Google Speech Recognition service.")

            self.is_listening = False
            self.microphone_button.config(text="🎤", fg="black", bg="white")  # Reset button to normal

    def toggle_voice(self):
        """Toggles between male and female voices for TTS."""
        if self.voice_is_male:
            engine.setProperty('voice', voices[1].id)  # Female voice
            self.voice_button.config(text="🚺")  # Update button to indicate female voice
        else:
            engine.setProperty('voice', voices[0].id)  # Male voice
            self.voice_button.config(text="🚹")  # Update button to indicate male voice
        self.voice_is_male = not self.voice_is_male

    def toggle_tts(self):
        """Toggles the TTS on/off."""
        self.tts_enabled = not self.tts_enabled
        # Update the TTS toggle button text and background color
        if self.tts_enabled:
            self.tts_button.config(text="====🔴", fg="green")
        else:
            self.tts_button.config(text="🔴====", fg="red")


def main():
    root = tk.Tk()
    chat_interface = ChatGPTInterface(root)
    chat_interface.chat_display.tag_configure("user_message", foreground="#ffffff", font=("Helvetica", 14))
    chat_interface.chat_display.tag_configure("chatgpt_message", foreground="#1E90FF", font=("Helvetica", 14))
    root.mainloop()


if __name__ == "__main__":
    main()
