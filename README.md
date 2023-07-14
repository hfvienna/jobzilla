# Jobzilla

Jobzilla stomps onto the job search scene, ferociously sniffing out opportunities like a wild beast on the hunt, aggressively tracking down opportunities and crushing its competition with its monstrous AI might.

Jobzilla is a revolutionary AI-powered job hunting tool designed to automate and simplify the job search process in the modern era.

## Features
1. Personalized Job Ranking: Our app grades job offers using an LLM based on user-specific preferences, providing a tailored ranking of job opportunities. Users can customize their search criteria, including job location, work hours, industry, and company size.
2. Auto Job Application: If a job offer meets a certain user-defined threshold, Jobzilla applies on their behalf using the user's resume. This eliminates the need for manual job applications.
3. Not yet implemented: Automatic daily scraping of job plattforms.

# Architecture

![Jobzilla](https://github.com/hfvienna/jobzilla/assets/130350299/ee3d9394-12dd-48d0-82cb-ff75bfb45851)

Jobs are initially manually collected from company career pages and job platforms. As there is no additional effort once the job is added to the app, every remotely interesting job is added. After the MVP is completed am automatic scraping will be built. Job descriptions are then stored. From hfvienna's Human Digital Twin (simplified a large data collection about hfvienna) the job requirements and their weighing for the job hunter are automatically determined and stored as well. If you adapt this code for your job hunt, you can just edit the job_requirements_and_weighing.txt file. Both are then merged in a prompt and sent to an LLM (Claude 2) which returns a Grade job-applicant-fit and returns it. A loop through all job offers then results in a job ranking list. This ranking list is sent to the Next.js view via Flask. For frontend design, TailwindCSS and DaisyUI is used and React is by default in a Next.js app.

A threshold is set in the ranking list, e. g. apply to every job with a ranking percentage above 70%. As with sought out jobs a typical likelyhood of getting the job is 1-3 % and thus is a numbers game it is a good idea to apply to a high doubly digit number of jobs.

Using the original scraped job description, and the CV, an application letter if written. If the company values AI and coding experience (otherwise one might consider not to apply at all ;) ), a link to this github repository with an explaining sentence is added. The email is then sent out.

# tree -L 2

.  
├── README.md  
├── api  
│   ├── __pycache__  
│   └── index.py  
├── app  
│   ├── favicon.ico  
│   ├── globals.css  
│   ├── layout.js  
│   ├── page.js  
│   └── ranking  
├── craco.config.js  
├── jsconfig.json  
├── next.config.js  
├── node_modules  

If you copy and paste the tree into an environment that uses a monospace font (like most code editors or terminals), the vertical lines (│) align correctly. If you're seeing misalignment this is due to GitHub's markdown renderer.

## Next.js






This is a [Next.js](https://nextjs.org/) project bootstrapped with [`create-next-app`](https://github.com/vercel/next.js/tree/canary/packages/create-next-app).

## Getting Started

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

This project uses [`next/font`](https://nextjs.org/docs/basic-features/font-optimization) to automatically optimize and load Inter, a custom Google Font.

## Learn More

To learn more about Next.js, take a look at the following resources:

- [Next.js Documentation](https://nextjs.org/docs) - learn about Next.js features and API.
- [Learn Next.js](https://nextjs.org/learn) - an interactive Next.js tutorial.

You can check out [the Next.js GitHub repository](https://github.com/vercel/next.js/) - your feedback and contributions are welcome!

## Deploy on Vercel

The easiest way to deploy your Next.js app is to use the [Vercel Platform](https://vercel.com/new?utm_medium=default-template&filter=next.js&utm_source=create-next-app&utm_campaign=create-next-app-readme) from the creators of Next.js.

Check out our [Next.js deployment documentation](https://nextjs.org/docs/deployment) for more details.
