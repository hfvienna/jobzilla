'use client'

import { useState, useEffect } from 'react';
import 'daisyui/dist/full.css';
import axios from 'axios';

export default function JobsTable() {
  const [jobs, setJobs] = useState([]);

  useEffect(() => {
    async function fetchData() {
      // Fetch data from your JSON file
      const response = await fetch('/table2.json');
      const data = await response.json();
      
      console.log(data);  // Log the data here
      
      // Set the state
      setJobs(data);
    }
    fetchData();
  }, []);

  return (
    <div className="overflow-x-auto">
      <table className="table">
        <thead>
          <tr>
            <th></th>
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
            <th>
              <label>  
                <input type="checkbox" className="checkbox" />
              </label>
            </th>
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
