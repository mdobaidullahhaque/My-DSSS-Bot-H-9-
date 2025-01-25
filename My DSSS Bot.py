#!/usr/bin/env python
# coding: utf-8

# In[1]:


pip install python-telegram-bot transformers torch


# In[3]:


pip install nest_asyncio


# In[5]:


import nest_asyncio
nest_asyncio.apply()


# In[8]:


import logging
import nest_asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from transformers import pipeline

import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from transformers import pipeline

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# My api token from BotFather
API_TOKEN = "8016136987:AAEcqhpf9mWTAIde6ohIEhUU43dtZObiFgY"

# Load the language model pipeline
logger.info("Loading the language model...")
model_pipeline = pipeline("text-generation", model="gpt2")

# Start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a welcome message when the /start command is issued."""
    await update.message.reply_text("Hi! I am your AI assistant. How can I help you today?")

# Message handler
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Process user messages and respond using the language model."""
    user_input = update.message.text  # Get the user's message
    logger.info(f"Received message: {user_input}")

    # Generate a response using the model
    try:
        response = model_pipeline(user_input, max_length=100, num_return_sequences=1)[0]["generated_text"]
    except Exception as e:
        logger.error(f"Error during model inference: {e}")
        response = "Sorry, I couldn't process your request."

    # Send the response back to the user
    await update.message.reply_text(response)

# Main function to start the bot
def main() -> None:
    """Run the bot."""
    # Create the application
    application = ApplicationBuilder().token(API_TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start the bot
    logger.info("Bot is running...")
    application.run_polling()

if __name__ == "__main__":
    main()


# In[ ]:




