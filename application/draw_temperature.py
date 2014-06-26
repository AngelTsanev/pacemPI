import sqlite3
import sys
import cgi
import cgitb


# global variables
dbname='/home/pi/pacemPI/db.sqlite3'


# the HTML head section
# arguments are the page title and the table for the chart
def HTMLHead(title, table):
    HTMLHead = """
    <head>
     <link rel="icon" type="image/png"
       href="/static/favicon.ico">

     <title>
    {}
     </title>
    
    {}

    </head>""" .format(title, graph_script(table))
    return HTMLHead

# get data from the database
# if an interval is passed,
# return a list of records from the database
def get_data(interval):

    conn=sqlite3.connect(dbname)
    curs=conn.cursor()

    if interval == None:
        curs.execute("SELECT * FROM current_day")
    else:
        curs.execute("SELECT * FROM  current_day WHERE timestamp>datetime('now', 'localtime', '-{} hours')".format(interval))
        
    rows=curs.fetchall()

    conn.close()

    return rows
 

# convert rows from database into a javascript table
def create_table(rows):
    chart_table=""

    for row in rows[:-1]:
        rowstr="['{0}', {1}],\n".format(str(row[0]),str(row[1]))
        chart_table+=rowstr

    row=rows[-1]
    rowstr="['{0}', {1}]\n".format(str(row[0]),str(row[1]))
    chart_table+=rowstr

    return chart_table


# print the javascript to generate the chart
# pass the table generated from the database info
def graph_script(table):

    # google chart snippet
    chart_code="""
<script type="text/javascript" src="https://www.google.com/jsapi"></script>
<script type="text/javascript">
google.load("visualization", "1", {packages:["corechart"]});
google.setOnLoadCallback(drawChart);
function drawChart() {
var data = google.visualization.arrayToDataTable([
['Time', 'Temperature'],
%s
]);

var options = {
title: 'Temperature'
};

var chart = new google.visualization.LineChart(document.getElementById('chart_div'));
chart.draw(data, options);
}
</script>"""

    return (chart_code % (table))



# print the div that contains the graph
def show_graph():
    GRAPH = """
    <h2>Temperature Chart</h2>
    <div id="chart_div" style="width: 1350px; height: 750px;"></div>
    """
    return GRAPH



# connect to the db and show some stats
# argument option is the number of hours
def show_stats(option):

    conn=sqlite3.connect(dbname)
    curs=conn.cursor()

    if option is None:
        option = str(24)

    curs.execute("""SELECT timestamp, max(temperature) FROM  current_day WHERE 
    timestamp>datetime('now', 'localtime', '-%s hour') AND timestamp<=datetime('now', 'localtime')""" % option)
    rowmax=curs.fetchone()
    rowstrmax="{0}   {1}C".format(str(rowmax[0]), "%.3f " % rowmax[1])

    curs.execute("""SELECT timestamp, min(temperature) FROM  current_day WHERE
    timestamp>datetime('now', 'localtime', '-%s hour') AND timestamp<=datetime('now', 'localtime')""" % option)
    rowmin=curs.fetchone()
    rowstrmin="{0}   {1}C".format(str(rowmin[0]), "%.3f " % rowmin[1])

    curs.execute("""SELECT avg(temperature) FROM  current_day WHERE 
    timestamp>datetime('now', 'localtime', '-%s hour') AND timestamp<=datetime('now', 'localtime')""" % option)
    rowavg=curs.fetchone()
    
    STATS = """
    <hr>
    <h2>Minumum temperature</h2>
    {}
    <h2>Maximum temperature</h2>
    {}
    <h2>Average temperature</h2>
    {}
    <hr>
    <h2>In the last hour:</h2>
    <table>
    <tr><td><strong>Date/Time</strong></td><td><strong>Temperature</strong></td></tr>""".format(rowstrmin, rowstrmax, "%.3f C" % rowavg)

    curs.execute("""SELECT * FROM current_day 
    WHERE timestamp>datetime('now', 'localtime', '-1 hour') AND timestamp<=datetime('now', 'localtime')""")
    rows = curs.fetchall()
    print(rows)
    for row in rows:
        STATS += "\n<tr><td>{0}&emsp;&emsp;</td><td>{1}C</td></tr>".format(str(row[0]), str(row[1]))
    
    STATS += "\n</table>"
    STATS += "\n<hr>"

    conn.close()
    return STATS




def time_selector(option):
    TIME_SECTION = """
    <h3><center>Get log for the last :</center></h3>
    <center>
     <TABLE BORDER="0">
      <TR>
       <TD>
        <FORM METHOD="LINK" ACTION="/application/temperature/6">
         <INPUT TYPE="submit" VALUE="6 Hours">
        </FORM>
       </TD>

       <TD>
        <FORM METHOD="LINK" ACTION="/application/temperature/12">
         <INPUT TYPE="submit" VALUE="12 Hours">
        </FORM>
       </TD>

       <TD>
        <FORM METHOD="LINK" ACTION="/application/temperature/24">
         <INPUT TYPE="submit" VALUE="24 Hours">
        </FORM>
       </TD>
      </TR>
     </TABLE>
    </center> """     

    return TIME_SECTION


# check that the option is valid
# and not an SQL injection
def validate_input(option_str):
    # check that the option string represents a number
    if option_str.isalnum():
        # check that the option is within a specific range
        if int(option_str) > 0 and int(option_str) <= 24:
            return option_str
        else:
            return None
    else:
        return None


# main function
# This is where the program starts
def make_html(option):
    HTML = ""

    cgitb.enable()


    if option is None:
        option = str(24)

    # get data from the database
    records = get_data(option)

    if len(records) != 0:
        # convert the data into a table
        table = create_table(records)
    else:
        print("No data found")
        return

    # start printing the page
    HTML += "\n<html>"
    # print the head section including the table
    # used by the javascript for the chart
    HTML += HTMLHead("Temperature Logger", table)

    # print the page body
    HTML += "\n<body>"
    HTML += "\n<h1>Temperature Logger</h1>"
    HTML += "\n<hr>"
    HTML += time_selector(option)
    HTML += show_graph()
    HTML += show_stats(option)
    HTML += "\n</body>"
    HTML += "\n</html>"
    sys.stdout.flush()
    return HTML
