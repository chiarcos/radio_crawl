import sys,re,os,traceback,json
import subprocess
from subprocess import PIPE

def norm_genre(string : str):
    return re.sub(r"[^0-9a-z]","",string.lower())

def help():
    sys.stderr.write("""synopsis: artist2genre [--help|-h|-?] [--add_genre] DIR[1..n]
        --help      print this message and exit
        --add_genre update mp3 files with genre information, mark by final '*'
        DIR         one or more files or directories that contain MP3 files
        given one or more directories, retrieve artists and genre. with --add_genre,
        add genre to untagged MP3s\n""")
    sys.exit()

if len(sys.argv)<=1 or "--help" in sys.argv or "-h" in sys.argv or "-?" in sys.argv:
    help()

add_genre="--add_genre" in sys.argv

dir_path = os.path.dirname(os.path.realpath(__file__))

cache=os.path.join(dir_path,"artist2genre.json")

# to do some post-crawling pruning
# preferences are expressed as substrings, see below
dispreferred=set(["unknown", "Unknown", "2", "50 Cent", "Artists I have seen Live", "Awesome", "bedroom pop", "better than selena gomez", "bon temps du rock and roll", "brazilian", "brighton", "british invasion", "brown music for pink people", "Canadian", "canadians", "Cream", "crossover", "crossover thrash metal", "Czech Republic", "damon albarn", "Danger Mouse", "dark cabaret", "Deep Purple family", "drill", "electro body", "finland", "francais", "gary lightbody", "glo-fi", "guitar trio", "Hard and Blues", "Hardtek", "Herbie Langhans", "Hooligans", "Hotel Costes", "im cheesing my fucking brain out", "industrial jungle pussy punk", "international band", "japanese", "japanese grime", "jimi hendrix", "katy perry", "kenny wayne shepherd", "lounge and chillout", "Love Metal", "male vocalists", "martial industrial", "melancholic", "minimalistic", "mistagged artist", "Mittelalter", "Motorhead", "music for skinheads", "music i tried but didnt like", "netherlands", "New Orleans", "New Zealand", "next level beats", "Nintendocore", "noise", "not alternative rock", "powernoise", "power pop", "Rhythmic Noise", "rock-hard", "Romanian", "salt lake city", "sexysExxxxy", "slow jamz", "somafm", "south africa", "spotify", "the hazy hollow", "trashbags", "underrated essentials", "United States", "video game music", "wellington flash black", "argentina", "chaotic hardcore", "chillwave", "East Coast", "icelandic", "indietronica", "shoegaze", "Skinny Puppy related", "switzerland", "witch house", "australian", "down tempo", "indie folk", "madchester", "sleaze rock", "Electroclash", "guitar virtuoso", "United Kingdom", "experimental", "under 2000 listeners", "seen live","2", "50 Cent", "Absolut deafers", "Artists I have seen Live", "Awesome", "better than selena gomez", "Black", "Black Sabbath", "bon temps du rock and roll", "brazilian", "brighton", "brown music for pink people", "Canadian", "canadians", "chamber pop", "christmas", "Cream", "crossover", "Czech Republic", "damon albarn", "Danger Mouse", "dark cabaret", "Deep Purple family", "drill", "finland", "francais", "gary lightbody", "glo-fi", "guitar trio", "Hard and Blues", "Herbie Langhans", "Hooligans", "Hotel Costes", "im cheesing my fucking brain out", "industrial jungle pussy punk", "international band", "japanese", "japanese grime", "jimi hendrix", "juglar metal", "katy perry", "kenny wayne shepherd", "lounge and chillout", "Love Metal", "male vocalists", "melancholic", "minimalistic", "mistagged artist", "Mittelalter", "Motorhead", "music for skinheads", "music i tried but didnt like", "nederhop", "netherlands", "New Orleans", "New Zealand", "next level beats", "Nintendocore", "noise", "not alternative rock", "nouvelle chanson francaise", "powernoise", "power pop", "Progressive", "psychobilly", "punk rock", "Rhythmic Noise", "rock alternativo", "Romanian", "salt lake city", "sexysExxxxy", "slow jamz", "somafm", "south africa", "spotify", "the hazy hollow", "trashbags", "underrated essentials", "United States", "video game music", "wellington flash black", "argentina", "chaotic hardcore", "chillwave", "dream pop", "East Coast", "icelandic", "indietronica", "shoegaze", "Skinny Puppy related", "witch house", "australian", "down tempo", "madchester", "sleaze rock", "Electroclash", "guitar virtuoso", "United Kingdom", "experimental", "under 2000 listeners", "seen live"])

