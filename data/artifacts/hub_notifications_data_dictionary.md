# Data Dictionary

## Source System: Analytics hub

## Table Name: hub_notifications

## Description of Data: 

This table contains comprehensive notification tracking information for tiles containing 18 columns and 108 rows. It captures notification events and their associated metadata. Each record represents a unique notification instance sent to tiles, including both the content (title and description) and the complete audit trail of creation and modification events.

## Data Details:

The dataset spans approximately 18 months, covering notifications from June 27, 2023, to December 24, 2024. The data maintains a complete audit trail for each notification, tracking both the original creation and any subsequent updates, including:
- Creation metadata (timestamp and user information)
- Modification history (when applicable, including who made the changes)
- Notification content (titles and descriptions)
- Tile targeting information

##  Data Object Properties (Columns)

| Column Name    | Data Type | Description                                     | Constraints          |
|----------------|-----------|-------------------------------------------------|----------------------|
| id             | string    | Unique identifier for each notification         | Primary Key, Not Null|
| title          | string    | Title of notification                           | Not Null             |
| description    | string    | Detailed description of the notification        | Not Null             |
| type           | string    | Type of notification                            | Nullable             |
| classification | string    | Classification of notification                  | Nullable             |
| tile           | string    | Associated tile(s) to the notification          |                      |
| role           | string    | Role associated with the notification           |                      |
| start          | integer   | Start timestamp of the notification             | Not Null             |
| end            | integer   | End timestamp of the notification               | Not Null             |
| created_date   | integer   | Creation timestamp of notification              | Not Null             |
| updated_date   | integer   | Timestamp of notification update                |                      |
| created_by     | string    | Name of user that created the notification      | Nullable             |
| _rid           | string    | System generated identifier                     | Not Null             |
| _self          | string    | System generated reference URL                  | Not Null             |
| _etag          | string    | System generated entity tag                     | Not Null             |
| _attachments   | string    | System generated attachment storage             |                      |
| _ts            | integer   | System generated timestamp                      | Not Null             |
| updated_by     | string    | Name of user that modified the notification     | Nullable             |


## Metadata 
- Created By: Isha Srivastava
- Created On: 2025/02/04  
- Email/Contact Info: isrivastava4@wisc.edu

## Version History
| Version | Date       | Description                |
|---------|------------|----------------------------|
| 1.0     | 2025/02/04 | Initial draft created      |
