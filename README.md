# radio_crawl

Some simple scripts to crawl, dump and tag MP3 files from internet radios.
This is to create a local directory of automatically genre-labelled MP3 files.
Avoid streaming, save the planet.

## Setting up

Requires a Unix-style environment and Python3 ;)

*Pre-requisites*:
- `streamripper` (`sudo apt install streamripper`)
- `ffprobe` (`sudo apt install ffmpeg`)
- `mp3-tagger` (`pip3 install mp3-tagger`)

*Cloning*:

  $> git clone https://github.com/chiarcos/radio_crawl

Edit `record-music.sh` with your favorite radios and directory preferences. (See https://onlineradiobox.com to find some.) It currently has a space limit of 1 GB (`-M 1000`) per station *per call*, you might want to change this. Stations differ in quality, so you might want to put each source into a different directory.

## Recording

  $> radio_crawl/record-music.sh

Now, wait for a day ;)

Note: Running `record-music.sh` will spawn parallel processes. If you run two instances of `record-music.sh` in parallel, they will overwrite each other's output.

## Managing

Use your audioplayer of choice to fix and prune (delete!) the resulting files and their metadata. We have some helper scripts.

*Maintaining*:

When running for a few days, this will dump a lot of data. Track the size of your music directory using `du -h /ADD/YOUR/MUSIC_FOLDER(S)`.

> Before starting another instance or doing any maintanance or tagging operation, make sure to kill all `streamripper` processes, e.g., using `$> pkill streamripper`

  $> radio_crawl/remove-duplicates.sh /ADD/YOUR/MUSIC_FOLDER(S)

This will eliminate duplicates (same name, same directory). Should not be run in parallel with `record-music.sh`.

*Tagging* (fixing metadata):

The retrieved music will mostly lack metadata. For subsequent filtering, we extrapolate ID3v2 genre information from your local music library and last.fm.

  $> python3 radio_crawl/artist2genre.py /ADD/YOUR/LIBRARY

This call is optional and will use your local MP3 files (in your library) to bootstrap a mapping from artists to genres. The resulting mapping is stored in `artist2genre.json`.

  $> python3 radio_crawl/artist2genre.py /ADD/YOUR/MUSIC_FOLDER(S) --add_genre

This will update all *.mp3 files in the provided directories with genre information if they lacked it before, using one of the following principles:

  - if an artist is tagged for a genre in the directories, we apply the most frequent tag to all other songs of that artist that don't have genre tags; otherwise
  - if an artist does have a genre tag in `artist2genre.json`, apply it; otherwise
  - if an artist can be found on last.fm, retrieve the first tag as candidate genre (you can define additional filters in `radio_crawl/artist2genre.py`). if it loosely matches anything in your existing genre annotations, normalize its spelling accordingly. Inferred genres that have not previously been used are marked with `*`, so that you can filter and manually correct them in your audio player.
  - if an artist cannot be found, but there is a close match (dropping numbers, dropping characters other than `[a-zA-Z ]`), use that genre tag, but append `*`. This is because some stations put the playlist number into the artist field. Check, filter and fix these `*` categories. Often, within a genre, there will be just one artist with that tag, so it is easier to fix artist and metadata for all their songs.

Note that existing ID3 metadata will always take priority in this process and will only be changed if genre information is absent. Last.fm will only be consulted for unknown artist, `artist2genre.py` creates an internal classification of artists to default genres along the way, but this will be overridden if your local libraries use a different tag with higher frequency.

Should not be run in parallel with `record-music.sh`.
