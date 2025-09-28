from django.shortcuts import render
import speech_recognition as sr

def detect_formality(text):
    informal_keywords = ["hi", "hey", "yo", "lol", "ok", "thanks", "thx", "bye"]
    text_lower = text.lower()
    if any(word in text_lower for word in informal_keywords):
        return "Informal"
    else:
        return "Formal"

def audio_to_text(request):
    context = {}
    if request.method == "POST" and request.FILES.get('audio_file'):
        audio_file = request.FILES['audio_file']

        # Save temporary file
        with open("temp_audio.wav", "wb+") as f:
            for chunk in audio_file.chunks():
                f.write(chunk)

        # Convert audio to text
        r = sr.Recognizer()
        with sr.AudioFile("temp_audio.wav") as source:
            audio_data = r.record(source)
            try:
                text = r.recognize_google(audio_data)
                formality = detect_formality(text)
                context['text'] = text
                context['formality'] = formality
            except sr.UnknownValueError:
                context['text'] = "Could not understand audio"
                context['formality'] = "N/A"
            except sr.RequestError as e:
                context['text'] = f"Error: {e}"
                context['formality'] = "N/A"

    return render(request, 'audio_form.html', context)
