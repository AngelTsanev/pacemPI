import sqlite3
import sys
import cgi
import cgitb


# global variables
speriod=(15*60)-1
dbname='/home/pi/pacemPI/db.sqlite3'

#the HTTP header
def HTTPheader():
    return "Content-type: text/html\n\n"


# the HTML head section
# arguments are the page title and the table for the chart
def HTMLHead(title, table):
    HTMLHead = """
    <head>
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
        curs.execute("SELECT * FROM  current_day WHERE timestamp>datetime('now','-%s hours')" % interval)
        
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
    <div id="chart_div" style="width: 900px; height: 500px;"></div>
    """
    return GRAPH



# connect to the db and show some stats
# argument option is the number of hours
def show_stats(option):

    conn=sqlite3.connect(dbname)
    curs=conn.cursor()

    if option is None:
        option = str(24)

    curs.execute("SELECT timestamp,max(temperature) FROM  current_day WHERE timestamp>datetime('now','-%s hour') AND timestamp<=datetime('now')" % option)
    rowmax=curs.fetchone()
    rowstrmax="{0}&nbsp&nbsp&nbsp{1}C".format(str(rowmax[0]),str(rowmax[1]))

    curs.execute("SELECT timestamp,min(temperature) FROM  current_day WHERE timestamp>datetime('now','-%s hour') AND timestamp<=datetime('now')" % option)
    rowmin=curs.fetchone()
    rowstrmin="{0}&nbsp&nbsp&nbsp{1}C".format(str(rowmin[0]),str(rowmin[1]))

    curs.execute("SELECT avg(temperature) FROM  current_day WHERE timestamp>datetime('now','-%s hour') AND timestamp<=datetime('now')" % option)
    rowavg=curs.fetchone()

    STATS = """
    <hr>
    <h2>Minumum temperature&nbsp</h2>
    {}
    <h2>Maximum temperature</h2>
    {}
    <h2>Average temperature</h2>
    {}
    <hr>
    <h2>In the last hour:</h2>
    <table>
    <tr><td><strong>Date/Time</strong></td><td><strong>Temperature</strong></td></tr>""".format(
    rowstrmin, rowstrmax, "{}C".format(rowavg))

    rows=curs.execute("SELECT * FROM  current_day WHERE timestamp>datetime('new','-1 hour') AND timestamp<=datetime('new')")
    for row in rows:
        rowstr="\n<tr><td>{0}&emsp;&emsp;</td><td>{1}C</td></tr>".format(str(row[0]),str(row[1]))
        STATS += rowstr
    STATS += "</table>"
    STATS += "<hr>"

    conn.close()
    return STATS




def time_selector(option):
    TIME_SECTION ="""
    <form action="/cgi-bin/webgui.py" method="POST">
     Show the temperature logs for
    <select name="timeinterval">"""


    if option is not None:

        if option == "6":
            TIME_SECTION += "\n<option value=\"6\" selected=\"selected\">the last 6 hours</option>"
        else:
            TIME_SECTION += "\n<option value=\"6\">the last 6 hours</option>"

        if option == "12":
            TIME_SECTION += "\n<option value=\"12\" selected=\"selected\">the last 12 hours</option>"
        else:
            TIME_SECTION += "\n<option value=\"12\">the last 12 hours</option>"

        if option == "24":
            TIME_SECTION += "\n<option value=\"24\" selected=\"selected\">the last 24 hours</option>"
        else:
            TIME_SECTION += "\n<option value=\"24\">the last 24 hours</option>"

    else:
        TIME_SECTION += """
        <option value="6">the last 6 hours</option>
        <option value="12">the last 12 hours</option>
        <option value="24" selected="selected">the last 24 hours</option>
        """

    TIME_SECTION += """
     </select>
     <input type="submit" value="Display">
     </form>
    """
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


#return the option passed to the script
def get_option():
    form=cgi.FieldStorage()
    if "timeinterval" in form:
        option = form["timeinterval"].value
        return validate_input (option)
    else:
        return None




# main function
# This is where the program starts
def make_html():
    HTML = ""

    cgitb.enable()

    # get options that may have been passed to this script
    option=get_option()

    if option is None:
        option = str(24)

    # get data from the database
    records = get_data(option)

    # print the HTTP header
    #HTML += HTTPheader()

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
