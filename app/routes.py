from flask import Blueprint, render_template, request, send_file, redirect, url_for
from app.pdf_handler import process_links_to_pdf
import os
import tempfile
import asyncio

main = Blueprint("main", __name__)

@main.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@main.route("/upload", methods=["POST"])
def upload():
    urls = request.form.get("urls", "").strip().splitlines()
    gdoc = request.form.get("gdoc", "").strip()
    file = request.files.get("file")

    links = [u.strip() for u in urls if u.strip()]
    if gdoc:
        links.append(gdoc)

    if file and file.filename:
        filepath = os.path.join(tempfile.gettempdir(), file.filename)
        file.save(filepath)

        ext = file.filename.lower().split(".")[-1]
        if ext == "pdf":
            from app.utils import extract_links_from_file
            links += extract_links_from_file(filepath)
        elif ext == "docx":
            from app.utils import extract_links_from_docx
            links += extract_links_from_docx(filepath)

    zip_path = asyncio.run(process_links_to_pdf(links))

    return send_file(zip_path, as_attachment=True)
    
@main.route("/reset")
def reset_app():
    from app.utils import clear_outputs
    clear_outputs()
    return redirect(url_for("main.home"))