genre2freq={}
artist2genre2freq={}
unclassified_artists=[]
artist2genre={}

if os.path.exists(cache):
    with(open(cache)) as input:
        artist2genre=json.load(input)
    artist2genre= { artist : genre for artist, genre in artist2genre.items() if not genre in dispreferred or genre+"*" in dispreferred }
    artist2genre2freq = { artist : { genre : 0 } for artist, genre in artist2genre.items() }
    for _,g in artist2genre.items():
        if not g in genre2freq:
            genre2freq[g]=1
        else:
            genre2freq[g]+=1

files=sys.argv[1:]
while(len(files)>0):
    file=files[0]
    files=files[1:]
    if os.path.exists(file):
        if os.path.isdir(file):
            for f in os.listdir(file):
                files.append(os.path.join(file,f))
        else:
            feats={}
            if "-" in os.path.basename(file):
                feats["artist"] = [ os.path.basename(file).split("-")[0].strip() ]
            ffprobe=subprocess.Popen(["ffprobe",file,"-show_entries","format_tags=artist,genre"],stdout=PIPE, stderr=PIPE)
            stdout, stderr=ffprobe.communicate()
            tags=stdout.decode("utf-8").split("\n")
            tags=[ ":".join(tag.split(":")[1:]).strip() for tag in tags if tag.lower().startswith("tag:")]
            tags=[ (tag.split("=")[0].strip(), "=".join(tag.split("=")[1:]).strip()) for tag in tags]
            for feat,val in tags:
                if feat in feats:
                        if not val in feats[feat]:
                            feats[feat].append(val)
                else:
                        feats[feat]=[val]

            if len(feats)>0:
                artist=feats["artist"][-1].lower().strip()
                if "genre" in feats:
                    for genre in feats["genre"]:
                        if not genre.endswith("*"): # these are unconfirmed categories
                            if not genre in genre2freq:
                                genre2freq[genre]=1
                            else:
                                genre2freq[genre]+=1
                            if not artist in artist2genre2freq:
                                artist2genre2freq[artist] = { genre : 1 }
                            elif not genre in artist2genre2freq[artist]:
                                artist2genre2freq[artist][genre]=1
                            else:
                                artist2genre2freq[artist][genre]+=1
                            while artist in unclassified_artists:
                                unclassified_artists.remove(artist)
                elif not artist in artist2genre2freq:
                    if not artist in unclassified_artists:
                        unclassified_artists.append(artist)

            sys.stderr.write(str(len(genre2freq))+" genres, "+str(len(artist2genre2freq))+" classified artists, "+str(len(unclassified_artists))+" unclassified\r")
            sys.stderr.flush()
            # artist_t=
            # print(file,feats)

sys.stderr.write("\n")

norm2genres={}
for g in genre2freq:
    norm=norm_genre(g)
    if norm in norm2genres:
        if not g in norm2genres[norm]:
            norm2genres[norm].append(g)
    else:
        norm2genres[norm]=[g]
for n,genres in list(norm2genres.items()):
    genres=list(genres)
    genre=genres[0]
    for g in genres:
        if not genre in genre2freq or (g in genre2freq and genre2freq[g] > genre2freq[genre]):
            genre=g
    norm2genres[n]=[genre]

