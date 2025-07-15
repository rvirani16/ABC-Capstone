# Data Dictionary

## Source System: []

## Table Name: associate_export

## Description of Data: 

This dataset, comprising 22,000 rows, contains Active Directory information for employees within the organization. It includes essential columns such as title, capstone_name, capstone_email, capstone_employee_id, capstone_ad_account, and manager_capstone_employee_id. This data maintains employee roles, contact information, and the organizational structure. 

## Data Details:

Data is assumed to be updated whenever a new employee joins the company and an entry is removed when they leave the company.

##  Data Object Properties (Columns)

| Column Name                 | Data Type | Description                                              | Constraints          |
|-----------------------------|-----------|----------------------------------------------------------|----------------------|
|title                        | String    |The job title of the employee                             | Nullable             |
|capstone_name                | String    |Name of the employee                                      | Not Null             |
|capstone_email               | String    |Email address of the employee                             | Not Null             |
|capstone_employee_id         | Int       |Employee ID of the employee (unique)                      | Not Null             |
|capstone_ad_account          | String    |Active Directory account ID associated with the employee  | Not Null (PK)        |
|manager_capstone_employee_id | Int       |The employee ID of the employee's direct manager          | Nullable             |


## Metadata 
- Created By: Leena 
- Created On: 2025/02/04
- Email/Contact Info: leena@wisc.edu

## Version History
| Version | Date       | Description                |
|---------|------------|----------------------------|
| 1.0     | 2025/02/04 | Initial draft created      |