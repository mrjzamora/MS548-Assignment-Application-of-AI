import tkinter as tk
from textblob import TextBlob
import nltk
from nltk.corpus import wordnet

#NLTK resources
nltk.download('wordnet', quiet=True)
nltk.download('averaged_perceptron_tagger', quiet=True)
nltk.download('omw-1.4', quiet=True)

def get_positive_synonyms(word):
    """
    Attempt to find positive synonyms for a given word using WordNet.
    Avoid synonyms with inherently negative connotations.
    """
    synonyms = []
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            if lemma.name().lower() != word and not lemma.antonyms():  # Check for non-negative synonyms
                synonyms.append(lemma.name().replace('_', ' '))
    return list(set(synonyms))

def improve_sentence(sentence):
    """
    Improve sentence sentiment by replacing negative adjectives with positive synonyms.
    """
    words = nltk.word_tokenize(sentence)
    tagged_words = nltk.pos_tag(words)
    improved_words = []
    
    for word, tag in tagged_words:
        if tag.startswith('JJ'):  # Adjective
            analysis = TextBlob(word).sentiment
            if analysis.polarity < 0:  # Negative adjective
                synonyms = get_positive_synonyms(word)
                if synonyms:
                    improved_words.append(synonyms[0])  # Use the first synonym
                else:
                    improved_words.append(word)
            else:
                improved_words.append(word)
        else:
            improved_words.append(word)
    
    return ' '.join(improved_words)

def analyze_sentiment():
    """
    Analyze the sentiment of the provided text and display results.
    """
    user_input = text_input.get("1.0", "end-1c")
    analysis = TextBlob(user_input)
    polarity = analysis.sentiment.polarity
    
    if polarity > 0:
        sentiment.set("Positive")
        output_text.set("No improvement needed. Good to go!")
    elif polarity == 0:
        sentiment.set("Neutral")
        output_text.set("Text is neutral. Need more emotional expression.")
    else:
        sentiment.set("Negative")
        improved_text = improve_sentence(user_input)
        output_text.set(improved_text)

    output_display.config(state='normal')
    output_display.delete("1.0", "end")
    output_display.insert("1.0", output_text.get())
    output_display.config(state='disabled')

def clear_text():
    """
    Clear all text fields.
    """
    text_input.delete("1.0", "end")
    output_display.config(state='normal')
    output_display.delete("1.0", "end")
    output_display.config(state='disabled')
    sentiment.set("")
    output_text.set("")

#main window
root = tk.Tk()
root.title("Jaime Zamora - From Negative to Positive Sentiment")

# User input text area
text_input = tk.Text(root, height=10, width=50)
text_input.pack()

# buttons
analyze_button = tk.Button(root, text="Click here to Analyze Sentiment", command=analyze_sentiment)
analyze_button.pack()

clear_button = tk.Button(root, text="Clear", command=clear_text)
clear_button.pack()

#display for results
sentiment = tk.StringVar()
sentiment_label = tk.Label(root, textvariable=sentiment)
sentiment_label.pack()

output_text = tk.StringVar()
output_display = tk.Text(root, height=10, width=50, state='disabled')
output_display.pack()

# GUI
root.mainloop()
