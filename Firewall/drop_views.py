from router.models import *

import hashlib
import iptc

def insert_drop( data, token ):
    # drop needs to be insert into chain of which matches the forward rule

    # need to find forward entry
    try:
        forward_entry = ForwardEntry.objects.get( entry_id = data['ForwardEntry'], token_id = token )
    except ForwardEntry.DoesNotExist:
        raise ValueError("Cant Find Forward Entry")

    hashParams = hashlib.sha1("firewall" + data['data']['srcaddress'] + ":" + data['data']['srcport'] + ":" + \
                    data['data']['dstaddress'] + ":" + data['data']['dstport'] + ":" + data['data']['proto'] ).hexdigest()[0:20]

    if FirewallEntry.objects.filter( entry_id = hashParams, token = Token.objects.get( token_id = token ), forward = ForwardEntry.objects.get( entry_id = data['ForwardEntry'] ), dstaddress = data['data']['dstaddress'], dstport = data['data']['dstport'], srcaddress = data['data']['srcaddress'], srcport = data['data']['srcport'], proto =  data['data']['proto'], action = "DROP").exists():
        raise ValueError("Value Already Exists")

    FirewallEntry( entry_id = hashParams, token = Token.objects.get( token_id = token ), forward = ForwardEntry.objects.get( entry_id = data['ForwardEntry'] ), dstaddress = data['data']['dstaddress'], dstport = data['data']['dstport'], srcaddress = data['data']['srcaddress'], srcport = data['data']['srcport'], proto =  data['data']['proto'], action = "DROP").save()

    rule = iptc.Rule()
    rule.protocol = data['data']['proto']
    rule.src      = data['data']['srcaddress']
    rule.dst      = data['data']['dstaddress']
    rule.out_interface = "eth1"
    rule.create_match( data['data']['proto'] ).dport = data['data']['dstport']
    rule.create_match( data['data']['proto'] ).sport = data['data']['srcport']
    rule.create_target("DROP")

    iptc.Chain(iptc.Table(iptc.Table.FILTER), forward_entry.entry_id ).insert_rule( rule )

    return {'rule' : hashParams }
#endfunction
def get_drop( data, token):
    True
#endfunction
def delete_drop( data, token ):
    True
#endfunction
