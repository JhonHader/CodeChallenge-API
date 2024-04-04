# CodeChallenge-API

**SECTION 1**

The proposed solution is shown in Solution.pdf file, architecture is based in AWS services.

API endpoint: **https://uj0k9ljpqh.execute-api.us-east-2.amazonaws.com/dev/**

Endpoints:
  - "/" (GET): Home
  - "/status" (GET) : Check API status
  - "/hired_employees" (GET): Retrieve all records from hired_employee table in AWS RDS Postgre DB.
  - "/jobs" (GET): Retrieve all records from job table in AWS RDS Postgre DB.
  - "/departments" (GET): Retrieve all records from departments table in AWS RDS Postgre DB.
  - "/upload/hired_employee" (POST): Load csv file (must have headers in first line) to s3 bucket and insert those records to hired_employee table in AWS RDS Postgre DB.
  - "/upload/job" (POST): Load csv file (must have headers in first line) to s3 bucket and insert those records to job table in AWS RDS Postgre DB.
  - "/upload/department" (POST): Load csv file (must have headers in first line) to s3 bucket and insert those records to department table in AWS RDS Postgre DB.

Use:
  Refers to Use Example.pdf to see use demo request with postman.
  Take in consideration when make a post, load file in the body as binary.

  Example: https://uj0k9ljpqh.execute-api.us-east-2.amazonaws.com/dev/jobs
  Retrieve SELECT * FROM job; SQL sentence.
