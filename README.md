# 🦖Jobzilla v0.1.0

Jobzilla stomps onto the job search scene, ferociously sniffing out opportunities like a wild beast on the hunt, aggressively tracking down opportunities and crushing its competition with its monstrous AI might.

Jobzilla is a revolutionary AI-powered job hunting tool designed to automate and simplify the job search process in the modern era.

# Features
1. Personalized Job Ranking: Our app grades job offers using an LLM based on user-specific preferences, providing a tailored ranking of job opportunities. Users can customize their search criteria, including job location, work hours, industry, and company size.
2. Auto Job Application: If a job offer meets a certain user-defined threshold, Jobzilla applies on their behalf using the user's resume. This eliminates the need for manual job applications.
3. Not yet implemented: Automatic daily scraping of job plattforms.

# Architecture

![Jobzilla](https://github.com/hfvienna/jobzilla/assets/130350299/86e106bf-83cd-41f2-8972-e55e1de6bfad)

Jobs are initially manually collected from company career pages and job platforms. As there is no additional effort once the job is added to the app, every remotely interesting job is added. After the MVP is completed am automatic scraping will be built. Job descriptions are then stored. From hfvienna's Human Digital Twin (simplified a large data collection about hfvienna) the job requirements and their weighing for the job hunter are automatically determined and stored as well. If you adapt this code for your job hunt, you can just edit the job_requirements_and_weighing.txt file. Both are then merged in a prompt and sent to an LLM (Claude 2) which returns a Grade job-applicant-fit and returns it. A loop through all job offers then results in a job ranking list. This ranking list is sent to the Next.js. For frontend design, TailwindCSS and DaisyUI is used and React is by default in a Next.js app.

A threshold is set in the ranking list, e. g. apply to every job with a ranking percentage above 70%. As with sought out jobs a typical likelyhood of getting the job is 1-3 % and thus is a numbers game it is a good idea to apply to a high doubly digit number of jobs.

Using the original scraped job description, and the CV, an application letter if written. If the company values AI and coding experience (otherwise one might consider not to apply at all ;) ), a link to this github repository with an explaining sentence is added. The email is then sent out.

# Todos
1. Reduce hallucinations when writing the applications by replacing Claude 2 with GPT-4. First tests have shown that for this task, GPT-4 performs decicivly better, more than there 50 ELO difference would have one expect.
2. Add key applied (boolean) to JSON to separate job postings for which an application has already been sent out
3. Update README, add templates, and requirements.txt to enable third parties a quick start
4. Implement automatic scraping
5. Add LLAMA2 for "easy" tasks as POC

# Getting Started (currently next.js boilerplate)

First, run the development server:

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

You can start editing the page by modifying `app/page.js`. The page auto-updates as you edit the file.
