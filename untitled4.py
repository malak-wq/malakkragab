import pyodbc
import json
import socket

# Database connection parameters
conn_str = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=LAPTOP-O9NAVCSL;"
    "DATABASE=school;"
    "Trusted_Connection=yes;"
)

# Create and write HTML output to a file
def create_html_file():
    try:
        # Establish the database connection
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        # Execute a query to retrieve data from the 'students' table
        cursor.execute("SELECT * FROM students")

        # Start building the HTML output with embedded CSS for a white and blue theme
        html_output = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>exam time table</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background-color: #e6f7ff; /* Light blue background */
                    color: #00274d; /* Dark blue text */
                    margin: 20px;
                }
                table {
                    width: 100%;
                    border-collapse: collapse;
                }
                th, td {
                    border: 1px solid #00274d; /* Dark blue border */
                    padding: 8px;
                    text-align: left;
                }
                th {
                    background-color: #00509e; /* Blue background for headers */
                    color: #ffffff; /* White text */
                }
                tr:nth-child(even) {
                    background-color: #d1e7ff; /* Light blue for even rows */
                }
                h1 {
                    color: #00274d; /* Dark blue header */
                }
            </style>
        </head>
        <body>
            <h1>exam time table</h1>
            <table>
                <tr>
        """

        # Add column headers
        columns = [column[0] for column in cursor.description]
        for col in columns:
            html_output += f"<th>{col}</th>"
        html_output += "</tr>"

        # Add data rows
        for row in cursor.fetchall():
            html_output += "<tr>"
            for cell in row:
                html_output += f"<td>{cell}</td>"
            html_output += "</tr>"

        # Close the table and HTML tags
        html_output += """
            </table>
        </body>
        </html>
        """

        # Write the HTML output to an index.html file
        with open("indexxx.html", "w", encoding="utf-8") as file:
            file.write(html_output)

        print("HTML file 'indexxx.html' has been created successfully.")

    except Exception as e:
        print("An error occurred:", e)

    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# Run the Python HTTP server
def run_server():
    # Create a TCP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 8080))
    server_socket.listen(5)
    print("Server is running on http://localhost:8080...")

    while True:
        # Accept an incoming connection
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address}")

        # Receive the HTTP request
        request = client_socket.recv(1024).decode('utf-8')
        print("Request received:\n", request)

        # Create HTTP response
        try:
            with open("indexxx.html", "r", encoding="utf-8") as file:
                html_content = file.read()

            response = (
                "HTTP/1.1 200 OK\n"
                "Content-Type: text/html\n"
                "Connection: close\n\n"
                f"{html_content}"
            )
        except Exception as e:
            response = (
                "HTTP/1.1 500 Internal Server Error\n"
                "Content-Type: text/html\n"
                "Connection: close\n\n"
                f"<html><body><h1>500 Internal Server Error</h1><p>{str(e)}</p></body></html>"
            )

        # Send the response to the client
        client_socket.sendall(response.encode('utf-8'))
        client_socket.close()

# Run the Python script
if __name__ == '__main__':
    create_html_file()  # Create the HTML file first
    run_server()        # Start the HTTP server


