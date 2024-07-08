#!/bin/bash

# record a number of favorite stations
# selected stations from https://onlineradiobox.com
# cf https://itectec.com/ubuntu/ubuntu-gui-program-to-record-internet-radio-with-songs-tags-title-artist-etc/
# stations from their registered internet radios

# streamripper http://185.14.252.141:8040/listen.pls -u "Mozilla/5.0 (Mobile; nnnn; rv:26.0) Gecko/26.0 Firefox/26.0" -D ~/Desktop/music/www.metalheartradio.com/ -M 1000 2>&1 >> 1.log &
  # nice music, but skrews up artist metadata

# starting to be repetitive (but ok, we just delete repetitions)
streamripper http://uk1.internet-radio.com:8294/live.m3u -u "Mozilla/5.0 (Mobile; nnnn; rv:26.0) Gecko/26.0 Firefox/26.0" -D ~/Desktop/music/www.RadioBloodstream.com/ -M 1000 2>&1 >> 3.log &
streamripper http://192.111.140.6:9772/listen.pls -u "Mozilla/5.0 (Mobile; nnnn; rv:26.0) Gecko/26.0 Firefox/26.0" -D ~/Desktop/music/www.SanctuaryRadio.com/ 2>&1 >> 4.log &

streamripper http://cast2.my-control-panel.com:8026/autodj -u "Mozilla/5.0 (Mobile; nnnn; rv:26.0) Gecko/26.0 Firefox/26.0" -D ~/Desktop/music/www.rockradio.lt/ -M 1000 2>&1 >> 2.log &
streamripper http://5.35.214.196:8000/listen.pls  -u "Mozilla/5.0 (Mobile; nnnn; rv:26.0) Gecko/26.0 Firefox/26.0" -D ~/Desktop/music/darkedge.ro/ -M 1000 2>&1 >> 7.log &
streamripper http://stream.laut.fm/wavebreaker.m3u  -u "Mozilla/5.0 (Mobile; nnnn; rv:26.0) Gecko/26.0 Firefox/26.0" -D ~/Desktop/music/laut.fm.wavebreaker/ -M 1000 2>&1 >> 8.log &
streamripper http://stream.laut.fm/synthpop.m3u -u "Mozilla/5.0 (Mobile; nnnn; rv:26.0) Gecko/26.0 Firefox/26.0" -D ~/Desktop/music/laut.fm.synthpop/ -M 1000 2>&1 >> 9.log &
streamripper http://stream.laut.fm/schwarzeszene.m3u -u "Mozilla/5.0 (Mobile; nnnn; rv:26.0) Gecko/26.0 Firefox/26.0" -D ~/Desktop/music/schwarzeszene/ -M 1000 2>&1 >> 10.log &
streamripper http://stream.laut.fm/romance.m3u -u "Mozilla/5.0 (Mobile; nnnn; rv:26.0) Gecko/26.0 Firefox/26.0" -D ~/Desktop/music/laut.fm.romance/ -M 1000 2>&1 >> 11.log &
streamripper http://channel.angelsradio.ru:9000/angels -u "Mozilla/5.0 (Mobile; nnnn; rv:26.0) Gecko/26.0 Firefox/26.0" -D ~/Desktop/music/angelsradio.ru/ -M 1000 2>&1 >> 12.log &
streamripper http://stream.laut.fm/dark-sound-united.m3u  -u "Mozilla/5.0 (Mobile; nnnn; rv:26.0) Gecko/26.0 Firefox/26.0" -D ~/Desktop/music/dark-sound-united/ -M 1000 2>&1 >> 13.log &
streamripper http://stream.laut.fm/mittelalter-net.m3u -u "Mozilla/5.0 (Mobile; nnnn; rv:26.0) Gecko/26.0 Firefox/26.0" -D ~/Desktop/music/mittelalter-net/ -M 1000 2>&1 >> 15.log &
streamripper https://allzic27.ice.infomaniak.ch/allzic27.mp3 -u "Mozilla/5.0 (Mobile; nnnn; rv:26.0) Gecko/26.0 Firefox/26.0" -D ~/Desktop/music/alzic-gothique.ch/ -M 1000 2>&1 >> 17.log &

# apparently dead
# streamripper http://192.111.140.6:8084/listen.pls -u "Mozilla/5.0 (Mobile; nnnn; rv:26.0) Gecko/26.0 Firefox/26.0" -D ~/Desktop/music/www.rosanegraradio.com/ -M 1000 2>&1 >> 5.log &
# streamripper http://66.55.145.43:7744/listen.pls -u "Mozilla/5.0 (Mobile; nnnn; rv:26.0) Gecko/26.0 Firefox/26.0" -D ~/Desktop/music/crimradio.rocks/ -M 1000 2>&1 >> 6.log &
# streamripper http://stream.laut.fm/snakedance.m3u -u "Mozilla/5.0 (Mobile; nnnn; rv:26.0) Gecko/26.0 Firefox/26.0" -D ~/Desktop/music/snakedance/ -M 1000 2>&1 >> 14.log &
# streamripper https://radio.metal-invasion.fr/radio/8000/stream.mp3 -u "Mozilla/5.0 (Mobile; nnnn; rv:26.0) Gecko/26.0 Firefox/26.0" -D ~/Desktop/music/metal-invasion.fr/ -M 1000 2>&1 >> 16.log &
# streamripper http://138.201.234.215:10080/stream -u "Mozilla/5.0 (Mobile; nnnn; rv:26.0) Gecko/26.0 Firefox/26.0" -D ~/Desktop/music/darkradio.de/ -M 1000 2>&1 >> 18.log &
# streamripper "http://stream.rockyou.fm/;stream.nsv" -u "Mozilla/5.0 (Mobile; nnnn; rv:26.0) Gecko/26.0 Firefox/26.0" -D ~/Desktop/music/rockyou-fm.de/ -M 1000 2>&1 >> 19.log &
# streamripper http://216.144.247.101:8130/live -u "Mozilla/5.0 (Mobile; nnnn; rv:26.0) Gecko/26.0 Firefox/26.0" -D ~/Desktop/music/dark-radio-brasil/ -M 1000 2>&1 >> 20.log &
