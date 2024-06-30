# HGP_PROGRAM

Program of a hostel administration system using local database (SQLite) or remote databases (MySQL).

Databases:
- SQLAlchemy allows to connect to SQLite and MySQL databases that have the same tables. The structure is found in the directory db.
- Main entity tables in the databases are: Habitaciones (rooms), Clientes (clients), Alquileres (rents), and Habitaciones_estado(room states).
- The program allos to migrate data between two databases

Architechture:
- MVC (Model-View-Controller)
  Model: db.py
  View: gui_hgp.py
  Controller: hgp.py

Languagues:
- Python

Main Libraries:
- SQL Alchemy (connection to SQLite and MySQL)
- Pyqt 6 (GUI)

GUI:

Main window view:
- Subwindows for observing and modifying table entities: Habitaciones (rooms), Clientes (clients), Alquileres (rents), and Habitaciones_estado(room states)
![alt text](https://github.com/JhonVelasquez/HGP_PROGRAM/program_main.png)

Database management:
- Selection of the route to the database.
- Migration between two databases, the route for address source and destination are needed.
![alt text](https://github.com/JhonVelasquez/HGP_PROGRAM/db_management.png)
