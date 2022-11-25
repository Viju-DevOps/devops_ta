import data_parser
from configuration.configuration import get_configurations


if __name__ == '__main__':
    table_name = 'user_details'
    column_name = 'data_source'

    # Fetch configurations from configuration YAML file
    configurations = get_configurations()

    # Start RBI parsing
    rbi_data_list = data_parser.start_rbi_parser(configurations)

    # Start RBI Data insertion
    if rbi_data_list:
        data_parser.clear_table_contents(configurations, table_name, column_name, 'RBI')
        data_parser.start_db_insertion(configurations, rbi_data_list)

    # Start UK parsing
    uk_data_list = data_parser.start_uk_parser(configurations)
   
    # Start UK Data insertion
    if uk_data_list:
        data_parser.clear_table_contents(configurations, table_name, column_name, 'UK')
        data_parser.start_db_insertion(configurations, uk_data_list)

    # Start US parsing
    us_data_list = data_parser.start_us_parser(configurations)
   
    # Start US Data insertion
    if us_data_list:
        data_parser.clear_table_contents(configurations, table_name, column_name, 'US')
        data_parser.start_db_insertion(configurations, us_data_list)

    # Start EU parsing
    eu_data_list = data_parser.start_eu_parser(configurations)

    # Start EU Data insertion
    if eu_data_list:
        data_parser.clear_table_contents(configurations, table_name, column_name, 'EU')
        data_parser.start_db_insertion(configurations, eu_data_list)
