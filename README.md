# AI Resume Screening System

## Overview

The AI Resume Screening System is designed to simplify the hiring process by automatically reviewing and evaluating resumes. Using advanced algorithms, the system analyzes resumes for key information such as skills, experience, and qualifications, and compares them to job requirements. This allows recruiters to quickly identify the most suitable candidates, streamlining the hiring process while ensuring a fair and unbiased evaluation.

## Features-

- **Upload and Process Resumes**: Supports PDF format.
- **Analyze Job Descriptions**: Compare job descriptions with resumes.
- **Extract Key Roles**: Identify key roles and average years of experience from resumes.
- **Calculate Similarity Scores**: Determine the match rate between job descriptions and resumes.
- **Display Analytics**: Show total resumes processed, average experience, match rate, and job categories.

## Project Structure

- `index.html`: The frontend user interface for uploading resumes and job descriptions.
- `login.html`: The frontend user interface for user login and signup.
- `app.py`: The backend server that handles file uploads and processes resumes done by Flask web framework.
- `style.css`: The stylesheet for the frontend user interface.
- `uploads/`: Directory for storing uploaded resumes temporarily.

## Usage

1. **Upload Job Description:**

   - Paste the job description in the provided textarea.

2. **Upload Resume:**

   - Click the "Upload your resume" button and select a resume file in PDF format.

3. **View Analytics:**

   - After uploading, view the extracted key roles, average experience, match rate, and job category.

4. **Login and Signup:**
   - Use the `login.html` page to log in or sign up for an account.

## Example

1. **Upload Job Description:**
   ![Job Description](screenshots/job_description.png)

2. **Upload Resume:**
   ![Upload Resume](screenshots/upload_resume.png)

3. **View Analytics:**
   ![View Analytics](screenshots/view_analytics.png)

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## NLP model details
