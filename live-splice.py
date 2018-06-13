from moviepy.editor import *
from pathlib import Path
import datetime
import click


def read_cut_data(cut_data, video_end_timecode):
    first_cut = "00:00:00"
    last_cut = None

    cut_list = []

    lines = cut_data.split("\n")
    for line in lines:
        if line.startswith("START"):
            pass
        elif line.startswith("STOP"):
            pass
        elif len(line) == 0:
            pass
        else:
            if last_cut is None:
                last_cut = first_cut

            cut_list.append([last_cut, line])
            last_cut = line

    cut_list.append([last_cut, video_end_timecode])

    return cut_list


def add_transitions(vid):
    t1 = vfx.fadein(clip=vid, duration=0.25)
    t2 = vfx.fadeout(clip=t1, duration=0.25)
    return t2


@click.command()
@click.option('-m', help='Movie file to splice')
@click.option('-c', help='Text file from OBS InfoWriter with cut times')
def splice_video(m, c):
    # Read the video
    src = VideoFileClip(m)

    # Get it's length
    length = datetime.timedelta(seconds=int(src.duration))
    last_timecode = str(length)

    # Determine cut points
    cut_file = Path(c)
    dt = "-".join(cut_file.stem.split("-")[:-1])
    print("Date is", dt)

    cut_data = cut_file.read_text()
    cuts = read_cut_data(cut_data, last_timecode)

    # setup outro
    # create from image
    outro_img = ImageClip("outro-logo.png", duration=9)
    outro_vid = add_transitions(outro_img)

    # create sub-clips
    videos = [src.subclip(cut[0], cut[1]) for cut in cuts]

    # add transitions
    clips = [add_transitions(video) for video in videos]

    # add outro
    # highlights = [concatenate_videoclips([clip, outroVid]) for clip in clips]
    highlights = [concatenate_videoclips([clip, outro_vid]) for clip in clips]

    # create output
    for h, highlight in enumerate(highlights):
        highlight.write_videofile(f"output/{dt}-h{h}.mp4", fps=30)


if __name__ == "__main__":
    splice_video()