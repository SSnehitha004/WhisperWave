import os
import fitz  # PyMuPDF
from textblob import TextBlob
import spacy
from transformers import pipeline, AutoTokenizer
import edge_tts
import asyncio
import streamlit as st

# Initialize NLP and summarization models once
nlp = spacy.load('en_core_web_sm')
summarizer = pipeline('summarization', model='sshleifer/distilbart-cnn-12-6')
tokenizer = AutoTokenizer.from_pretrained('sshleifer/distilbart-cnn-12-6')
qa_model = pipeline("question-answering", model="distilbert-base-cased-distilled-squad")

# Function to extract text from PDF using fitz
def extract_text_from_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()
    return text

# Function to split text into smaller chunks based on token length
def split_text_into_chunks(text, max_tokens=1024):
    words = text.split()
    chunks = []
    current_chunk = []

    for word in words:
        current_chunk.append(word)
        if len(tokenizer(' '.join(current_chunk))['input_ids']) >= max_tokens:
            chunks.append(' '.join(current_chunk[:-1]))
            current_chunk = [word]
    
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    
    return chunks

# Function to analyze text for persons, places, and emotional words
def analyze_text(text):
    doc = nlp(text)
    persons = list(set([ent.text for ent in doc.ents if ent.label_ == 'PERSON']))
    places = list(set([ent.text for ent in doc.ents if ent.label_ in ('GPE', 'LOC')]))
    emotional_words = extract_emotional_words(text)
    return persons, places, emotional_words

# Function to extract emotional words from text
def extract_emotional_words(text):
    emotional_words = []
    emotion_keywords = {
        'happy': ['happy', 'joy', 'elated', 'excited'],
        'sad': ['sad', 'unhappy', 'down', 'depressed'],
        'angry': ['angry', 'mad', 'furious', 'irritated'],
    }
    blob = TextBlob(text)
    for word in blob.words:
        for emotion, keywords in emotion_keywords.items():
            if word.lower() in keywords:
                emotional_words.append((word, emotion))
    return emotional_words

# Function to determine the overall tone of the text
def determine_tone(emotional_words):
    emotion_counts = {'happy': 0, 'sad': 0, 'angry': 0}
    for _, emotion in emotional_words:
        if emotion in emotion_counts:
            emotion_counts[emotion] += 1

    if not any(emotion_counts.values()):
        return "Neutral"

    tone = max(emotion_counts, key=emotion_counts.get)
    return tone.capitalize()

# Function to summarize text using a summarization model
def summarize_text(text):
    chunks = split_text_into_chunks(text)
    summaries = [summarizer(chunk, max_length=150, min_length=30, do_sample=False)[0]['summary_text'] for chunk in chunks]
    combined_summary = ' '.join(summaries)
    return combined_summary

# Function to generate speech from text using edge_tts
async def generate_speech(text, voice):
    audio_file_path = 'summary.wav'
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(audio_file_path)
    return audio_file_path

# Streamlit app
def main():
    st.title("PDF Text Analysis and Summarization")

    uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

    if uploaded_file is not None:
        with open(os.path.join("uploads", uploaded_file.name), "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        text = extract_text_from_pdf(os.path.join("uploads", uploaded_file.name))
        st.subheader("Extracted Text")
        st.write(text)

        summary = summarize_text(text)
        st.subheader("Summary")
        st.write(summary)

        persons, places, emotional_words = analyze_text(text)
        
        st.subheader("Persons")
        st.write(persons)
        
        st.subheader("Places")
        st.write(places)
        
        st.subheader("Emotional Words")
        st.write(emotional_words)

        tone = determine_tone(emotional_words)
        st.subheader("Overall Tone")
        st.write(tone)

        st.subheader("Ask a Question about the PDF")
        question = st.text_input("Enter your question:")
        if question:
            answer = qa_model(question=question, context=text)
            st.write(f"Answer: {answer['answer']}")

        st.subheader("Generate Speech")
        voices = {
            "Tony": "en-US-GuyNeural",  # Different male US voice
            "Ryan": "en-GB-RyanNeural",
            "Jenny": "en-US-JennyNeural",
            "Libby": "en-GB-LibbyNeural"
        }
        selected_voice = st.selectbox("Select Voice", list(voices.keys()))

        if st.button("Generate Speech"):
            audio_file_path = asyncio.run(generate_speech(summary, voices[selected_voice]))
            audio_file = open(audio_file_path, "rb").read()
            st.audio(audio_file, format="audio/wav")

if __name__ == "__main__":
    main()
