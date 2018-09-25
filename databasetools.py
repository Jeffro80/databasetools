# To Add:

# - Factor for students with the same name - find duplicates and set these to
# - 'Unknown' Student ID

# Known issues

# - 

# To Fix:

# - 


import re


def add_ids(ids, raw_data, name_pos, name_format='n'):
    """Add Enrolment and Student IDs to data set based on Student Name.
    
    Adds the Enrolment ID, Student ID and Course to each record in the data by
    finding the Student in the ids list. name_format can be 'n' for the Name
    being First Name + Last Name. If the name columns are separated use the
    name_format 'fl'. If a name cannot be found 'Unknown' will be placed in the
    ID columns and needs to be processed by the calling function. Returned data
    has a column added with the Enrolment ID returned (in postion 0), Student
    ID (in position 1) and Course (in position 2). These columns will be added
    to the data (should not be present in the raw data when passed).
    
    Any names that cannot be found in the ids list will be returned in a list.
    The caller needs to handle this list, printing out the names and saving to
    a file for instance.
    
    Args:
        ids (list): List of Enrolment IDs, Student IDs, Course and 
        Student Names.
        raw_data (list): List of lists containing student data. Data must
        have a column for the student name.
        name_pos (int): Column position in raw_data with name or first name
        data.
        name_format (str): Indicates the format of the name in rw_data:
            - 'n' is First Name Last Name (one column)
            - 'fl' is First Name, Last Name (two columns).
    
    Returns:
        updated_data (list): List of lists with Student ID added.
        unknown_names (set): List of Student Names that could not be found.
        
    List structure (ids):
        EnrolmentID, StudentID, Name.
    """
    updated_data = []
    unknown_names = set()
    print('\nGetting Student and Enrolment ID\'s')
    if name_format not in ['n', 'fl']:
        return raw_data
    else:
        num_students = len(raw_data) # For calculating % complete
        n = 1
        for student in raw_data:
            # Display progress
            progress = round((n/num_students) * 100)
            print("\rProgress: {}{}".format(progress, '%'), end="", flush=True)
            this_student = []
            # Check name format
            if name_format == 'n': # One column for name 
                name = student[name_pos] # Get student name
            elif name_format == 'fl': # Two column for name
                name = student[name_pos] + ' ' + student[name_pos + 1]
            found = False
            # Look for student name in ids
            for record in ids:
                if record[3] == name: # Name found
                    enrolment_id = record[0]
                    student_id = record[1]
                    course = record[2]
                    found = True
                    break
            # Student not found in ids
            if not found:
                unknown_names.add(name)
                enrolment_id = 'Unknown'
                student_id = 'Unknown'
                course = record[2]
            # Add student data
            this_student.append(enrolment_id)
            this_student.append(student_id)
            this_student.append(course)
            for item in student:
                this_student.append(item)
            # Add student to updated_data
            updated_data.append(this_student)
            n += 1
        print('\rFinished getting Student ID\'s')            
        return updated_data, unknown_names  


def add_student_ids(ids, raw_data, name_pos, name_format='n'):
    """Add Student ID number to data set based on Student Name.
    
    Adds the Student ID number to each record in the data by finding the
    Student in the ids list. name_format can be 'n' for the Name being First
    Name + Last Name. If the name columns are separated use the name_format
    'fl'. If a name cannot be found 'Unknown' will be placed in the Student ID
    column and needs to be processed by the calling function. Returned data has
    a column added with the Student ID returned (in postion 0). Note the
    student's Enrolment ID Number can be supplied and then added to the data
    instead.
    
    Args:
        ids (list): List of Student IDs and Student Names:
        raw_data (list): List of lists containing student data that does not
        have a Student ID but does have a column for student names.
        name_pos (int): Column position in raw_data with name or first name
        data.
        name_format (str): Indicates the format of the name in rw_data:
            - 'n' is First Name Last Name (one column)
            - 'fl' is First Name, Last Name (two columns).
    
    Returns:
        updated_data (list): List of lists with Student ID added.
        
    List structure (ids):
        StudentID, Name
    """
    updated_data = []
    '''
    for student in raw_data:
        name = student[name_pos]
        print(name)
    '''
    print('\nGetting Student ID\'s')
    if name_format not in ['n', 'fl']:
        return raw_data
    else:
        num_students = len(raw_data) # For calculating % complete
        n = 1
        for student in raw_data:
            # Display progress
            progress = round((n/num_students) * 100)
            print("\rProgress: {}{}".format(progress, '%'), end="", flush=True)
            this_student = []
            # Check name format
            if name_format == 'n': # One column for name 
                name = student[name_pos] # Get student name
            elif name_format == 'fl': # Two column for name
                name = student[name_pos] + ' ' + student[name_pos + 1]
            found = False
            # Look for student name in ids
            for record in ids:
                if record[1] == name: # Name found
                    student_id = record[0]
                    found = True
                    break
            # Student not found in ids
            if not found:
                student_id = 'Unknown'
            # Add student data
            this_student.append(student_id)
            for item in student:
                this_student.append(item)
            # Add student to updated_data
            updated_data.append(this_student)
            n += 1
        print('\rFinished getting Student ID\'s')
        return updated_data  