sys.stderr.write("consult lastfm\n")
for artist in unclassified_artists:
    lastfm=subprocess.Popen(["curl","http://ws.audioscrobbler.com/2.0/?method=artist.getinfo&artist="+re.sub(r"\s+","%20",artist)+"&autocorrect=0&api_key=2b950d5fa92d92dec12801d84dcc9941&format=json"],stdout=PIPE, stderr=PIPE)
    stdout, stderr=lastfm.communicate()
    # if stderr:
    #     sys.stderr.write(stderr.decode("utf-8")+"\n")
    #     sys.stderr.flush()
    if stdout:
        # print(stdout,stdout.decode("utf-8"))
        result= json.loads(stdout) # stdout.decode("utf-8").split("\n")
        if type(result)==dict:
            result=[result]
        tags=[]
        try:
            for r in result:
                for tag in r["artist"]["tags"]["tag"]:
                    tag=tag["name"]
                    if not tag in tags:
                        tags.append(tag)

            genre=None

            # my personal tag preferences ;)
            if genre==None:
                for t in tags:
                    normt=norm_genre(t)
                    if "metal" or "female" or "punk" or "goth" or "grunge" or "folk" or "wave" or "synth" in normt:
                        if genre==None or len(t) > len(genre):
                            if normt in norm2genres:
                                genre=norm2genres[normt][0]
                            else:
                                genre=t+"*" # marks automatically created genres

            # take the longest term that overlaps with known genres
            if genre==None:
                for t in tags:
                    normt=norm_genre(t)
                    # print(normt,norm2genres)
                    if normt in norm2genres:
                        cand=norm2genres[normt][0]
                        # print("=>",cand,"?")
                        if genre==None or len(cand)>len(genre):
                            genre=cand
                            # print("=>",cand,"!")

            if genre==None and len(tags)>0:
                while tags[0] in dispreferred and len(tags)>1:
                    tags=tags[1:]
                genre=tags[0]+"*"   # marks automatically created genres, first should be most prototypical

            if genre!=None:
                normg=norm_genre(genre)
                if not normg in norm2genres:
                    norm2genres[normg]=[genre]

                artist2genre[artist]=genre
                print(artist,"=>",genre)
        except:
            traceback.print_exc()


sys.stderr.write("save to "+cache)
with(open(cache,"w")) as output:
    for artist in artist2genre2freq:
        freq=0
        for g,f in artist2genre2freq[artist].items():
            if not artist in artist2genre or f>freq or (f==freq and genre2freq[g]>genre2freq[artist2genre[artist]]):
                freq=f
                artist2genre[artist]=g
    json.dump(artist2genre,output)
sys.stderr.write(" .. saved\n")

if add_genre:

    from mp3_tagger import MP3File, VERSION_1, VERSION_2, VERSION_BOTH

    files=sys.argv[1:]
    while(len(files)>0):
        file=files[0]
        files=files[1:]
        if os.path.exists(file):
            if os.path.isdir(file):
                for f in os.listdir(file):
                    files.append(os.path.join(file,f))
            elif file.lower().endswith("mp3"):
                feats={}
                if "-" in os.path.basename(file):
                    feats["artist"] = [ os.path.basename(file).split("-")[0].strip() ]
                ffprobe=subprocess.Popen(["ffprobe",file,"-show_entries","format_tags=artist,genre"],stdout=PIPE, stderr=PIPE)
                stdout, stderr=ffprobe.communicate()
                tags=stdout.decode("utf-8").split("\n")
                tags=[ ":".join(tag.split(":")[1:]).strip() for tag in tags if tag.lower().startswith("tag:")]
                tags=[ (tag.split("=")[0].strip(), "=".join(tag.split("=")[1:]).strip()) for tag in tags]
                for feat,val in tags:
                    if feat in feats:
                            if not val in feats[feat]:
                                feats[feat].append(val)
                    else:
                            feats[feat]=[val]

                if len(feats)>0:
                    artist=feats["artist"][-1].lower().strip()
                    for norm_artist in [ artist, re.sub(r"[^a-zA-Z 0-9]","",artist).strip(), re.sub(r"[^a-zA-Z ]","",artist).strip() ]:
                        if not "genre" in feats or feats["genre"] == None or len(feats["genre"])==0:
                            if len(norm_artist)>0 and norm_artist in artist2genre:
                                genre=artist2genre[norm_artist] #+"*" # this is actually quite ok
                                genre="".join(genre.split('"'))
                                if artist!=norm_artist:
                                    if not genre.endswith("*"):
                                        genre=genre+"*"
                                bak=file+".bak"
                                if not os.path.exists(bak):
                                    subprocess.call(["cp",file,bak])
                                subprocess.call(["ffmpeg","-i",bak,"-metadata","genre="+genre,"-codec","copy","-y",file])
                                os.remove(bak)
                                break
