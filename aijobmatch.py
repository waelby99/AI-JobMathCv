import fitz  # PyMuPDF for PDF parsing
import os
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
import re
import webbrowser
import threading
import json
from datetime import datetime
import time
import urllib.parse
import requests
from bs4 import BeautifulSoup
import random

class LinkedInJobScraper:
    """
    A class to scrape job listings from LinkedIn
    Handles pagination and detailed job information
    """
    
    def __init__(self, delay_between_requests=1.5):
        self.delay = delay_between_requests
        self.session = requests.Session()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Referer": "https://www.linkedin.com/",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "Cache-Control": "max-age=0"
        }
        
    def search_jobs(self, keyword, location="", max_jobs=10, job_type="", experience_level=""):
        """
        Search for jobs with the given keyword and parameters
        
        Args:
            keyword (str): The keyword to search for
            location (str): Optional location filter
            max_jobs (int): Maximum number of jobs to return
            job_type (str): Optional job type filter (e.g., "F", "C", "P", "T", "I" for full-time, contract, etc.)
            experience_level (str): Optional experience level filter
            
        Returns:
            list: A list of job dictionaries with details
        """
        all_jobs = []
        page = 0
        
        # Encode parameters for URL
        keyword_encoded = urllib.parse.quote(keyword)
        location_encoded = urllib.parse.quote(location) if location else ""
        
        # Build filter string
        filters = []
        if job_type:
            filters.append(f"f_JT={job_type}")
        if experience_level:
            filters.append(f"f_E={experience_level}")
        
        filter_string = "&".join(filters)
        if filter_string:
            filter_string = "&" + filter_string
        
        # Location parameter
        location_param = f"&location={location_encoded}" if location else ""
        
        while len(all_jobs) < max_jobs:
            # Calculate start parameter for pagination (25 results per page)
            start = page * 25
            url = f"https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords={keyword_encoded}{location_param}&start={start}{filter_string}"
            
            try:
                response = self.session.get(url, headers=self.headers, timeout=10)
                
                if response.status_code != 200:
                    break
                
                # Use BeautifulSoup for more reliable HTML parsing
                soup = BeautifulSoup(response.text, 'html.parser')
                job_cards = soup.find_all("li")
                
                if not job_cards:
                    break
                
                # Process job cards on this page
                for job_card in job_cards:
                    # Extract job details
                    job = self._extract_job_data(job_card, keyword)
                    if job:
                        all_jobs.append(job)
                        
                        # Stop if we've reached the maximum number of jobs
                        if len(all_jobs) >= max_jobs:
                            break
                
                # Random delay to avoid rate limiting
                delay = self.delay + (random.random() * 0.5)
                time.sleep(delay)
                
                # Move to next page
                page += 1
                
            except Exception as e:
                break
        
        return all_jobs[:max_jobs]
    
    def _extract_job_data(self, job_card, keyword):
        """Extract job data from a job card element"""
        try:
            # Find the job link and title
            job_link_elem = job_card.find("a", class_="base-card__full-link")
            if not job_link_elem:
                return None
                
            job_url = job_link_elem.get("href", "")
            job_title = job_link_elem.get_text().strip()
            
            # Find company name
            company_elem = job_card.find("h4", class_="base-search-card__subtitle")
            company = company_elem.get_text().strip() if company_elem else "Unknown company"
            
            # Find location
            location_elem = job_card.find("span", class_="job-search-card__location")
            location = location_elem.get_text().strip() if location_elem else "Unknown location"
            
            # Find posting date
            date_elem = job_card.find("time", class_="job-search-card__listdate")
            if date_elem:
                date = date_elem.get("datetime", "")
            else:
                # Try alternative date element
                date_elem = job_card.find("time")
                date = date_elem.get("datetime", "") if date_elem else ""
            
            # Find job ID
            job_id = ""
            data_id = job_card.get("data-id")
            if data_id:
                job_id = data_id
            else:
                # Try to extract from URL
                match = re.search(r'(?:jobs|view)/(\d+)', job_url)
                if match:
                    job_id = match.group(1)
            
            # Create job dictionary
            job = {
                "keyword": keyword,
                "job_id": job_id,
                "title": job_title,
                "company": company,
                "location": location,
                "url": job_url if job_url.startswith("http") else f"https://www.linkedin.com{job_url}",
                "date_posted": date,
                "scrape_time": datetime.now().isoformat()
            }
            
            return job
            
        except Exception as e:
            return None