def check_post_code(post_code, country):
    """Return the status of the post code.

    Checks if the post code has four digits (for NZ post codes).
    Uses country to make sure only NZ postcodes are evaluated. Country needs to
    be the name, e.g. 'New Zealand', and not a country code.

    Args:
        post_code (str): The post code to be checked.
        country (str): The country the post code is from.

    Returns:
        (str) with the following possibilities:
            'Missing' if no post_code provided (None, '')
            'Pass' if a non-NZ post code or NZ post code that is 4 characters
            'Fail' if the post code is not 3 or 4 characters long
            'Short' if the post code is only 3 characters long
    """
    if post_code in (None, ''):
        return 'Missing'
    elif country.strip() != 'New Zealand':
        return 'Pass'
    elif len(post_code) not in (3, 4):
        return 'Fail'
    elif len(post_code) == 3:
        return 'Short'
    else:
        return 'Pass'


def check_username(username):
    """Check that username is valid.

    Checks that username is only letter, no numbers or special characters.

    Args:
        username (str): The username to be checked.

    Returns:
        True if username is valid, False otherwise.
    """
    if username.isalpha():
        return True
    else:
        return False


def convert_pacific(ethnicity, islands):
    """Convert Pacific Island ethincities to 'Pasifika'.
    
    Args:
        ethnicity (str): Passed ethnicity.
        islands (list): List of Pacific Island nations.
    
    Retrurns:
        ethnicity (str) 'Pasifika' if ethnicity is found in the Pacific
        Island nations list or the passed ethnicity if it is not.
    """
    if ethnicity in islands:
        return 'Pasifika'
    else:
        return ethnicity 


def extract_course_code(course):
    """Extract the course code.
    
    Looks for the course code in a course string (XXX-XX-XXX). If it is present
    it returns the course code. If it is not present it returns 'Skip'.
    
    Args:
        course (str): Full course name to be searched.
    
    Returns:
        Either the course code or 'Skip' if a course code cannot be found.
    """
    if re.search('.+\(.+-.+-.+\)', course):
        # Extract the course code and return it
        start = course.index('(')
        return course[start+1:-1]
    else:
        return 'Skip'


def extract_street(street_data):
    """Extract street from data.
    
    Returns the string from the position after the first space to the end of
    the string. In theory this should be the street portion of the entry.
    
    Args:
        street_data (str): Combined Number and Street.
        
    Returns:
        (str): Street.
    """
    first = street_data.index(' ') + 1
    return street_data[first:]


def extract_street_number(street_data):
    """Extract street number from data.
    
    Returns the string from the start to the position before the first space of
    the string. In theory this should be the street number portion of the
    entry.
    
    Args:
        street_data (str): Combined Number and Street.
        
    Returns:
        (str): Street.
    """
    first = street_data.index(' ')
    return street_data[:first]


def get_ids(file_data, id_pos=0):
    """Extract Student IDs into a single list.
    
    Takes each Student ID that is an individual list and places the Student ID
    as a string into one list.
    
    Args:
        file_data (list): List of Student IDs, each as a list.
        id_pos (int): Position of the Student ID within the data.
        
    Returns:
        student_ids (list): List of Student IDs stored as strings.
    """
    student_ids = []
    for student in file_data:
        student_ids.append(student[id_pos])        
    return student_ids