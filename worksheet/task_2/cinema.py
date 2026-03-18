"""
This is where you should write your code and this is what you need to upload to Gradescope for autograding.

You must NOT change the function definitions (names, arguments).

You can run the functions you define in this file by using test.py (python test.py)
Please do not add any additional code underneath these functions.
"""

import sqlite3


def customer_tickets(conn, customer_id):
    """
    Return a list of tuples:
    (film_title, screen, price)

    Include only tickets purchased by the given customer_id.
    Order results by film title alphabetically.
    """
    query = """
    SELECT films.title AS film_title, screenings.screen, tickets.price
    FROM tickets
    JOIN screenings ON screenings.screening_id = tickets.screening_id
    JOIN films ON films.film_id = screenings.film_id
    WHERE tickets.customer_id = ?
    ORDER BY film_title ASC;
    """
    cursor = conn.execute(query, (customer_id,))
    return cursor.fetchall()


def screening_sales(conn):
    """
    Return a list of tuples:
    (screening_id, film_title, tickets_sold)

    Include all screenings, even if tickets_sold is 0.
    Order results by tickets_sold descending.
    """
    query = """
    SELECT screenings.screening_id, films.title AS film_title, COUNT(tickets.ticket_id) AS tickets_sold
    FROM screenings
    JOIN films ON films.film_id = screenings.film_id
    LEFT JOIN tickets ON tickets.screening_id = screenings.screening_id
    GROUP BY screenings.screening_id, films.title
    ORDER BY tickets_sold DESC;
    """
    cursor = conn.execute(query)
    return cursor.fetchall()


def top_customers_by_spend(conn, limit):
    """
    Return a list of tuples:
    (customer_name, total_spent)

    total_spent is the sum of ticket prices per customer.
    Only include customers who have bought at least one ticket.
    Order by total_spent descending.
    Limit the number of rows returned to `limit`.
    """
    query = """
    SELECT customers.customers_name, SUM(tickets.price) AS total_spent
    FROM tickets
    JOIN customers ON tickets.customer_id = customers.customers_id
    GROUP BY customers.customers_id, customers.customers_name
    ORDER BY total_spent DESC
    LIMIT ?;
    """
    cursor = conn.execute(query, (limit,))
    return cursor.fetchall()
