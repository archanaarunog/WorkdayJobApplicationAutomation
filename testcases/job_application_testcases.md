# Job Application Portal Test Cases

> Note: Negative scenarios and corner test cases are included in the table below for reference.

| Test Case ID | Feature                | Test Step Description                                 | Input Data                        | Expected Result                        | Actual Result | Status |
|--------------|-----------------------|------------------------------------------------------|------------------------------------|-----------------------------------------|---------------|--------|
| TC-001       | User Registration     | Register with valid details                          | Valid email, password, name, phone | User registered, success response      |               |        |
| TC-002       | User Registration     | Register with duplicate email                        | Existing email                     | 400 error, 'Email already registered'  |               |        |
| TC-003       | User Login            | Login with valid credentials                         | Registered email, password         | JWT token returned                     |               |        |
| TC-004       | Job Listing           | Fetch all jobs                                       | -                                  | List of jobs returned                  |               |        |
| TC-005       | Job Application       | Apply to a job as logged-in user                     | Job ID, JWT token                  | Application created, success response  |               |        |
| TC-006       | Application History   | Fetch applications for logged-in user                | JWT token                          | List of user's applications            |               |        |
| TC-007       | Job Application       | Apply to same job twice                              | Same Job ID, JWT token             | 400 error, 'Already applied'           |               |        |
| TC-008       | User Registration     | Register with invalid email format                   | Invalid email, valid other fields  | 422 error, validation failed           |               |        |
| TC-009       | User Login            | Login with incorrect password                        | Registered email, wrong password   | 401 error, Unauthorized                |               |        |
| TC-010       | Job Application       | Apply to a job without authentication                | Job ID, no JWT token               | 401 error, Unauthorized                |               |        |
| TC-011       | User Registration     | Register with maximum allowed field lengths          | Max length email, name, phone      | User registered, success response      |               |        |
| TC-012       | Job Application       | Apply to a job when there are no jobs listed         | Job ID (none exist), JWT token     | 404 error or appropriate error         |               |        |

> Add more test cases as features are implemented.
