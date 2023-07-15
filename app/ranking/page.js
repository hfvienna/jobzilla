"use client";

import { useState, useEffect } from "react";
import "daisyui/dist/full.css";

// Import job_table.json
import tableData from "../job_table.json";

// Define fallback value
const DEFAULT_VALUE = "-";

export default function JobsTable() {
  const [jobs] = useState(tableData);

  useEffect(() => {}, []);

  return (
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
        {jobs.map((job) => (
          <tr key={job.id}>
            <td>{job.company || DEFAULT_VALUE}</td>
            <td>{job.title || DEFAULT_VALUE}</td>
            <td>{job.fit || DEFAULT_VALUE}</td>
            <td>{job.dateAdded || DEFAULT_VALUE}</td>
            <td>{job.salaryRange || DEFAULT_VALUE}</td>
            <td>{job.location || DEFAULT_VALUE}</td>
          </tr>
        ))}
      </tbody>

      <tfoot>
        <tr>
          <th>Company</th>
          <th>Job Title</th>
          <th>Company Applicant Fit</th>
          <th>Date Added</th>
          <th>Salary Range</th>
          <th>Location</th>
        </tr>
      </tfoot>
    </table>
  );
}
