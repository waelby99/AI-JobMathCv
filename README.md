# 🧠 JobMatch AI 

**JobMatch AI** is a desktop application built with Python and Tkinter that helps you find job listings that match the skills extracted from your CV. It scrapes job listings from **LinkedIn** and **Indeed**, automatically detects technical skills from your resume (PDF format), and matches them to job postings in real-time.

## 🚀 Features

- 📝 **PDF CV Parsing** — Extracts your skills from a PDF resume using `PyMuPDF`.
- 🤖 **AI Skill Matching** — Detects technologies, languages, and frameworks from your CV.
- 🌍 **Job Scraping** — Searches jobs on **LinkedIn** and **Indeed** using custom filters.
- 🧩 **GUI Interface** — User-friendly Tkinter interface for uploading CVs, managing keywords, and viewing job matches.
- 📦 **Save Results** — Export matching jobs to JSON for later reference.


## 📦 Requirements

- Python 3.7+
- Packages:
  - `fitz` (PyMuPDF)
  - `requests`
  - `bs4` (BeautifulSoup)
  - `tkinter` (built-in with Python)
  - `threading`, `json`, `datetime`, etc.

Install dependencies with:

```bash
pip install pymupdf requests beautifulsoup4
```

## 🔧 How to Use

1. Clone the repo:
   ```bash
   git clone https://github.com/waelby99/AI-JobMathCv.git
   cd AI-JobMathCv
   ```

2. Run the app:
   ```bash
   python aijobmatch.py
   ```

3. Upload your CV (PDF).
4. Automatically detected skills will be shown — you can edit or add more.
5. Click **Find Matching Jobs** and browse matching results.

## 📚 Tech Stack

- **Frontend:** Tkinter (GUI)
- **Backend:** Python
- **PDF Parsing:** PyMuPDF
- **Scraping:** `requests`, `BeautifulSoup`
- **Job Sources:** LinkedIn + Indeed

## 🛡 Disclaimer

- This tool is for educational and personal use only.
- Be mindful of scraping terms of service on job platforms like LinkedIn and Indeed.
- This is not affiliated with or endorsed by any job board.

## 📄 License

MIT License
