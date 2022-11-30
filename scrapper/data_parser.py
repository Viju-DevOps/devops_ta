from rbi_parser.rbi_parser import start_rbi_parsing
from uk_parser.uk_parser import start_uk_parsing
from us_parser.us_parser import start_us_parsing
from eu_parser.eu_parser import start_eu_parsing
from db_manager import DbManager


def start_rbi_parser(configurations):
    """ Function to parse RBI sanction list file

    Args:
        configurations: list of configurations

    Returns: returns True if parsing completed successfully

    """
    # Start RBI parser
    rbi_sanction_list = start_rbi_parsing(configurations['RBI_URL'])
    return rbi_sanction_list


def start_uk_parser(configurations):
    """ Function to parse UK sanction list file

    Args:
        configurations: list of configurations

    Returns: returns True if parsing completed successfully

    """
    # Start UK parser
    uk_sanction_list = start_uk_parsing(configurations['UK_URL'])
    return uk_sanction_list


def start_us_parser(configurations):
    """ Function to parse US sanction list file

    Args:
        configurations: list of configurations

    Returns: returns True if parsing completed successfully

    """
    # Start US parser
    us_sanction_list = start_us_parsing(configurations['US_URL'])
    return us_sanction_list


def start_eu_parser(configurations):
    """ Function to parse European sanction list file

    Args:
        configurations: list of configurations

    Returns: returns True if parsing completed successfully

    """
    # Start EU parser
    eu_sanction_list = start_eu_parsing(configurations['EU_URL'], configurations['EU_DOWNLOAD_FOLDER_NAME'])
    return eu_sanction_list


def start_db_insertion(configurations, data_list):
    """Function to insert sanction data into database

    Args:
        configurations: list of configurations
        data_list: List of data

    Returns: returns True if database insertion is successful

    """
    db_obj = DbManager(configurations)
    db_obj.multiple_row_insertion(data_list, 'sanctions_list')
    db_obj.close_db_connection()


def clear_table_contents(configurations, table_name, column_name, value):
    """Function to clear sanction data in the database

    Args:
        configurations: list of configurations
        table_name: Name of the table in which data to be removed
        column_name: Name of the column to the value to be matched
        value: value in the column

    Returns: returns True if data removal is successful

    """
    db_obj = DbManager(configurations)
    db_obj.delete_multiple_rows(table_name, column_name, value)
    db_obj.close_db_connection()


