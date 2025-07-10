<div align="center">
  <h1 align="center">🌐 Web2PDF Converter</h1>

  <p align="center">
    Convert URLs, PDFs, DOCX, and Google Docs into clean, numbered PDF snapshots with ease.
    <br />
    Built with Python, Flask, Playwright, and a beautifully responsive UI.
    <br />
    <a href="#about-the-project"><strong>Explore Features »</strong></a>
  </p>
</div>

---

## 📌 About the Project

The **Web2PDF Converter** is a full-stack Python web app that extracts links from:
- Raw text input
- PDF / DOCX uploads
- Public Google Docs

It renders each webpage using a headless browser, bypasses Cloudflare, auto-scrolls to load full content, removes popups, and **saves a clean PDF** for each link.

✨ Features:
- 🎯 Link extraction from diverse formats (Google Docs, DOCX, PDF)
- 🧠 Auto-expands long pages (scrolls, expands "read more")
- 🔐 Cloudflare detection bypass
- 📄 Auto-saves pages as numbered PDFs
- 📦 ZIP of all PDFs + CSV report
- ⚡ Confetti animation, live status updates, responsive design
- ☀️ Light/Dark mode, mobile-friendly, and cancel button for long jobs

---

## 🚀 Live Demo

Coming Soon on: [https://web2pdf.publicvm.com](https://web2pdf.publicvm.com)

---

## 🛠 Built With

This modern stack powers the app:

- 💻 Python 3.11+
- 🧪 Flask
- 🕸️ Playwright
- 📄 Pandas + ReportLab
- 🎨 HTML + CSS (Responsive with JS Enhancements)
- 📦 Bootstrap Icons + Confetti.js

---

## 🧰 Getting Started

### Prerequisites

- Python 3.11+
- pip / venv
- Chrome browser (Playwright auto-installs)
- GitHub + DigitalOcean (for deployment)

### Installation

```bash
# Clone the repository
git clone https://github.com/skumar54uncc/Web2PDF.git
cd Web2PDF

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright browser drivers
playwright install

# Run the app locally
python app.py
```
## 🖥️ Usage

1. Go to `http://127.0.0.1:5000` in your browser.
2. Paste one or more URLs into the textbox **or** upload a PDF/DOCX file.
3. Optionally, enter a public Google Doc link to auto-extract links.
4. Click on **"Extract Links & Process"**.
5. The tool will:
   - Visit each link (scroll, expand, bypass Cloudflare)
   - Save clean snapshots as **PDFs**
   - Create a **CSV report** with link order and titles
   - Bundle everything in a downloadable **ZIP**

✅ You’ll see animated progress, status updates, confetti 🎉 on success, and can cancel anytime.

## 📦 Project Structure

Web2PDF/
│
├── templates/ # Frontend HTML (Jinja)
│ └── index.html # The main web UI
│
├── static/ # Assets like CSS, JS, icons (optional split)
│
├── app.py # Flask web server
├── pdf_handler.py # Core PDF generation and Playwright logic
├── utils.py # Helper functions for link extraction
│
├── requirements.txt # Python dependencies
├── Procfile # For deployment on platforms like Heroku/DigitalOcean
├── README.md # This file

Web2PDF/
│
├── templates/ # Frontend HTML (Jinja)
│ └── index.html # The main web UI
│
├── static/ # Assets like CSS, JS, icons (optional split)
│
├── app.py # Flask web server
├── pdf_handler.py # Core PDF generation and Playwright logic
├── utils.py # Helper functions for link extraction
│
├── requirements.txt # Python dependencies
├── Procfile # For deployment on platforms like Heroku/DigitalOcean
├── README.md # This file

## 👨‍💻 Author

**Shailesh Kumar**  
📧 shailesh.entrant@gmail.com
🔗 [GitHub](https://github.com/skumar54uncc)

## 🙏 Acknowledgments

- [Playwright for Python](https://playwright.dev/python/)
- [Flask Framework](https://flask.palletsprojects.com/)
- [Canvas Confetti.js](https://www.kirilv.com/canvas-confetti/)
- [Font Awesome Icons](https://fontawesome.com/)
- [DigitalOcean Deployment Guide](https://docs.digitalocean.com/)
- [OpenAI ChatGPT](https://openai.com/chatgpt) — for guidance and UI improvements 😄

---

> ⭐ If you found this project useful or inspiring, please consider giving it a star on GitHub!