class IndeedJobScraper:
    """
    A class to scrape job listings from Indeed
    (Simplified version for demonstration)
    """
    
    def __init__(self, delay_between_requests=1.5):
        self.delay = delay_between_requests
        self.session = requests.Session()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive"
        }
    
    def search_jobs(self, keyword, location="", max_jobs=10):
        """Basic Indeed job search (placeholder implementation)"""
        all_jobs = []
        
        # For demo purposes, return a fallback link
        job = {
            "keyword": keyword,
            "job_id": "indeed-fallback",
            "title": f"Search {keyword} jobs on Indeed",
            "company": "Indeed",
            "location": location if location else "Various locations",
            "url": f"https://www.indeed.com/jobs?q={urllib.parse.quote(keyword)}&l={urllib.parse.quote(location) if location else ''}",
            "date_posted": "",
            "scrape_time": datetime.now().isoformat()
        }
        all_jobs.append(job)
        
        return all_jobs

class JobMatchAgent:
    def __init__(self, root):
        self.root = root
        self.root.title("JobMatch AI ")
        self.root.geometry("900x700")
        self.root.minsize(800, 600)
        
        # Application state
        self.cv_text = ""
        self.keywords = []
        self.jobs = []
        self.search_in_progress = False
        self.scraper_options = {
            "max_jobs_per_keyword": 8,
            "locations": ["Remote"],
            "job_types": [""],
            "experience_levels": [""]
        }
        
        # Initialize scrapers
        self.linkedin_scraper = LinkedInJobScraper(delay_between_requests=1.5)
        self.indeed_scraper = IndeedJobScraper(delay_between_requests=1.5)
        
        # Set up styles
        self.style = ttk.Style()
        self.style.configure("TButton", font=("Arial", 11))
        self.style.configure("TLabel", font=("Arial", 11))
        
        # Create UI elements
        self.create_menu()
        self.create_widgets()
        
        # Load config if exists
        self.config_file = os.path.join(os.path.expanduser("~"), ".jobmatch_config.json")
        self.load_config()
    
    def create_menu(self):
        menu_bar = tk.Menu(self.root)
        
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Upload CV", command=self.upload_cv)
        file_menu.add_command(label="Save Results", command=self.save_results)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        tools_menu = tk.Menu(menu_bar, tearoff=0)
        tools_menu.add_command(label="Preferences", command=self.show_preferences)
        tools_menu.add_command(label="Clear All Data", command=self.clear_all)
        
        help_menu = tk.Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)
        
        menu_bar.add_cascade(label="File", menu=file_menu)
        menu_bar.add_cascade(label="Tools", menu=tools_menu)
        menu_bar.add_cascade(label="Help", menu=help_menu)
        
        self.root.config(menu=menu_bar)
    
    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(header_frame, text="JobMatch AI Agent", font=("Arial", 18, "bold")).pack(side=tk.LEFT)
        
        self.status_var = tk.StringVar(value="Ready")
        ttk.Label(header_frame, textvariable=self.status_var, font=("Arial", 10)).pack(side=tk.RIGHT)
        
        # Input frame
        input_frame = ttk.LabelFrame(main_frame, text="Upload and Analysis", padding="10")
        input_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(input_frame, text="Upload your CV (PDF) to extract skills and find matching jobs:").grid(row=0, column=0, sticky=tk.W, pady=5)
        
        button_frame = ttk.Frame(input_frame)
        button_frame.grid(row=1, column=0, sticky=tk.W)
        
        self.upload_button = ttk.Button(button_frame, text="Upload CV", command=self.upload_cv)
        self.upload_button.pack(side=tk.LEFT, padx=(0, 5))
        
        self.search_button = ttk.Button(button_frame, text="Find Matching Jobs", command=self.find_jobs, state=tk.DISABLED)
        self.search_button.pack(side=tk.LEFT)
        
        # Add job source selection
        source_frame = ttk.Frame(input_frame)
        source_frame.grid(row=1, column=1, sticky=tk.E)
        
        ttk.Label(source_frame, text="Source:").pack(side=tk.LEFT, padx=(0, 5))
        
        self.source_var = tk.StringVar(value="LinkedIn")
        sources = ttk.Combobox(source_frame, textvariable=self.source_var, values=["LinkedIn", "Indeed", "Both"], width=10, state="readonly")
        sources.pack(side=tk.LEFT)
        
        # File info
        self.file_info_var = tk.StringVar()
        ttk.Label(input_frame, textvariable=self.file_info_var, font=("Arial", 10, "italic")).grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        # Keywords frame
        keywords_frame = ttk.LabelFrame(main_frame, text="Detected Skills & Technologies", padding="10")
        keywords_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.keywords_var = tk.StringVar()
        ttk.Label(keywords_frame, textvariable=self.keywords_var, wraplength=850).pack(fill=tk.X)
        
        # Edit keywords
        edit_frame = ttk.Frame(keywords_frame)
        edit_frame.pack(fill=tk.X, pady=(5, 0))
        
        ttk.Label(edit_frame, text="Add/Edit Keywords:").pack(side=tk.LEFT, padx=(0, 5))
        self.keyword_entry = ttk.Entry(edit_frame, width=30)
        self.keyword_entry.pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(edit_frame, text="Add", command=self.add_keyword).pack(side=tk.LEFT)
        
        # Results frame
        results_frame = ttk.LabelFrame(main_frame, text="Job Matches", padding="10")
        results_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create canvas for scrolling
        self.canvas = tk.Canvas(results_frame)
        scrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=self.canvas.yview)
        
        self.results_container = ttk.Frame(self.canvas)
        self.results_container.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        
        self.canvas.create_window((0, 0), window=self.results_container, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress = ttk.Progressbar(main_frame, orient=tk.HORIZONTAL, variable=self.progress_var, mode='determinate')
        self.progress.pack(fill=tk.X, pady=(10, 0))
        
        # Status bar
        status_frame = ttk.Frame(main_frame)
        status_frame.pack(fill=tk.X, pady=(5, 0))
        
        ttk.Label(status_frame, text="© 2025 JobMatch AI").pack(side=tk.LEFT)
        self.job_count_var = tk.StringVar(value="No jobs found")
        ttk.Label(status_frame, textvariable=self.job_count_var).pack(side=tk.RIGHT)
    
    def upload_cv(self):
        path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if not path:
            return
            
        try:
            self.status_var.set("Extracting text from CV...")
            self.root.update()
            
            # Extract text in a separate thread to prevent UI freezing
            def extract_text():
                self.cv_text = self.extract_text_from_pdf(path)
                self.keywords = self.extract_tech_terms(self.cv_text)
                self.display_keywords()
                
                self.file_info_var.set(f"Loaded: {os.path.basename(path)}")
                self.search_button.config(state=tk.NORMAL)
                self.status_var.set("CV processed successfully")
            
            threading.Thread(target=extract_text).start()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to extract text from PDF: {str(e)}")
            self.status_var.set("Error processing CV")
    
    def extract_text_from_pdf(self, path):
        try:
            doc = fitz.open(path)
            text = "\n".join([page.get_text() for page in doc])
            doc.close()
            return text
        except Exception as e:
            raise Exception(f"PDF extraction error: {str(e)}")
    
    def extract_tech_terms(self, text):
        # Comprehensive list of technologies, frameworks, languages, etc.
        tech_pattern = r"\b(?:Angular|React|Vue\.js|Svelte|Next\.js|Gatsby|jQuery|D3\.js|" + \
                      r"Spring Boot|Django|Flask|Laravel|Ruby on Rails|ASP\.NET|Express|Symfony|FastAPI|" + \
                      r"Node\.js|Java|Python|C\+\+|C#|Ruby|PHP|Go|Rust|Swift|Kotlin|TypeScript|JavaScript|" + \
                      r"MongoDB|MySQL|PostgreSQL|Oracle|SQL Server|Redis|Cassandra|DynamoDB|" + \
                      r"Docker|Kubernetes|AWS|Azure|GCP|Terraform|Ansible|Jenkins|Git|" + \
                      r"TensorFlow|TensorFlow|PyTorch|Scikit-learn|Keras|Pandas|NumPy|Matplotlib|OpenCV|NLTK|SpaCy)\b"
        found = re.findall(tech_pattern, text, re.IGNORECASE)
        return sorted(set(map(str.title, found)))

    def display_keywords(self):
        self.keywords_var.set(", ".join(self.keywords))

    def add_keyword(self):
        new_kw = self.keyword_entry.get().strip()
        if new_kw and new_kw not in self.keywords:
            self.keywords.append(new_kw)
            self.display_keywords()
            self.keyword_entry.delete(0, tk.END)

    def find_jobs(self):
        if not self.keywords:
            messagebox.showwarning("No keywords", "Please upload a CV or add keywords.")
            return

        self.jobs.clear()
        self.status_var.set("Searching for jobs...")
        self.progress_var.set(0)
        self.job_count_var.set("Searching...")

        def search():
            sources = self.source_var.get()
            max_jobs = self.scraper_options["max_jobs_per_keyword"]
            locations = self.scraper_options["locations"]
            total_keywords = len(self.keywords)
            count = 0

            for kw in self.keywords:
                for loc in locations:
                    jobs = []
                    if sources in ["LinkedIn", "Both"]:
                        jobs += self.linkedin_scraper.search_jobs(kw, location=loc, max_jobs=max_jobs)
                    if sources in ["Indeed", "Both"]:
                        jobs += self.indeed_scraper.search_jobs(kw, location=loc, max_jobs=max_jobs)
                    self.jobs.extend(jobs)

                count += 1
                self.progress_var.set((count / total_keywords) * 100)
                self.root.update_idletasks()

            self.display_results()
            self.status_var.set("Search complete")
            self.job_count_var.set(f"Found {len(self.jobs)} jobs")

        threading.Thread(target=search).start()

    def display_results(self):
        for widget in self.results_container.winfo_children():
            widget.destroy()

        for job in self.jobs:
            frame = ttk.Frame(self.results_container, relief=tk.RIDGE, padding=5)
            frame.pack(fill=tk.X, pady=2)

            title = ttk.Label(frame, text=job['title'], font=('Arial', 12, 'bold'), foreground='blue', cursor='hand2')
            title.pack(anchor=tk.W)
            title.bind("<Button-1>", lambda e, url=job['url']: webbrowser.open(url))

            ttk.Label(frame, text=f"{job['company']} - {job['location']}").pack(anchor=tk.W)
            ttk.Label(frame, text=f"Posted: {job['date_posted']}").pack(anchor=tk.W)

    def save_results(self):
        if not self.jobs:
            messagebox.showwarning("No data", "No job results to save.")
            return

        path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])
        if path:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(self.jobs, f, indent=2)
            messagebox.showinfo("Saved", f"Results saved to {path}")

    def show_about(self):
        messagebox.showinfo("About", "JobMatch AI Agent\nCreated in 2025 for job matching using CV parsing and scraping.")

    def show_preferences(self):
        messagebox.showinfo("Preferences", "Preferences are not implemented yet.")

    def clear_all(self):
        self.cv_text = ""
        self.keywords = []
        self.jobs = []
        self.keywords_var.set("")
        self.job_count_var.set("No jobs found")
        self.file_info_var.set("")
        self.progress_var.set(0)
        for widget in self.results_container.winfo_children():
            widget.destroy()

    def load_config(self):
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r", encoding="utf-8") as f:
                    config = json.load(f)
                self.scraper_options.update(config.get("scraper_options", {}))
            except:
                pass

# To run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = JobMatchAgent(root)
    root.mainloop()
