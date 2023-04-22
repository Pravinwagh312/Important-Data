import { HttpClient, HttpHeaders } from '@angular/common/http';

// Set the authentication header with your GitHub personal access token
const headers = new HttpHeaders({
  Authorization: `Bearer ${your_github_token}`,
});

// Calculate the date range for the search query
const fromDate = new Date(Date.now() - 7 * 24 * 60 * 60 * 1000); // 7 days ago
const toDate = new Date(Date.now()); // today's date

// Construct the search query to search for workflow runs within the date range
const query = `is:completed updated:${fromDate.toISOString()}..${toDate.toISOString()}`;

// Make a GET request to the GitHub API's "Search for workflow runs" endpoint
this.http.get('https://api.github.com/search/actions', {
  headers, // Pass the authentication header to the request
  params: {
    q: query, // Pass the search query to the request parameters
    per_page: '100', // Set the page size to reduce the number of requests
  },
}).subscribe((response) => {
  // Extract the necessary KPI parameters from the API response
  const totalExecuted = response.total_count;
  const successfulWorkflow = response.items.filter((item) => item.conclusion === 'success').length;
  const failedWorkflow = response.items.filter((item) => item.conclusion === 'failure').length;
  const abortedWorkflow = response.items.filter((item) => item.conclusion === 'cancelled').length;

  // Create an object containing the KPI parameters
  const kpiParams = {
    totalExecuted,
    successfulWorkflow,
    failedWorkflow,
    abortedWorkflow,
  };

  // Send the KPI parameters to Kafka or any other destination
});
