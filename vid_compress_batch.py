#!/usr/bin/python3

# scan through all mp4 and mov files in the current directory and subdirectory. If the bitrate is larger than 500kbps, compress it to 500kbps.

import argparse
import os
import sys
import shutil
import subprocess

DEFAULT_VIDEO_BITRATE = "5M" # bit/s
RECYCLE_DIR = "./recycle"


def compress_file(full_path, video_bitrate):
    """Compress a file to a target bitrate using ffmpeg."""
    directory, filename = os.path.split(full_path)
    full_path_out = os.path.join(directory, "ffzip_" + filename)
    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        full_path,
        "-max_muxing_queue_size",
        "10000",
        "-b:v",
        video_bitrate,
        full_path_out,
    ]
    res = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return res.returncode, full_path_out


def conversion_successful(full_path_out):
    """Validate that ffmpeg produced a real playable video file."""
    if not os.path.exists(full_path_out):
        return False
    if os.path.getsize(full_path_out) <= 0:
        return False

    probe_cmd = [
        "ffprobe",
        "-v",
        "error",
        "-show_entries",
        "stream=codec_type",
        "-of",
        "default=noprint_wrappers=1:nokey=1",
        full_path_out,
    ]
    probe_res = subprocess.run(
        probe_cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True,
    )
    if probe_res.returncode != 0:
        return False

    stream_types = {
        line.strip() for line in probe_res.stdout.splitlines() if line.strip()
    }
    return "video" in stream_types


def get_recycle_path(filename):
    """Return a non-conflicting path under recycle directory."""
    base, ext = os.path.splitext(filename)
    candidate = os.path.join(RECYCLE_DIR, filename)
    index = 1
    while os.path.exists(candidate):
        candidate = os.path.join(RECYCLE_DIR, f"{base}_{index}{ext}")
        index += 1
    return candidate


def scan_files(directory, video_bitrate):
    """Scan a directory and its subdirectories for mp4 and mov files."""
    if not os.path.exists(directory):
        print("no such directory:", directory)
        sys.exit(1)

    if not os.path.exists(RECYCLE_DIR):
        os.makedirs(RECYCLE_DIR)

    recycle_abs = os.path.abspath(RECYCLE_DIR)
    for foldername, subfolders, filenames in os.walk(directory):
        folder_abs = os.path.abspath(foldername)
        if folder_abs == recycle_abs or folder_abs.startswith(recycle_abs + os.sep):
            continue
        for filename in filenames:
            # is_target_name = filename.startswith('RPReplay') or filename.startswith('Screen_Recording')
            is_target_name = True
            is_target_ext = filename.lower().endswith((".mp4", ".mov"))
            if is_target_name and is_target_ext:
                full_path = os.path.join(foldername, filename)
                print("\n\n", full_path)
                print("-----------------------------------------------------------")
                exit_code, full_path_out = compress_file(full_path, video_bitrate)
                if exit_code != 0 or not conversion_successful(full_path_out):
                    print("failed!")
                    try:
                        os.remove(full_path_out)
                    except OSError:
                        pass
                    continue

                out_path = get_recycle_path(filename)
                shutil.move(full_path, out_path)

    # delete `./recycle` if it's empty
    if os.path.exists(RECYCLE_DIR) and not os.listdir(RECYCLE_DIR):
        os.rmdir(RECYCLE_DIR)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Batch compress matching replay videos."
    )
    parser.add_argument(
        "directory",
        nargs="?",
        default=".",
        help="Directory to scan (default: current directory).",
    )
    parser.add_argument(
        "--video-bitrate",
        "-b",
        default=DEFAULT_VIDEO_BITRATE,
        help=f"Value passed to ffmpeg -b:v (default: {DEFAULT_VIDEO_BITRATE}).",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    print(f"Using ffmpeg video bitrate (-b:v): {args.video_bitrate}")
    scan_files(args.directory, args.video_bitrate)


if __name__ == "__main__":
    main()
