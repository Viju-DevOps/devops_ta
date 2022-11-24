import psycopg2


class DbManager(object):
    """
    DbManager class which handle database related functions
    """

    def __init__(self, db_configurations):
        super(DbManager, self).__init__()
        self.conn_string = "host=" + db_configurations["DB_HOST"] + " port=" + db_configurations["DB_PORT"] + " dbname="\
                           + db_configurations["DB_NAME"] + " user=" + db_configurations["DB_USER"] \
                           + " password=" + db_configurations["DB_PWD"]
        try:

            self.conn = psycopg2.connect(self.conn_string)
            self.cursor = self.conn.cursor()
            self.create_tables()
        except Exception as error:
            print(error)

    def create_tables(self):
        """ create tables in the database"""
        commands = [
            """CREATE TABLE IF NOT EXISTS user_details(
                       id SERIAL PRIMARY KEY NOT NULL,
                       name TEXT,
                       original_script TEXT SET DEFAULT NULL,
                       title TEXT[] SET DEFAULT NULL,
                       designation TEXT[] SET DEFAULT NULL,
                       dob TEXT[] SET DEFAULT NULL,
                       pob TEXT[] SET DEFAULT NULL,
                       gender TEXT SET DEFAULT NULL,
                       alias_name_good_quality TEXT[] SET DEFAULT NULL,
                       alias_name_low_quality TEXT[] SET DEFAULT NULL,
                       nationality TEXT[] SET DEFAULT NULL,
                       passport_no TEXT[] SET DEFAULT NULL,
                       national_identification_no TEXT[] SET DEFAULT NULL,
                       national_identification_details TEXT[] SET DEFAULT NULL,
                       identification_no json SET DEFAULT NULL,
                       drivers_license_no TEXT[] SET DEFAULT NULL,
                       email_address TEXT[] SET DEFAULT NULL,
                       address TEXT[] SET DEFAULT NULL,
                       listed_on TEXT SET DEFAULT NULL,
                       updated_on TEXT SET DEFAULT NULL,
                       position TEXT[] SET DEFAULT NULL,
                       other_information TEXT SET DEFAULT NULL,
                       data_source TEXT SET DEFAULT NULL,
                       created_on TIMESTAMP not null default CURRENT_TIMESTAMP
                            );""",
        ]
        try:
            for command in commands:
                self.cursor.execute(command)
            self.conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def close_db_connection(self):
        """Function to close the cursor and connection object

        Returns: return True if connection closed successfully

        """
        try:
            self.cursor.close()
            self.conn.close()
        except Exception as error:
            print(error)

    def multiple_row_insertion(self, data_list, table_name):
        """DB population of multiple Data lines of same category

        Args:
            data_list: List of multiple data
            table_name: Name of the table to insert the data

        Returns: returns true if the data insertion is successful

        """
        for data in data_list:
            query = "INSERT INTO "+table_name+" (" + ", ".join(data.keys()) + \
                    ") VALUES (" + ", ".join(["%("+details+")s" for details in data]) + ");"
            self.cursor.execute(query, data)
            self.conn.commit()

    def delete_multiple_rows(self, table_name, column_name, value):
        """Multiple row deletion of a table based on column value

        Args:
            table_name: Name of the table to delete the data
            column_name: Name of the column
            value: Value of the column to be deleted

        Returns: returns true if the data deletion is successful

        """
        query = "DELETE FROM "+table_name+" WHERE "+column_name+" = '"+value+"';"
        self.cursor.execute(query)
        self.conn.commit()
