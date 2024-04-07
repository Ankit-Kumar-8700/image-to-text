from flask import Flask, render_template, request, redirect
import pytesseract
from PIL import Image
from gtts import gTTS
from googletrans import Translator
from langdetect import detect

app = Flask(__name__)
app.use_x_sendfile = True

@app.route('/')
def index():
    return render_template('index.html')

text=['''''','']
onceDone=[False]

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files and onceDone[0]==False:
        return redirect("/")
    
    elif 'file' in request.files:
        file = request.files['file']
        if file.filename == '':
            return redirect('/')
        
        else:
            onceDone[0]=True
            image = Image.open(file)
            text[0] = pytesseract.image_to_string(image)
            # print(text[0])
    
    # Detect the language of the extracted text
    detected_language = detect(text[0])

    # Get the selected language from the form
    selected_language = request.form.get('language') or 'en'
    # print(selected_language,detected_language)

    # Translate the text to English if it's not already in English
    translator = Translator()
    translated_text = translator.translate(text[0], src=detected_language, dest=selected_language).text


    tts = gTTS(translated_text)
    audio_file_path = "static/output.mp3"
    tts.save(audio_file_path)

    return render_template('result.html', text=text[0], audio_file_path=audio_file_path, translated_text=translated_text, detected_language=detected_language)


if __name__ == '__main__':
    app.run(debug=True)
