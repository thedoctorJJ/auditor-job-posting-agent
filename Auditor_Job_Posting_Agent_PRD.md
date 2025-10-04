# Product Requirements Document (PRD)  
## Auditor Job Posting Agent  

---

### Step 1: Cursor Agent Setup Instructions  

This PRD is designed to be consumed by the **Cursor Agent in Agent Mode**. The Cursor Agent must behave as an **autonomous Senior Software Engineer**.  

**Initial Setup**  
1. Save this file in the project root directory with the name:  
   **`Auditor_Job_Posting_Agent_PRD.md`**  

2. Open Cursor Chat/Composer in **Agent Mode** (high autonomy recommended).  

3. Run the following prompt in Cursor:  

```
You are an autonomous Senior Software Engineer. Your task is to build the complete application from scratch based exclusively on the requirements detailed in the @Auditor_Job_Posting_Agent_PRD.md file.

PHASE 1: Planning (STOP AFTER THIS PHASE)
1. Analyze the @Auditor_Job_Posting_Agent_PRD.md file thoroughly, paying close attention to the Tech Stack and Key Features.
2. Generate a detailed, step-by-step Technical Implementation Plan in a new file called Auditor_Job_Posting_Agent_PLAN.md. This plan must break the PRD into 5–10 logical, implementable engineering tasks (for example: "Set up project structure and routing," "Implement database schema in Supabase," "Develop Outreach Review Dashboard component with placeholder data").
3. DO NOT start coding yet. Present the Auditor_Job_Posting_Agent_PLAN.md file to me for review and approval.
```  

Only after the PLAN file is approved should coding begin (see Step 2 at the end of this PRD).  

---

### 1. Vision and Background  

The Auditor Job Posting Agent is an AI-powered application that continuously scans job boards for auditing and accounting job postings, extracts structured information, and analyzes which roles are best suited for automation by AI workforce agents.  

Job postings are a direct reflection of market demand. They reveal what skills firms are seeking, how much they are willing to pay, and which responsibilities are repeated across multiple postings. This agent will systematically collect and analyze postings to:  

- Validate demand for roles that Tellen's current agents can automate.  
- Highlight new opportunities where additional agents could be developed.  
- Directly generate business development opportunities by reaching out to firms that are hiring for automatable roles.  

This project is both a **research tool** and a **business development tool**. On the research side, it creates a living dataset of market needs. On the BD side, it drafts and sends outreach emails to firms, offering Tellen as a solution at a fraction of the cost of traditional hiring.  

---

### 2. Objectives  

1. **Automated Collection of Job Listings**  
   The system must gather job postings daily from sites like Indeed, LinkedIn, and Glassdoor, starting with Indeed. Postings with salary details will be prioritized.  

2. **Structured Data Extraction**  
   Raw text must be normalized into fields: job title, employer, location, salary range, description, responsibilities, posting date, and URL.  

3. **Agent Mapping**  
   Each posting is analyzed against a library of tasks Tellen agents perform. Matches (e.g., AFC or FSP) are logged with confidence scores. Jobs outside scope are flagged as "other," with notes suggesting potential new agent concepts.  

4. **Ranking and Prioritization**  
   Postings are ranked by salary level, number of similar postings, and automation feasibility (based on repetitive, structured tasks).  

5. **Outreach Workflow**  
   The system generates personalized outreach drafts offering to do the role at **20% of the listed salary with the first month free**. Messages are stored for review.  

6. **Human-in-the-Loop Approval**  
   No outreach is sent automatically. JJ (or approver) must review and explicitly approve each draft via the Outreach Review Dashboard before it is sent.  

---

### 3. Stakeholders  

- **Product Owner**: JJ (requirements, validation, approvals).  
- **Engineering Execution**: Cursor agent, using OpenAI GPT-5-Codex to generate code, tests, and docs.  
- **End Users**: Tellen internal teams for strategy and sales, accounting firms as recipients of outreach.  

---

### 4. Functional Requirements  

#### 4.1 Job Scraping  
- Scrape postings daily, beginning with Indeed.  
- Extract structured fields from HTML.  
- Implement retry logic if pages fail to load.  

#### 4.2 Data Storage  
Supabase Postgres database with at least three tables:  
- **Jobs**: id, title, company, location, salary_min, salary_max, description, url, source, date_posted.  
- **AgentMatch**: job_id, matched_agent, confidence_score, notes.  
- **Outreach**: job_id, draft_email, status (draft, sent, rejected), timestamp, firm_contact.  

