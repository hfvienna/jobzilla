// app/ranking/page.js

'use client';

import { useState, useEffect } from 'react';
import 'daisyui/dist/full.css';

// Import job_table.json
import tableData from '../job_table.json';

// Log imported data
console.log('Imported data:', tableData); 

export default function JobsTable() {

  const [jobs, setJobs] = useState(tableData);

  useEffect(() => {
    console.log('Component mounted');
  }, []);

  return (

      <div className="overflow-x-auto">
        <table className="table table-zebra w-full">
          <thead>
            <tr>
              <th>Company</th> 
              <th>Job Title</th>
              <th>Company Applicant Fit</th>
              <th>Date Added</th>
              <th>Salary Range</th>
              <th>Location</th>
            </tr>
          </thead>

          <tbody>
          {jobs.map((job, index) => (
            <tr key={index}>
              <td>{job.company || '-'}</td>
              <td>{job.title || '-'}</td>
              <td>{job.fit || '-'}</td>
              <td>{job.dateAdded || '-'}</td>
              <td>{job.salaryRange || '-'}</td>
              <td>{job.location || '-'}</td>
            </tr>
          ))}
          </tbody>


          <tfoot>
            <tr>
              <th></th>
              <th>Company</th>
              <th>Job Title</th>
              <th>Company Applicant Fit</th>
              <th>Date Added</th>
              <th>Salary Range</th>
              <th>Location</th>
            </tr>
          </tfoot>
        </table>
      </div>

  );
}
