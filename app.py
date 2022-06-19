from flask import Flask, render_template,request
from datetime import datetime
from youtube_transcript_api import YouTubeTranscriptApi
from transformers import T5ForConditionalGeneration, T5Tokenizer
from transformers import pipeline
import requests
# define a variable to hold you app
app = Flask(__name__)

# define your resource endpoints

@app.route('/time', methods=['GET'])
def get_time():
    return str(datetime.datetime.now())

@app.errorhandler(404)
def invalid_route(e):
    return "invalid route"


def generateTranscript(videoId):
    
    video_id = videoId.split("=")[1]
    transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
    
    transcript = transcript_list.find_transcript(['en'])
    #translate the transcript
    #translated_transcript = transcript.translate('de')
    
    paragraph=''
    for t in transcript.fetch():
        paragraph += t['text']
        paragraph += " "
    #print(len(paragraph))
    model = T5ForConditionalGeneration.from_pretrained("t5-base")
    # initialize the model tokenizer
    tokenizer = T5Tokenizer.from_pretrained("t5-base")
    inputs = tokenizer.encode("summarize: " + paragraph, return_tensors="pt", max_length=1024, truncation=True)

    outputs = model.generate(
    inputs, 
    max_length=500, 
    min_length=200, 
    length_penalty=2.0, 
    num_beams=4, 
    early_stopping=True)
    # just for debugging
    #print(outputs)
    ret = str(tokenizer.decode(outputs[0]))
    print(ret)
    return(ret)
    
    '''summarizer = pipeline('summarization')
    num_iters = int(len(paragraph)/1000)
    summarized_text = []
    for i in range(0, num_iters + 1):
        start = 0
        start = i * 1000
        end = (i + 1) * 1000
        # print("input text \n" + result[start:end])
        out = summarizer(paragraph[start:end],min_length=30,max_length=100)
        out = out[0]
        out = out['summary_text']
        #print("Summarized text\n"+out)
        summarized_text.append(out)
    print(summarized_text)'''
    
    
    
    '''for trans in transcript_list:
 
    # the Transcript object provides metadata
    # properties
        print(
            trans.video_id,
            trans.language,
            trans.language_code,
       
            # whether it has been manually created or
            # generated by YouTube
            trans.is_generated,
         
            # whether this transcript can be translated
            # or not
            trans.is_translatable,
         
            # a list of languages the transcript can be
            # translated to
            trans.translation_languages,
        )'''

def generate_Summary(paragraph):
    
    # initialize the model architecture and weights
    model = T5ForConditionalGeneration.from_pretrained("t5-base")
    # initialize the model tokenizer
    tokenizer = T5Tokenizer.from_pretrained("t5-base")
    inputs = tokenizer.encode("summarize: " + paragraph, return_tensors="pt", max_length=1024, truncation=True)

    outputs = model.generate(
    inputs, 
    max_length=500, 
    min_length=200, 
    length_penalty=2.0, 
    num_beams=4, 
    early_stopping=True)
    # just for debugging
    #print(outputs)
    ret = list(tokenizer.decode(outputs[0]))
    print(ret)
    return(ret)

    '''summarizer = pipeline('summarization')
    num_iters = int(len(paragraph)/1000)
    summarized_text = []
    for i in range(0, num_iters + 1):
        start = 0
        start = i * 1000
        end = (i + 1) * 1000
        # print("input text \n" + result[start:end])
        out = summarizer(paragraph[start:end],min_length=30,max_length=100)
        out = out[0]
        out = out['summary_text']
        #print("Summarized text\n"+out)
        summarized_text.append(out)'''

    

@app.route("/", methods = ["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form.get("url")
        url_content = generateTranscript(url)
        return url_content
    return render_template("index.html")

# server the app when this file is run
if __name__ == '__main__':
    app.run(debug=True)