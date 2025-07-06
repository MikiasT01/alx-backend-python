```python
#!/usr/bin/python3
import seed

def paginate_users(page_size, offset):
    """
    Fetches a page of users from the user_data table with the specified page size and offset.
    Args:
        page_size (int): Number of rows to fetch per page.
        offset (int): Starting row number for the page.
    Returns:
        list: A list of dictionaries containing user_id, name, email, and age.
    """
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return rows

def lazy_paginate(page_size):
    """
    Generator function to lazily load paginated data from the user_data table.
    Args:
        page_size (int): Number of rows per page.
    Yields:
        list: A list of dictionaries for each page, containing user_id, name, email, and age.
    """
    offset = 0
    # Single loop to fetch pages until no more rows are returned
    while True:
        page = paginate_users(page_size, offset)
        if not page:  # Break if no more rows
            break
        yield page
        offset += page_size
```