#### 4.3 Agent Matching Logic  
- Match tasks in job descriptions to agents like AFC and FSP.  
- Assign confidence scores (0–1).  
- If no match, mark as "other" and auto-generate notes describing gaps.  

#### 4.4 Ranking and Analysis  
Jobs ranked on:  
1. **Salary** (normalized to annual basis).  
2. **Volume** (frequency of similar postings).  
3. **Automation Feasibility** (repetitive vs advisory).  

#### 4.5 Outreach Drafting  
- Draft emails tailored to each job posting.  
- Emails must explicitly:  
  - Mention the job title and firm.  
  - Explain how Tellen automates those tasks.  
  - Offer Tellen at **20% of the listed salary** with **first month free**.  
  - Include JJ's Calendly link:  
    [https://calendly.com/jasonjones/30min-video-chat-with-tellen](https://calendly.com/jasonjones/30min-video-chat-with-tellen).  

#### 4.6 Outreach Review Dashboard  

**Purpose**  
The Outreach Review Dashboard is the interface where JJ reviews and approves outreach drafts before they are sent. It must be built in **Next.js** with **Tailwind CSS** and **shadcn/ui components**.  

**Layout**  
- **Left Panel (Job List)**  
  - Table of pending postings.  
  - Columns: Job Title, Company, Location, Salary, Posting Date.  
  - Sortable and filterable.  

- **Right Panel (Detail View)**  
  - **Job Snapshot**: Key fields with link to original posting.  
  - **System Explanation**:  
    - Why this posting is a good opportunity.  
    - Which agent(s) map to it and how.  
  - **Draft Outreach Email**: Editable email body shown in a textarea.  
  - **Controls**:  
    - Approve and Send.  
    - Reject.  
    - Edit & Send (after inline modifications).  

**Approval Workflow**  
- Outreach drafts are stored as "Draft."  
- JJ reviews and approves. Only then is email sent.  
- Sent and rejected statuses are logged with timestamps.  
- The system may propose follow-ups later, also requiring approval.  

**Design Guidance**  
- Use `Card`, `Table`, `Textarea`, and `Button` from shadcn/ui.  
- Tailwind utilities for responsiveness and spacing.  
- Optimized for fast scanning of multiple postings.  

---

### 5. Technical Architecture  

- **Scraper**: Python with BeautifulSoup and Selenium.  
- **Parser**: Regex + GPT-powered classification.  
- **Database**: Supabase Postgres.  
- **Backend**: FastAPI exposing endpoints for scrape, query, outreach.  
- **Frontend**: Next.js + Tailwind + shadcn/ui dashboard.  
- **Hosting**: Google Cloud (Functions + VM).  
- **AI Layer**: GPT-5-Codex for classification, matching, and drafting.  

---

### 6. Development Methodology  

- Modular development in Cursor, with OpenAI acting as AI engineer.  
- Modules: scraper, parser, matcher, database connector, outreach generator, API, frontend dashboard.  
- Each module developed, tested, and documented in sequence.  
- GitHub repo as the single source of truth.  

---

### 7. Success Metrics  

- ≥500 postings ingested per week.  
- ≥80% parsing accuracy.  
- ≥70% correct agent match validation.  
- ≥20 approved outreach emails sent per month.  
- ≥3 new potential agent ideas surfaced per quarter.  

---

### 8. Next Steps  

1. Scaffold GitHub repo with backend, frontend, infra, docs directories.  
2. Build Indeed scraper and store data in Supabase.  
3. Implement matching and ranking.  
4. Generate outreach drafts with salary discount + free month offer.  
5. Build Outreach Review Dashboard UI in Next.js/shadcn.  
6. Connect approvals to outbound email system.  
7. Deploy via Google Cloud.  
8. Run validation and iterate.  

---

### Step 2: Execution Instructions (for Cursor Agent)  

Once the `Auditor_Job_Posting_Agent_PLAN.md` file has been created and approved, issue the following prompt in Cursor Agent Mode:  

```
I have reviewed and approved the `Auditor_Job_Posting_Agent_PLAN.md`.

Now, autonomously execute all the tasks listed in `Auditor_Job_Posting_Agent_PLAN.md` sequentially. Follow the plan and all constraints in the @Auditor_Job_Posting_Agent_PRD.md file strictly.
1. Run all necessary installation and setup commands in the integrated terminal.
2. Write all required code (frontend, backend, database).
3. Run unit tests and perform self-debugging after implementing each major task.
4. Keep me updated on your progress after completing each main step in the `Auditor_Job_Posting_Agent_PLAN.md`.
```  
