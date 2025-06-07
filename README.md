# Flask Asset Manager

This project demonstrates a small web application built with **Flask** and
**SQLite** for managing IT assets. It showcases common programming concepts such
as routing, templating, database interaction using ORM, authentication, and role
based access control. The app follows a modular design with reusable
components and includes automated tests with `pytest`.

## Agile Approach

Development was planned in small increments. Features were prioritised and
implemented iteratively:

1. Set up project structure and database models.
2. Implemented user registration and authentication.
3. Added CRUD operations for assets with role checks.
4. Created simple templates for usability.
5. Wrote automated tests to cover main functionality.
6. Updated documentation and sample data.

Each step could represent an iteration in an Agile process, allowing feedback to
shape the next phase.

## Running the application

Install the dependencies and start the development server:

```bash
pip install -r requirements.txt
python run.py
```

Visit `http://localhost:5000` in the browser. Register a new user or log in with
the credentials defined in the tests: `admin` / `admin` for administrator
access.

To populate the database with 10 sample users and assets run:

```bash
python sample_data.py
```

## Database Schema

Two tables are used:

- **User** – stores usernames, hashed passwords and roles (`admin` or
  `regular`).
- **Asset** – stores asset information such as name, type, serial number and
  location. Each asset is linked to the user that created it.

The tables include primary key fields (`id`) and a foreign key (`owner_id`)
linking assets to users.

## Programming Concepts

- **Blueprints** modularise routes (`auth` for authentication and `asset` for
  asset management).
- **Flask-SQLAlchemy** provides an ORM layer – models are Python classes mapped
  to tables. Queries use Python syntax rather than raw SQL.
- **Flask-Login** handles session management so routes can require an
  authenticated user.
- **Templates** use Jinja2 syntax to render HTML dynamically, with control
  structures like loops and conditionals.
- **Validation** logic checks for empty fields and duplicate serial numbers,
  showing messages when rules are broken.

## Tests

Run all tests with:

```bash
pytest
```

The tests create an isolated database, register users, log in and exercise CRUD
operations to ensure the application behaves as expected.
