# Online Crime Reporting System

A web application built with Django designed to streamline how users report crimes, submit evidence, and track case status—all without visiting a police station.

## About

This project enables users to file crime reports online—complete with options to submit evidence, track updates, and report anonymously if desired. It aims to bridge the gap between the public and law enforcement for faster, more accessible complaint logging

---

## Features

- **User Registration & Login** – Provides secure access for public users and admin roles.  
- **Crime & Missing Person Reporting** – Submit complaints with optional attachments such as photos or videos :contentReference[oaicite:1]{index=1}.  
- **Anonymous Tips & Alerts** – Report without revealing your identity; receive status updates on cases :contentReference[oaicite:2]{index=2}.  
- **Admin Dashboard** – Police personnel or administrators can view reports, update statuses, and manage data.  
- **Searchable Database** – Efficient retrieval of complaints, case history, and user reports.  
- **Awareness Features** – Share information on issues like women's safety, cybercrime awareness, or missing persons :contentReference[oaicite:3]{index=3}.

---

## Tech Stack

- **Backend**: Python with Django framework  
- **Database**: SQLite (default in Django setups; customizable to PostgreSQL or MySQL)  
- **Frontend**: HTML, CSS, JavaScript (Django templates)  
- **Dependencies**: Captured in `requirements.txt`

---

## Getting Started

### Prerequisites

- Python 3.x  
- pip package manager  
- (Optional but recommended) Virtual environment tool like `venv`

### Installation

```bash
git clone https://github.com/httpMeet/Online-Crime-Reporting-System.git
cd Online-Crime-Reporting-System
python3 -m venv venv
source venv/bin/activate     # On Windows: venv\Scripts\activate
pip install -r requirements.txt

