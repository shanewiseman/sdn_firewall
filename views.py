from django.shortcuts import render
from django.http import HttpResponse


from Firewall.forward_views import *
from Firewall.allow_views import *
from Firewall.drop_views import *
from models import *

import re
import json

def v1FirewallRequest(request, token, action ):

    response = HttpResponse()

    actionlist = {
            "ALLOW" : {
                    "POST"   : insert_allow,
                    "GET"    : get_allow   ,
                    "DELETE" : delete_allow,
                },

            "DROP" : {
                    "POST"   : insert_drop,
                    "GET"    : get_drop   ,
                    "DELETE" : delete_drop,
                },
            "FORWARD" : {
                    "POST"   : insert_forward,
                    "GET"    : get_forward ,
                    "DELETE" : delete_forward,
                },
    }

    try:
        Token.objects.get(token_id = token )
    except Token.DoesNotExist:
        response.status_code = 401
        return response

    try:
        body = actionlist[ action ][ request.method ](json.loads(request.body), token )
    except Exception as ex:
        print ex
        response.status_code = 500
        return response

    except ValueError as ex:
        response.status_code = 400
        return response

    return HttpResponse(formatJsonResponse(body), content_type='application/json' )
#endfunction

def formatJsonResponse( data ):

    response = json.dumps( data )
    response = re.sub(r'\\','', response)
    response = re.sub(r'"\{','{', response)
    response = re.sub(r'\}"','}', response)
    response = re.sub(r'"\[','[', response)
    response = re.sub(r'\]"',']', response)
    response = re.sub(r'""','"', response)

    return response
