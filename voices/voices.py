#!/usr/bin/python

from collections import namedtuple
import textwrap

VOICE = namedtuple("Voice", ["name", "lcode", "country", "letter"])

voice_table = [
        VOICE("en-AU-Wavenet-A", "en-AU", "Australia", "A"),
        VOICE("en-AU-Wavenet-B", "en-AU", "Australia", "B"),
        VOICE("en-AU-Wavenet-C", "en-AU", "Australia", "C"),
        VOICE("en-AU-Wavenet-D", "en-AU", "Australia", "D"),

        VOICE("en-GB-Wavenet-A", "en-GB", "Great Britain", "A"),
        VOICE("en-GB-Wavenet-B", "en-GB", "Great Britain", "B"),
        VOICE("en-GB-Wavenet-C", "en-GB", "Great Britain", "C"),
        VOICE("en-GB-Wavenet-D", "en-GB", "Great Britain", "D"),

        VOICE("en-US-Wavenet-A", "en-US", "The United States", "A"),
        VOICE("en-US-Wavenet-B", "en-US", "The United States", "B"),
        VOICE("en-US-Wavenet-C", "en-US", "The United States", "C"),
        VOICE("en-US-Wavenet-D", "en-US", "The United States", "D"),
        VOICE("en-US-Wavenet-E", "en-US", "The United States", "E"),
        VOICE("en-US-Wavenet-F", "en-US", "The United States", "F"),
]

def text_string(voice):
    text = textwrap.dedent("""
        Hello. I am speaker %s, from %s.
        The quick brown fox jumped over the lazy dog.
        Now is the time for all good men to come to the aid of their country.
        """
        )[1:-1] % (voice.letter, voice.country)

    return text

html = open("index.html", 'w')

hdr = textwrap.dedent("""
    <html>
    <head>
    </head>
    <body>
    """[1:-1]
)
html.write(hdr)

for voice in voice_table:
    with open(voice.name + ".txt", 'w') as fp:
        fp.write(text_string(voice))


    mp3file = voice.name + ".mp3"
    html.write(textwrap.dedent("""
        %s
        <br>
        <audio controls>
            <source src=%s type="audio/mpeg">
        </audio>
        <br>
        """[1:-1] % (voice.name, mp3file)
    ))

html.write("</body>\n")
html.close()
