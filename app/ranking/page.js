// Import Table and other components
import 'daisyui/dist/full.css';

export default function JobsTable() {

  return (
    <div className="overflow-x-auto">
      <table className="table">
        <thead>
          <tr>
            <th></th>
            <th>Company</th> 
            <th>Job Title</th>
            <th>Company-Applicant Fit</th>
            <th>Date Added</th>
            <th>Salary Range</th>
            <th>Location</th>
          </tr>
        </thead>

        <tbody>
          <tr>
            <th>
              <label>  
                <input type="checkbox" className="checkbox" />
              </label>
            </th>
            <td>Anthropic</td>
            <td>Software Engineer</td>
            <td>4/5</td>
            <td>July 10, 2023</td>
            <td>$120k - $150k</td>
            <td>Remote</td>
          </tr>
          
          <tr>
            <th>
              <label>
                <input type="checkbox" className="checkbox" />
              </label>  
            </th>
            <td>Google</td>
            <td>Product Manager</td>
            <td>3/5</td>
            <td>July 12, 2023</td>
            <td>$150k - $180k</td>
            <td>Mountain View, CA</td>
          </tr>
          
          <tr>
            <th>
              <label>
                <input type="checkbox" className="checkbox" />
              </label>
            </th>
            <td>Microsoft</td>
            <td>Software Engineer</td>
            <td>5/5</td> 
            <td>July 14, 2023</td>
            <td>$130k - $160k</td>
            <td>Redmond, WA</td>
          </tr>
        </tbody>

        <tfoot>
          <tr>
            <th></th>
            <th>Company</th>
            <th>Job Title</th>
            <th>Company-Applicant Fit</th>
            <th>Date Added</th>
            <th>Salary Range</th>
            <th>Location</th>
          </tr>
        </tfoot>
      </table>
    </div>
  )

}