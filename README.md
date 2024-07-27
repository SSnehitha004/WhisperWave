# Emotion-Based PDF Reader
## Project Description : 
This project is a comprehensive solution for analyzing and interacting with PDF files.
1. **User-Friendly Interface**: Allows users to upload PDF files easily with an intuitive and visually appealing UI.
2. **Person Identification and Emotion Detection**: Identifies references to people and places within the text and detects emotional words, displaying them on the UI.
3. **Emotion-Based PDF Reading** : Converts text to speech with emotion modulation, offering a choice of four different voices (two male, two female) for reading summaries.
4. **Summarization and Question-Answering**: Summarizes extracted text and provides instant, accurate answers to user questions based on the PDF content.

## Technologies Used.
1. **PyMuPDF (fitz)**: Extracts text from PDF files.
2. **TextBlob**: Analyzes text sentiment and extracts emotional words.
3. **spaCy**: Performs named entity recognition to identify persons and places.
4. **Hugging Face Transformers**: Provides text summarization and question-answering capabilities.
   - **Summarization Pipeline**
   - **AutoTokenizer**
   - **Question-Answering Pipeline**
5. **edge_tts**: Converts text to speech.
6. **Streamlit**: Creates an interactive web application interface.

## Setup Instructions
1. **Clone the Repository**:
   ```sh
   git clone https://github.com/SSnehitha004/WhisperWave.git
2. **Navigate to the Repository Directory**:
   ```sh
    cd WhisperWave
3. **Set Up a Virtual Environment**:
   ```sh
   python -m venv .venv
4. **Activate the Virtual Environment**:
    -   **On macOS/Linux**:
        ```sh
        source .venv/bin/activate
    - **On Windows**:
        ```sh
        .venv\Scripts\activate
5. **Install Dependencies**:
   ```sh
   pip install -r requirements.txt
6. **Run the Application**:
   ```sh
   streamlit run app.py
