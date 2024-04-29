import telebot
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import matplotlib.pyplot as plt
import io

bot_token = "6838990519:AAHQvI8mv2NPb69uIIe6Jop45yTHQzFoxm4"
bot = telebot.TeleBot(bot_token)

# Define a variable to store the user's input
user_input = ""

def send_pie_chart(chat_id):
    # Example data
    labels = ['Positive', 'Negative', 'Neutral']
    sizes = [30, 40, 30]  # Example percentages (should sum to 100)

    # Create a pie chart
    plt.figure(figsize=(6, 6))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
    plt.title('Sentiment Distribution')

    # Save the chart to a file-like object
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    # Send the photo to the user
    update.message.reply_photo(photo=buffer)
    
def handle_message(update, context):
    user_input = update.message.text
    print(user_input)
    sentiment_prediction = predict_sentiment(user_input)
    if sentiment_prediction == 'negative':
        selected_sentence = random.choice(negative_sentences)
        print(f"Predicted Sentiment: {sentiment_prediction}. {selected_sentence}")
        update.message.reply_text(f"{selected_sentence}")
    elif sentiment_prediction == 'positive':
        selected_sentence = random.choice(positive_sentences)
        print(f"Predicted Sentiment: {sentiment_prediction}. {selected_sentence}")
        update.message.reply_text(f"{selected_sentence}")
    elif sentiment_prediction == 'neutral':
        selected_sentence = random.choice(neutral_sentences)
        print(f"{selected_sentence}")
        update.message.reply_text(f"{selected_sentence}")

def handle_pie_chart_command(update, context):
    send_pie_chart(chat_id)

updater = Updater(token=bot_token, use_context=True)

# Get the dispatcher to register handlers
dispatcher = updater.dispatcher

# Register the command handler
dispatcher.add_handler(CommandHandler("send_pie_chart", handle_pie_chart_command))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

# Start the bot
updater.start_polling()
updater.idle()
