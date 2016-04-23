

# this is the list of attributes which head the columns in our CarsForSale table
attrs = ['a','b','c']
attr_types = ['INT','INT','CHAR']


# this function welcomes the user and acquaints him/her with the program
def welcome():
    print()
    print('Welcome to Ranger Motors Database Query Interface! \n' + 
          'Here you can run queries on Ranger Motors\' Inventory to \n' + 
          'to filter the inventory with custom criteria or run aggregate statistics on the inventory. \n' + 
          'Let\'s get started!')
    print()
    print('First I will ask you to choose some attributes to display in the query results. \n' + 
          'Then you can display those rows by: \n' +
          '     * filtering rows out based on the values of one or more of their attributes; \n' + 
          '     * sorting rows based on the values of one or more of their attributes; \n' +
          '     * grouping the results based on a customizable statistic from the table')
    print()
    print('Here are the attribute names from which you can choose: ')
    for attr in attrs:
        print('     ' + attr)
    print()

# this function builds the select clause of the query statement based on user input
# default is to select all attributes (SELECT *)
def build_select():
    print('We are now going to build the select statement for our query. \n' +
          'Please tell me which of the above attributes you\'d like to include in the results.')
    # make a set of the user's desired select attributes, so we have no repeats
    select_attrs = set( (input('To do this, type the full attribute name(s), as shown above, separated by spaces: ')).strip().split() )
    stmt = 'SELECT '
    # if the user input any attributes, add each to the statement in turn;
    # otherwise, select every attribute in the table
    if len(select_attrs):    
        for attr in select_attrs:
            stmt += attr + ', '
            # if the user input an attr name that doesn't exist, default to selecting all attributes
            if attr not in attrs:
                return 'SELECT *'
    else:
        stmt += '* '
    # delete the last comma from our select statement to make it syntactically correct
    stmt = stmt[:-2] + ' '
    return stmt 

# this function takes an attribute name and makes a string of the conditions for the attribute for the query, based on user input
def get_conditions(attr):
    idx = attrs.index(attr)
    attr_type = attr_types[idx]
    stmt = ''
    sub_stmt1 = ''
    sub_stmt2 = ''
    # based on the type, we will need different conditions input from the user
    print('For the attribute ' + attr + '...')
    # if the value is numeric, get upper and lower bounds
    if attr_type in ('YEAR','INT','FLOAT'):
        print('This attribute is numeric;')
        eb = input('Would you like to place an equality condition or bounds on this value? (e for equality, b for bound): ').strip().lower()
        if eb=='b':
            # get lower bound, if any
            yn = input('Would you like a lower bound on the value of this attribute? (y/n): ').strip().lower()
            if yn == 'y':
                ie = input('Would you like this bound to be inclusive or exclusive? (i/e): ')
                bound = input('What would you like the bound to be? (enter any numeric value): ')
                if ie == 'i':
                    sub_stmt1 = ' ' + attr + ' >= ' + bound + ' '
                else:
                    sub_stmt1 = ' ' + attr + ' > ' + bound + ' '
            # get upper bound, if any
            yn = input('Would you like an upper bound on the value of this attribute? (y/n): ').strip().lower()
            if yn == 'y':
                ie = input('Would you like this bound to be inclusive or exclusive? (i/e): ')
                bound = input('What would you like the bound to be? (enter any numeric value): ')
                if ie == 'i':
                    sub_stmt2 = ' ' + attr + ' <= ' + bound + ' '
                # by letting treating all else conditions as 'e', we are letting 'e' be default
                else:
                    sub_stmt2 = ' ' + attr + ' < '  + bound + ' '
            if sub_stmt1 and sub_stmt2:
                return sub_stmt1 + 'AND' + sub_stmt2
            else:
                stmt += sub_stmt1 if sub_stmt1 else ''
                stmt += sub_stmt2 if sub_stmt2 else ''
                return stmt
        # by letting treating all else conditions as 'e', we are letting 'e' be default
        else:
            equals = input('To what would you like the value of this attribute to be equal? (enter any numeric value): ').strip()
            stmt = ' ' + attr + ' = ' + equals + ' '
            return stmt 

    # if the value is stringish, see what values the user would like allowed in the string 
    elif attr_type in ('CHAR','VARCHAR'):
        print('This attribute is stringish;')
        allowed_str = (input('Please enter the string value you would like to search for: ')).strip()
        ie = input('Would you like the value to match exactly to the attribute value or to be found in the attribute value? (e for exactly, i for included/inexactly): ').strip().lower()
        # by letting treating all else conditions as 'i', we are letting 'i' be default
        if ie == 'e':
            stmt = attr + ' = ' + allowed_str
        else:
            stmt = attr + ' LIKE \'%' + allowed_str + '%\' '
        return stmt 

    # if the attr type didn't match any of the types above, this part of the where statement will be blank
    return stmt 

# this function builds the query's where statement based on user input
# default is to have no where statement
def build_where():
    print('Now we will build the where statement for our query. \n' +
          'Please tell me which of the attributes you would like to use to filter the results, \n' +
          'just as you did for the select statement. \n' +
          '(If you would like to place more than one condition on an attribute,')
    # this time we want a list, since the user might input an attribute more than once
    where_attrs = (input('please enter that attribute the desired number of times as part of your input): ')).strip().split()
    stmt = ''
    # if we have some where attributes, we'll have a where clause, so go ahead and start that
    if where_attrs:
        stmt = 'WHERE '
        # for each attribute we want to filter, get the condition statement and add it to the where clause
        for attr in where_attrs:
            # just ignore any invalid attributes that were entered
            if attr in attrs:
                cond_stmt = get_conditions(attr)
            # depending on how much of the where clause we have, we'll add this condition differently
            if stmt == 'WHERE ':
                stmt += cond_stmt
            else:
                stmt += 'AND ' + cond_stmt
        # if somehow we added no attribute conditions, return an empty where statement
        if stmt == 'WHERE ':
            return ''
        # otherwise, return the where clause we built with some space at the end
        return stmt + ' '


def main():

    welcome()
    select_stmt = build_select()
    # all selects will be from our single table that has all cars for sale and their attributes
    from_stmt = 'FROM CarsForSale'
    where_stmt = build_where()
    print(select_stmt)
    print(from_stmt)
    print(where_stmt)




main()





