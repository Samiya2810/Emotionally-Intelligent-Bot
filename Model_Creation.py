import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
import speech_recognition as sr
import pyttsx3
import random

# Load your labeled dataset
# Replace 'your_dataset.csv' with the path to your dataset
dataset = pd.read_csv('Tweets.csv')

X = dataset['text']
y = dataset['sentiment']

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Convert text data to TF-IDF features
vectorizer = TfidfVectorizer(max_features=5000)  # You can adjust the max_features parameter
X_train_tfidf = vectorizer.fit_transform(X_train.fillna(''))  # Impute NaN with an empty string
X_test_tfidf = vectorizer.transform(X_test.fillna(''))

# Train the Support Vector Machine (SVM) model
svm_classifier = SVC(kernel='linear')  # You can try different kernels like 'linear', 'rbf', etc.
svm_classifier.fit(X_train_tfidf, y_train)

negative_sentences = [
    "Every challenge is an opportunity for growth. You've got this!",
    "Remember, tough times don't last, but tough people do. Stay resilient!",
    "Mistakes are proof that you are trying. Keep pushing forward!",
    "A positive attitude can turn a setback into a comeback. Keep your head up!",
    "Every cloud has a silver lining. Look for the positive in every situation.",
    "Believe in yourself, and you'll be unstoppable. You are capable of amazing things.",
    "It's okay not to be okay sometimes. Tomorrow is a new day, full of possibilities.",
    "You are stronger than you think. Embrace challenges as stepping stones to success.",
    "Focus on progress, not perfection. Each step forward is a victory.",
    "Your journey may be tough, but it's shaping you into the person you are destined to become."
]

positive_sentences = [
    "Fantastic news! Your positive outlook is a beacon of inspiration to others.",
    "Your optimism is contagious – keep spreading that positive energy!",
    "I'm thrilled to hear about the positive vibes! Your resilience shines through.",
    "In the midst of challenges, your positivity is a powerful force. Keep it up!",
    "Your positive mindset is a key to success. Embrace the journey ahead!",
    "What a wonderful attitude! Your positivity has the potential to create amazing experiences.",
    "Your optimism is a gift to yourself and those around you. Keep embracing the good vibes!",
    "The world needs more positivity, and you're contributing beautifully. Well done!",
    "Your positive spirit is like a ray of sunshine. Keep brightening the world!",
    "Celebrate the wins, no matter how small. Your positivity is making a difference."
]

neutral_sentences = [
    "Sometimes, a neutral perspective allows for balance and clarity. Take your time to process.",
    "Neutral moments can be a chance to reflect and find peace within. Embrace the stillness.",
    "It's okay to have moments of neutrality. Use this time to explore new possibilities.",
    "Life has its ebb and flow. Neutrality can be a pause before the next exciting chapter.",
    "In the midst of neutrality, discover the beauty of simplicity and the joy of being present.",
    "Neutrality is a natural part of the journey. Trust that the path ahead holds new adventures.",
    "A neutral stance can provide the mental space needed for creative insights. Stay open.",
    "Sometimes, neutrality is a signal for self-care. Take a moment to nurture your well-being.",
    "Neutrality offers a chance to find equilibrium. Focus on self-discovery and personal growth.",
    "Embrace the neutrality as a blank canvas. What colors will you paint on it next?"
]

def predict_sentiment(input_text):
    # Transform the input text using the TF-IDF vectorizer
    input_text_tfidf = vectorizer.transform([input_text])

    # Predict sentiment using the loaded SVM model
    prediction = svm_classifier.predict(input_text_tfidf)

    return prediction[0]

def convert_speech_to_text():
    recognizer = sr.Recognizer()

    # Use the default microphone as the audio source
    with sr.Microphone() as source:
        print("Say something:")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source, timeout=5)

    try:
        print("Recognizing...")
        text = recognizer.recognize_google(audio)
        print("You said:", text)
        return text
    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return ""
    
def text_to_speech(text):
    # Initialize the text-to-speech engine
    engine = pyttsx3.init()

    # Set properties (optional)
    engine.setProperty('rate', 120)  # Speed of speech
    engine.setProperty('volume', 2)   # Volume level (0.0 to 1.0)

    # Convert the text to speech
    engine.say(text)

    # Wait for the speech to finish
    engine.runAndWait()
