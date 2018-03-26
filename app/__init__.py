import cherrypy
from cherrypy.lib.static import serve_file
import text_extractor
import os, os.path


class Root(object):
    @cherrypy.expose
    def index(self):
        return """<html>
          <head><link href="/static/css/style.css" rel="stylesheet"></head>
          <body>
            <h1>Get all the text in a deck</h1>
            <form method="get" action="generate">
              <input type="text" value="8" name="deck_id" />
	      <input type="text" value="http://qr.quodeck.com" name="url" />
              <button type="submit">Get Values</button>
            </form>
          </body>
        </html>"""
    
    @cherrypy.expose
    def generate(self, deck_id, url):
        key = text_extractor.extract_slide_text_from_quodeck(url, deck_id)
        return serve_file(key, "application/x-download", "attachment")

    @cherrypy.expose
    def generate_tags(self, deckId):
        return text_extractor.extract_keywords_from_quodeck('http://localhost:3000', deckId)

    @cherrypy.expose
    def tags(self):
        return "aaaaa"

    @cherrypy.expose
    def generate_audio_tags(self):
        return text_extractor.extract_keywords_from_audio("/home/sunny/Desktop/Salil_s_Kohler_Radio_Intro.mp3")
    
    @cherrypy.expose
    def generate_docdeck_tags(self, docdeck_id):
        return text_extractor.extract_keywords_from_docdecks('http://localhost:3000', docdeck_id)

    @cherrypy.expose
    def generate_slidewise_text_deck(self, deckId):
        key = text_extractor.extract_slide_text_from_quodeck('http://qr.quodeck.com', deckId)
        return serve_file(key, "application/x-download", "attachment")
        # return key

