#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse, glob, os, subprocess


def convert(input_file, output_file):
    subprocess.call(["ffmpeg", "-i", input_file, "-c:v", "copy", "-c:a", "libmp3lame", "-q:a", "0", output_file])


def basename_mp3(input_file):
    return "{}.mp3".format(os.path.splitext(os.path.basename(input_file))[0])


def iter_files(input_directory, extension):
    for input_file in glob.glob1(input_directory, "*.{}".format(extension)):
        yield os.path.join(input_directory, input_file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Converts all audio files of a given input format to MP3 VBR highest quality.")
    parser.add_argument("input_directory", nargs="+")
    parser.add_argument("--input-format", "-i", default="mp3", choices=("mp3", "ogg", "flac", "m4a",))
    parser.add_argument("--create-topdir", "-c", action="store_true")
    parser.add_argument("output_directory")

    args = parser.parse_args()

    for input_directory in args.input_directory:
        print ("Converting directory '{}'".format(input_directory))

        if args.create_topdir:
            output_directory = os.path.join(args.output_directory, os.path.basename(os.path.abspath(input_directory)))
        else:
            output_directory = args.output_directory

        if not os.path.exists(output_directory):
            os.mkdir(output_directory)
        elif not os.path.isdir(output_directory):
            raise Exception("'{}' exists but is not a directory.".format(output_directory))

        #for input_file in glob.glob(os.path.join(input_directory, "*.{}".format(args.input_format))):
        #for input_file in glob.glob1(input_directory, "*.{}".format(args.input_format)):
        for input_file in iter_files(input_directory, args.input_format):
            output_file = os.path.join(output_directory, basename_mp3(input_file)) 
            convert(input_file, output_file)
