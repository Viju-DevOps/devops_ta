import re
import json
import datetime
import pandas as pd

def remove_multiple_delimiters(string, delimiter_string):
    """Function to split a string with multiple delimiters

    Args:
        string: String contains multiple delimiters'
        delimiter_string: list of delimiters

    Returns: returns list of strings in which multiple delimiters are removed

    """
    output_string_list = []
    if string:
        string_list = re.split(delimiter_string, string)
        for string in string_list:
            if string != "":
                output_string_list.append(string.strip().replace(".","").replace("Approximately","").strip())
    return output_string_list


def split_values_and_generate_list(lst):
    """Function to extract individual place from a string
    of comma separated places.

    Args:
        lst: list containing list of multiple places'

    Returns: returns list of strings in which individual places are seperated

    """
    return json.dumps([single_place for places in lst for single_place in places.split(",") if single_place !=""])


def dob_format_converter_uk(dob_string):
    """Function to extract individual dobs from a string
    of number "(0)" seperated dobs.

    Args:
        dob_string: string containing list of multiple dobs'
        

    Returns: returns list of strings in which individual dobs are seperated

    """
    import datetime
    dates=[]
    digits_delimiters_dob= r'[(][0-9]\)'
    converter=remove_multiple_delimiters(dob_string, digits_delimiters_dob)

    for i in converter:
        if "--" in i:
            dates.append(i[-4:])
        elif "/" in i:
            raw_date = datetime.datetime.strptime(i, "%d/%m/%Y")
            s = raw_date.strftime('%Y-%m-%d')
            dates.append(s)
        else:
            dates.append(i)
    
    return json.dumps(dates)


def dob_format_converter_us(date_list):
    """Function to extract individual dobs from a string
    of number "(0)" seperated dobs and containing "circa" and months in letter format.

    Args:
        dob_string: string containing list of multiple dobs'
        

    Returns: returns list of strings in which individual dobs are seperated

    """
    dates=[]
    for dob_string in date_list:
        if "circa" in dob_string:
            continue
        else:
            dates.append(dob_string)
    return dates

def json_converter(lst):
    """"
    Args : list of data

    Returns : json converted list
    """
    return json.dumps(lst)



def dob_format_converter_rbi(splitted):
    """Function to extract individual dobs from a list of dobs in various formats.
  

    Args:
        splitted: list containing dobs in various formats
        

    Returns: returns list of dobs in which individual dobs are seperated

    """
    months = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10,
              'Nov': 11, 'Dec': 12}
    try:
        final_date_list=[]
        between_years=[]
        
        for i in splitted:
            if len(i)!=4:
                if "Between"  not in i:
                    date=i.split(" ")
                    dd=date[0]
                    mm=months[date[1]]
                    yy=date[2]
                    convert=str(yy)+"-"+str(mm)+"-"+str(dd)
                    final_date_list.append(convert)
                elif "Between" in i:
                    for year in i.split(" "):
                        if year.isnumeric()==True:
                            between_years.append(year)
                    start=int(between_years[0])
                    end=int(between_years[1])
                    count=0
                    while start <= end:
                        count=start
                        final_date_list.append(str(count))
                        start+=1

            else:
                final_date_list.append(str(i))
    except Exception as e:
        pass
    return final_date_list


def dob_format_converter_eu(dates_lst):
   
    years=[]
    final_date_list=[]
    for dates in dates_lst:
        if "Circa" or "from" in dates:
            split_date=dates.split(" ")
            if len(split_date)>2:
                for content in split_date:
                    if content.isnumeric()==True:
                        years.append(content)
                start=int(years[0])
                end=int(years[1])
                count=0
                while start <= end:
                    count=start
                    final_date_list.append(str(count))
                    start+=1
            elif len(split_date)==2: #Circa 1903 , Circa 05/05/1955
                slash_splitter = split_date[1].split("/")
                if len(slash_splitter)!=3:
                    final_date_list.append(split_date[1])
            else:
                pass #Circa
        if "/" in dates:
            split=dates.split("/")
            if len(split)==3:
                date=split[2]+"-"+split[1]+"-"+split[0].replace("Circa","").strip()
                final_date_list.append(date)
        elif len(dates)==4:
            final_date_list.append(dates)
    
    return final_date_list

def us_gender(gender):
    if len(gender)>6:
        pass
    else:
        return gender