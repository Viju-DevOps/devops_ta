import psycopg2
import mysql.connector


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
            self.conn = mysql.connector.connect(host=db_configurations["DB_HOST"], database=db_configurations["DB_NAME"], user=db_configurations["DB_USER"], password=db_configurations["DB_PWD"],auth_plugin='mysql_native_password',port= db_configurations["DB_PORT"])
            # self.conn = psycopg2.connect(self.conn_string)
            self.cursor = self.conn.cursor()
            self.create_tables()
        except Exception as error:
            print(error)

    def create_tables(self):
        """ create tables in the database"""
        commands = [
            """CREATE TABLE IF NOT EXISTS user_details (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    name TEXT,
                    original_script TEXT,
                    title JSON,
                    designation JSON,
                    dob JSON,
                    pob JSON,
                    gender VARCHAR(5),
                    alias_name_good_quality JSON,
                    alias_name_low_quality JSON,
                    nationality JSON,
                    passport_no JSON,
                    national_identification_no JSON,
                    national_identification_details JSON,
                    identification_no JSON,
                    drivers_license_no JSON,
                    email_address JSON,
                    address JSON,
                    listed_on TEXT,
                    updated_on TEXT,
                    position JSON,
                    other_information TEXT,
                    data_source VARCHAR(5),
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
