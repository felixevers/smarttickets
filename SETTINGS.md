# Settings

## available settings

| Keys                      | Description                                         |
| ------------------------- |-----------------------------------------------------|
| title                     | system-name like ticket-system                      |
| imprint                   | imprint in the frontend                             |
| order1                    | text displayed at in step one of an order           |
| order2                    | text displayed at in step two of an order           |
| order3                    | text displayed at in step three of an order         |
| customer_mail_title       | title of the mail if a customer was created         |
| customer_mail_content     | content of the mail if a customer was created       |
| ticket_mail_title         | title of the mail when a ticket has been paid       |
| ticket_mail_content       | content of the mail when a ticket has been paid     |
| buy_mail_title            | title of the mail if a customer reserved a ticket   |
| buy_mail_content          | content of the mail if a customer reserved a ticket |
| intro                     | text displayed on the start page                    |
| banner                    | main image (base64)                                 |
| mail_cc                   | mail as cc                                          |
| question_mail             | mail for questions                                  |
| question_mail_subject     | subject of mail for questions                       |
| ticket_img                | the image that is displayed on the ticket (base64)  |
| inc                       | html include on each site                           |

## mail variables

The mail variables can be used in the setting value like this:
`{{variable}}`  

The variables are supported:  

| Variables                 | Description                                      |
| ------------------------- | ------------------------------------------------ |
| name                      | full name of target customer                     |
| customer                  | link to the customer dashboard                   |
| amount                    | amount to be paid (not in customer_mail_content) |
