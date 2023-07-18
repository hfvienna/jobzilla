"use client";
import { useState, useEffect } from "react";
import "daisyui/dist/full.css";

// Import job_table.json
import tableData from "../job_table.json";

// Define fallback value
const DEFAULT_VALUE = "-";

// Truncate text to maximum length
const truncate = (text, maxLength) => {
  if (text.length > maxLength) {
    return text.substring(0, maxLength) + '...';
  }
  return text;
}

export default function JobsTable() {
  const [jobs] = useState(tableData);

  useEffect(() => {}, []);

  return (
    <table className="table table-zebra">
      <thead>
        <tr>
          <th>UUID</th>
          <th>Company</th>
          <th>Job Title</th>
          <th>Fit Total</th>
          <th>Fit Recruiter View</th>
          <th>Fit Recruiter View Detailed</th>
          <th>Fit Applicant View</th>
          <th>Fit Applicant View Detailed</th>
          <th>Date Added</th>
          <th>Salary Range</th>
          <th>Location</th>
        </tr>
      </thead>
      <tbody>
        {jobs.map((job, index) => (
          <tr key={job.id}>
            <td>{index + 1}</td>
            <td>{job.company || DEFAULT_VALUE}</td>
            <td>{job.title || DEFAULT_VALUE}</td>
            <td>{(job.fit_recruiter + job.fit_applicant) || DEFAULT_VALUE}</td>
            <td>{job.fit_recruiter || DEFAULT_VALUE}</td>
            <td>{truncate(job.fit_recruiter_detailed, 200) || DEFAULT_VALUE}</td>
            <td>{job.fit_applicant || DEFAULT_VALUE}</td>
            <td>{truncate(job.fit_applicant_detailed, 200) || DEFAULT_VALUE}</td>
            <td>{job.date_added || DEFAULT_VALUE}</td>
            <td>{job.salary_range || DEFAULT_VALUE}</td>
            <td>{job.location || DEFAULT_VALUE}</td>
          </tr>
        ))}
      </tbody>
      <tfoot>
        <tr>
          <th>UUID</th>
          <th>Company</th>
          <th>Job Title</th>
          <th>Fit Total</th>
          <th>Fit Recruiter View</th>
          <th>Fit Recruiter View Detailed</th>
          <th>Fit Applicant View</th>
          <th>Fit Applicant View Detailed</th>
          <th>Date Added</th>
          <th>Salary Range</th>
          <th>Location</th>
        </tr>
      </tfoot>
    </table>
  );
}
