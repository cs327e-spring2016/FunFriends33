
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pymysql
import getpass

# initialize the list of attributes, their types, their numeric-/stringy-ness, 
# and the aggregate functions the user can use ... for the query interface
attrs = ['Price', 'Year', 'Make', 'Model', 'Body style', 'Mileage', 'Transmission', 'Engine', 'Drivetrain', 'Exterior', 'Interior', 'Doors', 'Stock', 'VIN', 'Fuel Mileage', 'Conditon']
attr_types = ['INT','YEAR','VARCHAR(30)','VARCHAR(30)','VARCHAR(30)','INT','VARCHAR(30)','VARCHAR(30)','VARCHAR(30)','VARCHAR(30)','VARCHAR(30)','INT','VARCHAR(30)','VARCHAR(30)','VARCHAR(30)','VARCHAR(30)']
numeric_attrs = ['INT','FLOAT','YEAR']
stringy_attrs = ['CHAR','VARCHAR(30)']
aggregate_fns = ['COUNT','MAX','MIN','SUM','AVG']


# this function holds all the query interface parts
# and runs them, interacting with the user to build a query and display the results with pymysql
def query_interface(conn,cur):

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
            return stmt
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
        else:
            return stmt 

    # this function builds the query's order by statement, if we have one
    def build_order_by():
        print()
        print('We will now build the order by clause of our query. \n')
            
        stmt = ''
        want_ordered = input('Would you like to order the results by any attributes? (y/n): ').strip().lower()
        if want_ordered=='y':
            stmt += 'ORDER BY '
            order_attrs = input('Please enter all attributes by which you would like to order the results, \n' +
                               'separated by spaces, in the order you would like them applied (for an aggregate function, match AGG(Attr) ): ').strip().split()
            for attr in order_attrs:
                if attr in attrs or aggy(attr):
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

    # this function checks whether an attribute looks like an aggregation over another attribute, so that we are able to order by aggregate functions of attrs
    def aggy(attr):
        agg = ''
        sub_attr = ''
        idx = 0
        for i in range(len(attr)):
            idx = i
            if attr[i]=='(':
                break
            agg += attr[i] 
        if agg.upper() not in aggregate_fns:
            return False
        for i in range(idx, len(attr)):
            if attr[i]==')':
                break
            sub_attr += attr[i]
        return sub_attr in attrs

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


    def query_main():

        welcome()
        select_stmt = build_select()
        # all selects will be from our single table that has all cars for sale and their attributes
        from_stmt = 'FROM CarsForSale'
        where_stmt = build_where()
        group_by_stmt,having_stmt,select_stmt = build_group_by_having(select_stmt)
        order_by_stmt = build_order_by()
        


        query = ''
        for stmt in [select_stmt, from_stmt, where_stmt, order_by_stmt, group_by_stmt, having_stmt]:
            if stmt:
                query += stmt + ' '

        try:
            cur.execute(query)
        except pymysql.err.InternalError as e :
            print(e)
            print()
            print(query)
            print()
            print("Uh-oh! Looks like that query doesn\'t work! Sorry... ")
            pass


        results = cur.fetchall()
        # print the results in a little bit cleaner of a way
        for result in results :
            st = ''
            for attr_val in result :
                st = st + str(attr_val) + ' : '
            print(st)


    query_main()

