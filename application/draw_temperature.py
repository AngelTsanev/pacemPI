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

     <title>{}</title>

       {}

    </head>""" .format(title, graph_script(table))
    return HTMLHead

# get data from the database
# if an interval is passed,
# return a list of records from the database
def get_data(interval):

    connection = sqlite3.connect(dbname)
    cursor = connection.cursor()

    if interval == None:
        cursor.execute("SELECT * FROM current_day")
    else:
        cursor.execute("SELECT * FROM  current_day WHERE timestamp>datetime('now', 'localtime', '-{} hours')".format(interval))
        
    rows = cursor.fetchall()

    connection.close()

    return rows
 

# convert rows from database into a javascript table
def create_table(rows):
    chart_table=""

    for row in rows[:-1]:
        row_string = "['{0}', {1}],\n".format(str(row[0]),str(row[1]))
        chart_table += row_string

    row = rows[-1]
    row_string = "['{0}', {1}]\n".format(str(row[0]),str(row[1]))
    chart_table += row_string

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
    <center><h2>Temperature Chart</h2></center>
    <div id="chart_div" style="width: 1350px; height: 750px;"></div>
    """
    return GRAPH



# connect to the db and show some stats
# argument option is the number of hours
def show_stats(option):

    connection = sqlite3.connect(dbname)
    cursor = connection.cursor()

    if option is None:
        option = str(24)

    cursor.execute("""SELECT timestamp, max(temperature) FROM  current_day WHERE 
    timestamp>datetime('now', 'localtime', '-%s hour') AND timestamp<=datetime('now', 'localtime')""" % option)
    data_max = cursor.fetchone()
    string_max = "{0}   {1}C".format(str(data_max[0]), "%.3f " % data_max[1])

    cursor.execute("""SELECT timestamp, min(temperature) FROM  current_day WHERE
    timestamp>datetime('now', 'localtime', '-%s hour') AND timestamp<=datetime('now', 'localtime')""" % option)
    data_min = cursor.fetchone()
    string_min = "{0}   {1}C".format(str(data_min[0]), "%.3f " % data_min[1])

    cursor.execute("""SELECT avg(temperature) FROM  current_day WHERE 
    timestamp>datetime('now', 'localtime', '-%s hour') AND timestamp<=datetime('now', 'localtime')""" % option)
    data_average = cursor.fetchone()
    
    STATS = """
    <hr>
    <center><h2>Minumum temperature</h2></center>
    <center>{0}</center>
    <center><h2>Maximum temperature</h2></center>
    <center>{1}</center>
    <center><h2>Average temperature</h2></center>
    <center>{2}</center>
    <hr>
    <center><h2>In the last hour:</h2></center>
    <center><table>
    <tr><td><strong>Date/Time</strong></td><td><strong>Temperature</strong></td></tr>""".format(string_min, string_max, "%.3f C" % data_average)

    cursor.execute("""SELECT * FROM current_day 
    WHERE timestamp>datetime('now', 'localtime', '-1 hour') AND timestamp<=datetime('now', 'localtime')""")
    rows = cursor.fetchall()
    print(rows)
    for row in rows:
        STATS += "\n<tr><td>{0}    </td><td>{1}C</td></tr>".format(str(row[0]), str(row[1]))
    
    STATS += "\n</table></center>"
    STATS += "\n<hr>"

    connection.close()
    return STATS




def time_selector():
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
        return """
        <html>
         <body bgcolor="#E6E6FA">
          <center><h1>PacemPI Temperature Logger</h1></center>
            {}
           <center>Sorry NO data found</center>
         </body>
        </html> """.format(time_selector())

    # start printing the page
    HTML += "\n<html>"
    # print the head section including the table
    # used by the javascript for the chart
    HTML += HTMLHead("PacemPI Temperature", table)

    # print the page body
    HTML += """
    <body bgcolor="#E6E6FA">
    <center><h1>PacemPI Temperature Logger</h1></center>
    <hr><center>"""
    HTML += time_selector()
    HTML += show_graph()
    HTML += show_stats(option)
    HTML += "</center>\n</body>"
    HTML += "\n</html>"
    sys.stdout.flush()
    return HTML
