from django.shortcuts import render
from django.http import HttpResponse


from Firewall.forward_views import *
from Firewall.allow_views import *
from Firewall.drop_views import *
from models import *

import re
import json

def v1FirewallRequest(request, token, action, address ):

    response = HttpResponse()

    actionlist = {
            "ALLOW" : {
                    "POST"   : insert_allow( address, request.body ),
                    "GET"    : get_allow   ( address, request.body ),
                    "DELETE" : delete_allow( address, request.body ),
                },

            "DROP" : {
                    "POST"   : insert_drop( address, request.body ),
                    "GET"    : get_drop   ( address, request.body ),
                    "DELETE" : delete_drop( address, request.body ),
                },
            "FORWARD" : {
                    "POST"   : insert_forward( address, request.body ),
                    "GET"    : get_forward   ( address, request.body ),
                    "DELETE" : delete_forward( address, request.body ),
                },
    }

    try:
        Token.objects.get(token_id = token )
    except Token.DoesNotExist:
        response.status_code = 401
        return response

    if not re.search('(POST|GET|DELETE)', request.method ):
        response.status_code = 402
        return response

    try:
        body = actionlist[ action ][ request.method ]
    except Exception as ex:
        response.status_code = 500
        return response

    response.body = formatJsonResponse(body)
    response.status_code = 200
    return response
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
