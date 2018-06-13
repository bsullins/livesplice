# livesplice
chop up a video into highlights

# idea
automate the creation of highlights from live stream

# missing
- auto upload to youtube

# installation
- install moviepy `(sudo) pip install moviepy`
- install click `(sudo) pip install click`

# setup
- While streaming from OBS, use OBS InfoWriter hotkey to log timestamps
- Configrue InfoWriter to use date in filename like so  `%F-live.txt`

# creating highlights
- Run from command line with movie file (-m) and cut list (-c)

`$ python live-splice.py -m /Users/ben/Movies/2018-06-13_13-50-45.mp4 -c /Users/ben/YouTube/live-log/2018-06-13-live.txt
`