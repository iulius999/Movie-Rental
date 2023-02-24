# Movie-Rental
Movie Rental Application - Python, Layered Architecture implementation (with Object-Oriented Programming and Test-Driven Development)

UI ---> SERVICES ---> REPOSITORY ---> DOMAIN                                                                                                                             
The application can be started by running the file start.py and it has its own exception classes.

The Movie Rental Application allows users to: 
 - add, remove and update movies, clients or rentals
 - rent and return movies
 - search movies, clients and rentals by typing matching characters
 - view different kinds of statistics such as most rented movies, most active clients
 - undo operations, by implementing an undo stack having a cascading effect (deleting a client also removes all his rentals, for example)
 
 It has a console based user interface and it interacts with the user by giving him instructions for typing the corresponding commands for the desired action. The app 
 also catches errors and throws the corresponding error messages back to the user.
