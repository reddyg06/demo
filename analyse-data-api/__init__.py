import logging 
import azure.functions as func
import json
import os
import sys
sys.path.append(os.path.abspath(""))
from SharedCode import analyse_data

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if not name:
        return func.HttpResponse(
             "Please pass a name on the query string or in the request body",
             status_code=400
        )
    
    try:
        with open('config_list.json') as f:
            datajson = json.load(f)
            print(datajson)
    except Exception as e:
        print('Error in loading json file')
        print(e)
        return_body = "<h3>Error while fetching config details !!!</h3>" + str(e)
        return func.HttpResponse(return_body,mimetype='text/html')

    # try:
    #     read_log = open(os.path.join(name + '.txt'), 'r').read()
    # except Exception as e:
    #     print(e)
    #     return_body = "<h3>Error while reading log file !!!</h3>" + str(e)
    #     return func.HttpResponse(return_body,mimetype='text/html')
        
    try:
        output = analyse_data.parse_data(datajson,name)
        print('OUTPUT')
        print(output)
        if output[0] == False:
            html_body = '<h1>Hurray!! No issues found</h1>'
            return func.HttpResponse(html_body,mimetype='text/html')
        else:
            html_body = ''
            for item in output[1].keys():
                html_body = html_body + '<h5>' + item + '</h5><table>'
                for i in output[1][item].keys():
                    html_body = html_body + '<tr><td>'+ i  + '</td><td>' + output[1][item][i] + '</td></tr>';
                html_body = html_body + '</table><br>'
            return func.HttpResponse(html_body,mimetype='text/html')
        return func.HttpResponse(output,mimetype='text/html')
    except Exception as e:
        return_body = "<h3>Error while parsing log file !!!</h3>" + str(e)
        return func.HttpResponse(return_body,mimetype='text/html')
