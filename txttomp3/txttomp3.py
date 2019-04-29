#!/usr/bin/python3

from contextlib import contextmanager
import datetime
import time
import os
import sys
import tempfile
import subprocess
import shlex
import argparse
import shutil
import atexit
from mutagen.id3 import ID3, TIT2

from . import cache

devnull = open(os.devnull, 'w')


@contextmanager
def rate_limit(*runtimes):
    """Limit the minimum time a task will take"""

    minruntime = max(runtimes)
    start = datetime.datetime.now()

    yield None

    duration = datetime.datetime.now() - start
    sleeptime = minruntime - duration.total_seconds()

    if sleeptime > 0:
        time.sleep(sleeptime)


@cache.cache
def synthesize_text(name, language_code, text):
    """Synthesizes speech from the input string of text."""
    from google.cloud import texttospeech
    client = texttospeech.TextToSpeechClient()

    input_text = texttospeech.types.SynthesisInput(text=text)

    # Note: the voice can also be specified by name.
    # Names of voices can be retrieved with client.list_voices().
    voice = texttospeech.types.VoiceSelectionParams(
        name=name,
        language_code=language_code,
    )

    audio_config = texttospeech.types.AudioConfig(
        audio_encoding=texttospeech.enums.AudioEncoding.MP3)

    response = client.synthesize_speech(input_text, voice, audio_config)

    return response.audio_content


def parse_args():
    parser = argparse.ArgumentParser(
        description="Convert a text file to an MP3 file",
    )

    parser.add_argument(
        "text_file",
        help="the text file to convert to mp3",
        type=str,
    )

    parser.add_argument(
        "-s", "--speaker",
        help="The Google Text-to-Speech speaker to use "
             "(default: en-US-Wavenet-C)",
        type=str,
        default="en-US-Wavenet-C",
    )

    parser.add_argument(
        "-l", "--language_code",
        help="The language code (default en-US)",
        type=str,
        default="en-US",
    )

    parser.add_argument(
        "-j", "--json-file",
        help="The Google credentials file",
        type=str,
        default="None",
    )

    args = parser.parse_args()

    return args


def get_credentials(json_arg):
    if json_arg:
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = json_arg
    elif not os.environ['GOOGLE_APPLICATION_CREDENTIALS']:
        for entry in os.listdir('.'):
            if entry[-5:] == ".json":
                os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = entry


def main():

    args = parse_args()

    get_credentials(args.json_file)

    cache.set_base_dir("/var/cache/txttomp3")

    tmpd = tempfile.mkdtemp()
    atexit.register(shutil.rmtree, tmpd)

    infile = args.text_file
    outfile = os.path.splitext(infile)[0] + ".mp3"

    lines = open(infile, 'r').read().split('\n')

    for line in lines:
        if len(line) > 4800:
            print("Error: paragraph too long\n\n")  # noqa
            print(line)                             # noqa
            sys.exit(1)

    audios = []
    for line in lines:
        # limit ourselves to 250 calls/min, and 100000 chars/min
        with rate_limit(60./250, 60./100000 * len(line)):
            tmpfl = tempfile.mktemp(suffix=".mp3", dir=tmpd)

            mp3data = synthesize_text(args.speaker, args.language_code, line)

            with open(tmpfl, 'wb') as fp:
                fp.write(mp3data)

            audios.append(tmpfl)

    lstfile = tempfile.mktemp(suffix=".list", dir=tmpd)

    with open(lstfile, 'w') as fp:
        fp.write('\n'.join(["file '%s'" % x for x in audios]))

    cmd = "ffmpeg -y -f concat -safe 0 -i %s -c copy %s" % (lstfile, outfile)
    subprocess.call(shlex.split(cmd), stdout=devnull, stderr=subprocess.STDOUT)

    tags = ID3(outfile)
    tags["TIT2"] = TIT2(encoding=3, text=os.path.splitext(outfile)[0])
    tags.save()


if __name__ == "__main__":
    main()