# this function gets the user's MySQL connection information
def get_connection():

    conn_host = ''
    conn_port = 0
    conn_user = ''
    conn_pass = ''
    conn_sock = ''
    conn_db   = ''
    conn_chrs = 'utf8'


    db_connection = input('Would you like to use Adam\'s, David\'s, or Ned\'s database connection \n' +
                          'or enter your own custom connection? \n' + 
                          'Type a for Adam, d for David, n for Ned, or c for custom: ').strip().lower()

    if db_connection=='d':
        conn_host = 'localhost'
        conn_port = 3306
        conn_user = 'root'
        conn_pass = 'lenneth6'
    elif db_connection=='a':
        conn_host = '127.0.0.1'
        conn_user = 'dbproject'
        conn_pass = 'cs327e'
        conn_sock = '/tmp/mysql.sock'
        conn_db   = 'mysql'
        conn_chrs = 'utf8'
    elif db_connection=='n':
        conn_host = '127.0.0.1'
        conn_user = 'dbproject'
        conn_pass = 'cs327e'
        conn_sock = '/tmp/mysql.sock'
        conn_db   = 'mysql'
        conn_chrs = 'utf8'
    # default to custom
    else:
        mp = input('Do you have a Mac or PC? (m/p): ').strip().lower()
        if mp=='m':
            conn_host = '127.0.0.1'
            conn_user = input('Please enter your username: ').strip()
            conn_pass = getpass.getpass(prompt='Please enter your password: ')
            conn_sock = input('Please enter your unix socket string: ').strip()
            conn_db   = 'mysql'
            conn_chrs = 'utf8'
        # default to pc
        else:
            conn_host = input('Please enter your host: ').strip()
            conn_port = int (input ('Please enter your port: ').strip() )
            conn_user = input('Please enter your username: ').strip()
            conn_pass = getpass.getpass(prompt='Please enter your password: ')
    # now create the connection based on the info we got
    if db_connection in ('a','n') or mp=='m':
        conn = pymysql.connect(host=conn_host, unix_socket=conn_sock, user=conn_user, passwd=conn_pass, db=conn_db, charset=conn_chrs)
    else:
        conn = pymysql.connect(host=conn_host, port=conn_port, user=conn_user, passwd=conn_pass)
    return conn 

# this function scrapes the Ranger Motors website for all the car info,
# then puts all the information in the database
def pipeline(conn,cur):

    # scrape all listing urls and returns a list of listing urls
    def get_list_of_listing_urls () : 
        
        inventory = urlopen('http://www.rangermotorsaustin.com/inventory/')
        soup_inventory = BeautifulSoup(inventory.read(), 'html.parser')

        listing_tags = soup_inventory.findAll('a', {'class':'inv-view-details'})
        listing_urls = []

        for tag in listing_tags :
            url = 'http://www.rangermotorsaustin.com' + tag.attrs['href']
            listing_urls.append(url)

        return listing_urls 

    # return dictionaries full of relevant data given a list of urls
    def get_list_of_dictionaries (urls) : 

        list_of_listing_dictionaries = []

        for url in urls :
            u = urlopen(url)
            soup_listing = BeautifulSoup(u.read(), 'html.parser')

            listing_dictionary = {}
            ul_listgroup_tag = soup_listing.find('ul', class_='list-group')
            li_listgroupitem_tags = ul_listgroup_tag.find_all('li', class_='list-group-item')
            li_listgroupitem_tags = li_listgroupitem_tags[:-1]

            for tag in li_listgroupitem_tags :
                span_tags = tag.find_all('span')
                key = span_tags[0].get_text().strip()
                val = span_tags[1].get_text().strip()
                listing_dictionary[key] = val

            price = soup_listing.find('span', {'class':'details-price'}).get_text()
            price = price.split()[2]
            price = price.strip().replace(',', '').replace('$', '')
            listing_dictionary['Price'] = price
            print('SCRAPED ' + listing_dictionary['Make'] + ' : ' + listing_dictionary['Model'])

            list_of_listing_dictionaries.append(listing_dictionary)

        return list_of_listing_dictionaries

    # fill in nulls for each dictionary and returns the modified list of dictionaries
    def fill_in_nulls (list_of_dictionaries) : 

        list_of_keys = ['Price', 'Year', 'Make', 'Model', 'Body style', 'Mileage', 'Transmission', 'Engine', 'Drivetrain', 'Exterior', 'Interior', 'Doors', 'Stock', 'VIN', 'Fuel Mileage', 'Conditon']

        for l in list_of_dictionaries :
            for k in list_of_keys :
                if not (k in l) :
                    l[k] = 'NULL'

        return list_of_dictionaries

    # change data types from string to integers where applicable and returns the modified list of dictionaries
    def fix_data_types(list_of_dictionaries) : 
        
        for l in list_of_dictionaries :
            if not (l['Doors'] == 'NULL') :
                l['Doors'] = l['Doors'][0]
            l['Mileage'] = l['Mileage'].replace(',', '')

        return list_of_dictionaries

    # create insert statement for each car and returns a list of insert statements
    def create_list_of_insert_statements (list_of_dictionaries, vins) : 
        list_of_insert_statements = []
        for l in list_of_dictionaries :
            b = False
            for v in vins :
                if l['VIN'] == v[0] :
                    b = True
            if not b :
            #       THIS IS WHERE YOU CHANGE THE TABLE INTO WHICH YOU INSERT RECORDS
                insert_statement = 'INSERT INTO CarsForSale SET '
                for key in l :
                    if key == 'Body style' :
                        insert_statement = insert_statement + 'Body_Style=("' + l[key] + '"), '
                    elif key == 'Fuel Mileage' :
                        insert_statement = insert_statement + 'Fuel_Mileage=("' + l[key] + '"), '
                    else :
                        if not (l[key] == 'NULL') :
                            insert_statement = insert_statement + key + '=("' + l[key] + '"), ' 
                insert_statement = insert_statement[:-2]
                list_of_insert_statements.append(insert_statement)

        return list_of_insert_statements

    urls = get_list_of_listing_urls()

    dictionaries = get_list_of_dictionaries(urls)
    dictionaries = fill_in_nulls(dictionaries)
    dictionaries = fix_data_types(dictionaries)


    # THIS IS WHERE YOU CHANGE THE DATABASE USED
    cur.execute('USE FunFriends33')

    # get all vins to check against
    cur.execute('select vin from CarsForSale')
    vins = cur.fetchall()

    insert_statements = create_list_of_insert_statements(dictionaries, vins)

    print('WRITE DATA INTO DATABASE')
    for ins_st in insert_statements :
        cur.execute(ins_st)

    conn.commit()

