
import os, shutil, subprocess, tempfile, uuid
from pathlib import Path
from flask import Flask, request, render_template, send_from_directory, redirect, url_for, flash

BASE = Path(__file__).resolve().parent
UPLOADS = BASE / "uploads"
OUTPUTS = BASE / "outputs"
UPLOADS.mkdir(exist_ok=True)
OUTPUTS.mkdir(exist_ok=True)

app = Flask(__name__)
app.secret_key = "change-this-secret-key"

ALLOWED = {".mp4", ".mov", ".mkv", ".avi", ".webm", ".m4v"}

def cartoon_filter(input_path, output_path):
    # FFmpeg-only cartoon look: edge detection + color reduction.
    # This is lightweight and does not require a paid AI API.
    vf = (
        "scale='min(1280,iw)':-2:force_original_aspect_ratio=decrease,"
        "fps=24,"
        "split=2[a][b];"
        "[a]format=rgb24,edgedetect=mode=colormix:high=0.08:low=0.02,"
        "negate[edges];"
        "[b]format=rgb24,eq=saturation=1.35:contrast=1.08:brightness=0.02,"
        "posterize=6[base];"
        "[base][edges]blend=all_mode=multiply:all_opacity=0.55,"
        "unsharp=5:5:0.4:5:5:0"
    )
    cmd = [
        "ffmpeg", "-y", "-i", str(input_path),
        "-vf", vf,
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "22",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "128k",
        "-movflags", "+faststart",
        str(output_path)
    ]
    subprocess.run(cmd, check=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        f = request.files.get("video")
        if not f or not f.filename:
            flash("Please choose a video.")
            return redirect(url_for("index"))

        ext = Path(f.filename).suffix.lower()
        if ext not in ALLOWED:
            flash("Supported formats: MP4, MOV, MKV, AVI, WEBM, M4V.")
            return redirect(url_for("index"))

        job = uuid.uuid4().hex
        src = UPLOADS / f"{job}{ext}"
        out = OUTPUTS / f"{job}_animation.mp4"
        f.save(src)

        try:
            cartoon_filter(src, out)
        except FileNotFoundError:
            flash("FFmpeg is not installed. Install FFmpeg first.")
            src.unlink(missing_ok=True)
            return redirect(url_for("index"))
        except subprocess.CalledProcessError:
            flash("Conversion failed. Try another video.")
            src.unlink(missing_ok=True)
            out.unlink(missing_ok=True)
            return redirect(url_for("index"))

        src.unlink(missing_ok=True)
        return render_template("result.html", filename=out.name)

    return render_template("index.html")

@app.route("/download/<filename>")
def download(filename):
    return send_from_directory(OUTPUTS, filename, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
