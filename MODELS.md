# Models and Expressions
This document describes the models and relations between them of smarttickts.  

## Definition

### Setting
A setting is apart of the complete settings.  
It contains for example the image of the theatre which will displayed on in the frontend.

### Meeting
A meeting represents a show and is responsible for the sale start and so on.
You can also set the pricing for the meeting.

### Room
A room represents the structure of the physical room.
You can create a room-template and use this in different meetings.

### Seat
A seat is in exactly one room and contains attributes like the price, hints about the accessibility, 
the position and the direction.
 

### Ticket
A ticket is an paid or non-paid seat of one meeting.
It includes an qr-code and the customer.

### Customer
A customer can buy a ticket. He can access his order and account information by using the link of the 
confirmation mail.

### Administrator
An administrator is maintaining the system. He can create rooms, seats, meetings and update the settings.

## Questions
If you need free support by an configuration of your smartticket-system you can contact me (https://github.com/use-to/).  
I`ll try to help you as quick as possible.