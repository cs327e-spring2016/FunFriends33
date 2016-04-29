
# we'll need to reference a list of attributes, their types, and collect them by whether they are numeric or stringy, and reference a list of aggregate functions
# this is the list of attributes which head the columns in our CarsForSale table
attrs = ['a','b','c']
attr_types = ['INT','INT','CHAR']
numeric_attrs = ['INT','FLOAT','YEAR']
stringy_attrs = ['CHAR','VARCHAR']
aggregate_fns = ['COUNT','MAX','MIN','SUM','AVG',]

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
    print()
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


# this functions takes a string and returns the bit between parentheses if there are any; otherwise it returns the string as is
# it is used to make the get_conditions functions work for having clause conditions, where the attribute name is in parenthese, as an argument to the aggregate function
def between_parens(attr):
    if '(' in attr:
        # build a new string only including that between the parens
        st = ''
        record = False # to keep track of whether we should be recording the chs
        for ch in attr:
            if record:
                if ch == ')': # we've gotten all we can use, return the new string
                    return st 
                else:
                    st += ch 
            else:
                if ch == '(':
                    record = True
        # we should'nt make it out of the for loop, but if this somehow happens, return st as is to avoid issues
        return st 

    # otherwise the attr should be well-formatted
    else:
        return attr # as is


# this function takes an attribute name and makes a string of the conditions for the attribute for the query, based on user input
# this also works for the conditions of an aggregate function's value for the having clause
# to distinguish between these cases, which need to be handled slightly differently, we take the clause type (where or having) as an argument
def get_conditions(attr, clause):
    idx = attrs.index(between_parens(attr))
    attr_type = attr_types[idx]
    stmt = ''
    sub_stmt1 = ''
    sub_stmt2 = ''
    # based on the type, we will need different conditions input from the user
    print()
    print('For the attribute ' + attr + '...')
    # if the value is numeric, get upper and lower bounds
    if attr_type in numeric_attrs or clause == 'having': # having clause conditions should always be numeric
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
    elif attr_type in stringy_attrs:
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
    print()
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
                cond_stmt = get_conditions(attr,'where')
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

# this function builds the query's order by statement, if we have one
def build_order_by():
    print()
    print('We will now build the order by clause of our query. \n')
        
    stmt = ''
    want_ordered = input('Would you like to order the results by any attributes? (y/n): ').strip().lower()
    if want_ordered=='y':
        stmt += 'ORDER BY '
        order_attrs = input('Please enter all attributes by which you would like to order the results, \n' +
                           'separated by spaces, in the order you would like them applied: ').strip().split()
        for attr in order_attrs:
            if attr in attrs:
                ad = input('Would you like ' + attr + ' to be ordered ascending or descending? (a/d): ').strip().lower()
                if ad=='a':
                    stmt += attr + ' ASC, '
                # default to descending
                else:
                    stmt += attr + ' DESC, '
        # if we somehow didn't add anything to order by, just make the clause empty
        if stmt == 'ORDER BY ':
            stmt = ''
        # get rid of the last comma to make the clause syntactically correct
        else:
            stmt = stmt[:-2] + ' '
    # no matter what, we want to return the statement as is
    # note that we default to a 'n' response for want_ordered if input is faulty
    return stmt 

# this function builds the group by and having clauses of the query if the user wants to use aggregate functions;
# it takes the select statement as an argument, which will need to be altered depending on the aggregations chosen
def build_group_by_having(select_stmt):
    print()
    print('We will now build the group by and having clauses of our query.')
    yn = input('Would you like to use an aggregate function? (y/n): ').strip().lower()
    if yn =='y':
        print()
        # tell the user his/her options as far as aggregate functions go
        print('Here are the aggregation functions from which you can choose:')
        for aggregate_fn in aggregate_fns:
            print('     * ' + aggregate_fn)
        print()
        aggs = input('Please enter those of the above functions you would like to use to group your results, \n' + 
                     'as shown, separated by spaces: ').strip().upper().split()
        # get the attributes to which the user would like to apply the aggregations
        agg_attrs = []
        for agg in aggs:
            agg_attr = agg + '(' + input('Please enter the name of the attribute to which you wish to apply the aggregate function ' + agg + ': ').strip() + ')'
            agg_attrs.append(agg_attr)
        # get the group by attr
        group_by_stmt = ''
        gb = input('Please enter the name of the attribute by which you would like to group these aggregations: ').strip()
        if gb in attrs:
            group_by_stmt = 'GROUP BY ' + gb 
        # if we have a faulty group by, default to no group by / where clause
        else:
            return '','',select_stmt
            
        # now find out the conditions for the having clause
        having_conds = []
        for agg_attr in agg_attrs:
            cond = get_conditions(agg_attr,'having')
            having_conds.append(cond)
        # now we have to cycle through the aggs and conds to keep only those which are usable
        for i in range (len(aggs)):
            if aggs[i] in aggregate_fns:
                pass
            else:
                del aggs[i]
                del having_conds[i]
                del agg_attrs[i]

        # now create the having statement
        # this assumes that the attributes entered by the user for the having conditions are correct
        having_stmt = 'HAVING '
        for having_cond in having_conds:
            having_stmt += having_cond + ' AND ' 
        # delete the last AND from the having statement
        having_stmt = having_stmt[:-4]

        # now add the aggregations to the select clause
        # this assumes that the select clause includes at least one attribute,
        # and that we have at least one aggregation attribute
        for agg_attr in agg_attrs:
            select_stmt += ', ' + agg_attr

        return group_by_stmt, having_stmt, select_stmt


    # note that the default is no aggregation
    else:
        return '','',select_stmt # an empty group by / having clause


def main():

    welcome()
    select_stmt = build_select()
    # all selects will be from our single table that has all cars for sale and their attributes
    from_stmt = 'FROM CarsForSale'
    where_stmt = build_where()
    order_by_stmt = build_order_by()
    group_by_stmt,having_stmt,select_stmt = build_group_by_having(select_stmt)


    # test the shit by printing it and seeing if everything's cool
    print(select_stmt)
    print(from_stmt)
    print(where_stmt)
    print(order_by_stmt)
    print(group_by_stmt)
    print(having_stmt)




main()