# this function creates the FunFriends33 Database if the user does not already have it
def create_db(conn,cur):
    have_db = False
    yn = '23'
    while yn not in ('y','n'): # make sure the user gives us a straight answer here, because a wrong answer will give a MySQL error
        yn = input('Have you already created a MySQL database entitled \'FunFriends33\' ? (y/n): ').strip().lower()
        if yn=='y':
            pass
            have_db = True
        elif yn=='n':
            cur.execute('CREATE DATABASE FunFriends33')
        cur.execute('USE FunFriends33')
    return have_db

# this function creates the CarsForSale table if the user doesn't have one yet
def create_table(conn,cur,already_has_db):
    yn = '23'
    if already_has_db:
        while yn not in ('y','n'): # make sure the user gives us a straight answer here, because a wrong answer will give a MySQL error
            yn = input('Have you already created a table entitled \'CarsForSale\' in your FunFriends33 database? (y/n): ').strip().lower()
    if yn=='y':
        pass
    elif yn=='n' or not already_has_db:
        cur.execute('''CREATE TABLE CarsForSale (
                        VIN varchar(30) primary key,
                        Price int,
                        Year year,
                        Make varchar(30),
                        Model varchar(30),
                        Body_Style varchar(30),
                        Mileage int,
                        Transmission varchar(30),
                        Engine varchar(30),
                        Drivetrain varchar(30),
                        Exterior varchar(30),
                        Interior varchar(30),
                        Doors int,
                        Stock varchar(30),
                        Fuel_Mileage varchar(30),
                        Conditon varchar(30))''')

        conn.commit()



def main():
    print()
    conn = get_connection()
    print()
    cur = conn.cursor()
    print()
    already_has_db = create_db(conn,cur)
    print()
    create_table(conn,cur,already_has_db)
    print()
    pipeline(conn,cur)
    print()
    query_interface(conn,cur)

    conn.close()
    cur.close()

main()



