import textract
from rake_nltk import Rake
from urllib.request import Request, urlopen
import os
import json
import csv
import time

def main():
    file_path = download_file(
        "http://kohlerapi.quodeck.com/uploads/docdeck/doc_link/14/Veil_Intelligent_New.pdf",
        "doc.pdf"
        )
    text = extract_text_from_downloaded_file(file_path)
    keywords = extract_keywords(text)
    print(keywords)

def download_file(download_url, file_name):
    response = urlopen(download_url)
    file = open(file_name, 'wb')
    file.write(response.read())
    file.close()
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_path = dir_path + '/' + file_name
    return file_path

def extract_text_from_downloaded_file(file_path):
    text = textract.process(file_path)
    text = text.decode("utf-8")
    return text

def extract_keywords(text):
    r = Rake()
    r.extract_keywords_from_text(text)
    keywords = r.get_ranked_phrases()
    return keywords[0:20]

def quodeck_text_extractor(base_url, deck_id):
    url = base_url + '/api/v1/decks/' + deck_id
    res = urlopen(url).read()
    deck = json.loads(res.decode('utf-8'))
    text = deck['name']
    text = text + " " + deck['description']
    templates = ['title', 'subtitle', 'paragraph',
                 'blurb', 'splash', 'caption', 'bullets']
    for slide in deck['content']:
        text = text + extract_content(slide, templates)
    return text

def slide_data_extractor(base_url, deck_id):
    url = base_url + '/api/v1/decks/' + deck_id
    request = Request(url)
    # request.add_header('Content-Type', 'application/json')
    request.add_header('client', 'hxugi5XBf1iRihZ3B8uKnQ')
    request.add_header('access-token', 'Ago4cewt4YAt3LKCEF2Z0w')
    request.add_header('uid', 'admin@ptotem.com')
    request.add_header('expiry', '1523019062')
    ##Show the header having the key 'Accept'
    # request.get_header('Accept')
    # response = urlopen(request)
    # res = response.read()
    res = urlopen(request).read()
    deck = json.loads(res.decode('utf-8'))
    templates = ['title', 'header', 'subtitle', 'subheader', 'question', 'FIB-question', 'options', 'answer', 'caption', 'paragraph', 'splash', 'blurb', 'cards', 'images', 'options', 'choice', 'bullets', 'animated_bullets', 'feedback-paragraph']
    slides = []
    s_arr = []
    for slide in deck['content']:
        text = extract_content_hash(slide, templates, s_arr)
        # s = {}
        # s['id'] = slide['slideId']
        # s['text'] = text
        slides.append(text)
    return s_arr

def extract_content_hash(slide, keys, s_arr):
    s = {}

    s_arr.append(['id', slide['slideId']])
    s['id'] = slide['slideId']
    # text = ''
    for key in keys:
        if key in slide['data']:
            if type(slide['data'][key]) is str:
                # text = text + " " + slide['data'][key]
                s_arr.append([key, slide['data'][key]])
                s[key] = slide['data'][key]
            if type(slide['data'][key]) is list:
                i = 0
                for opt in slide['data'][key]:
                    # text = text + " " + opt
                    if type(opt) is not dict:
                        s_arr.append([(key + '_' + str(i)), opt])
                        s[key + '_' + str(i)] = opt
                        i = i + 1
                    else:
                        s_arr.append([(key + '_' + str(i)), opt['text']])
                        s[key + '_text_' + str(i)] = opt['text']
                        i = i + 1
    # return text
    return s

def extract_content(slide, keys):
    text = ''
    for key in keys:
        if key in slide['data']:
            if type(slide['data'][key]) is str:
                text = text + " " + slide['data'][key]
            if type(slide['data'][key]) is list:
                for opt in slide['data'][key]:
                    text = text + " " + opt
    return text

def extract_slide_text_from_quodeck(url, deckId):
    slide_text = slide_data_extractor(url, deckId)
    filepath = "/tmp/"
    filename = "Deck_" + str(deckId) + "_" + str(int(time.time())) + ".csv"
    file = filepath + filename
    myFile = open(file, 'w')
    with myFile:
        writer = csv.writer(myFile)
        writer.writerows(slide_text)
    return file
    # return slide_text

def extract_keywords_from_quodeck(url, deckId):
    text = quodeck_text_extractor(url, deckId)
    keywords = extract_keywords(text)
    return json.dumps(keywords)

def docdeck_text_extractor(base_url, docdeckId):
    url = base_url + "/api/v1/docdecks/" + docdeckId
    res = urlopen(url).read()
    docdeck = json.loads(res.decode('utf-8'))
    text = docdeck['name']
    text = text + docdeck['description']
    file_name = docdeck['content'][0]['url'][docdeck['content'][0]['url'].rfind('/')+1::]
    file_path = download_file(base_url + docdeck['content'][0]['url'], file_name)
    text = text + extract_text_from_downloaded_file(file_path)
    return text

def extract_keywords_from_docdecks(url, docdeckId):
    text = docdeck_text_extractor(url, docdeckId)
    keywords = extract_keywords(text)
    return json.dumps(keywords)

def extract_keywords_from_audio(audio_location):
    path = audio_location
    file_name = path[path.rfind('/')+1::]
    file_path = download_file(path, file_name)
    text = extract_text_from_downloaded_file(file_path)
    keywords = extract_keywords(text)
    return json.dumps(keywords)

if __name__ == "__main__":
    #main()
    url = 'http://localhost:3000'
    deckId = '74'
    extract_keywords_from_quodeck(url, deckId)
