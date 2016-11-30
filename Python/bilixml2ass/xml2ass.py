#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import json
import logging
import os
import sys

def get_video_size(media_urls):
    '''Determine the resolution of the video

    Arguments: [media_urls]

    Return value: (width, height)
    '''
    try:
        ffprobe_command = ['ffprobe', '-loglevel', 'repeat+warning', '-print_format', 'json', '-select_streams', 'v:0', '-show_streams', media_urls]
        # log_command(ffprobe_command)
        ffprobe_process = subprocess.Popen(ffprobe_command, stdout=subprocess.PIPE)
        try:
            ffprobe_output = json.loads(ffprobe_process.communicate()[0].decode('utf-8', 'replace'))
        except KeyboardInterrupt:
            logging.warning('Cancelling getting video size, press Ctrl-C again to terminate.')
            ffprobe_process.terminate()
            return 0, 0
        width, height, widthxheight = 0, 0, 0
        for stream in dict.get(ffprobe_output, 'streams') or []:
            if dict.get(stream, 'width')*dict.get(stream, 'height') > widthxheight:
                width, height = dict.get(stream, 'width'), dict.get(stream, 'height')
        return width, height
    except Exception as e:
        print(e)
        return 0, 0

def generate_ass(video_path, subtitle_path):
    width, height = get_video_size(video_path)
    out_path = os.path.splitext(video_path)[0] + '.ass'
    danmu2ass_command = ['./danmaku2ass.py', '-o', out_path, '-fs', '16', '-f', 'Bilibili', '-dm', '12', '-s', '%dx%d' % (width, height), subtitle_path]
    subprocess.Popen(danmu2ass_command, stdout=subprocess.PIPE)

def main():
    if len(sys.argv) < 3:
        print('Usage: %s <video> <subtitle>' % sys.argv[0])
        exit(0)
    generate_ass(sys.argv[1], sys.argv[2])

if __name__ == '__main__':
    main()

