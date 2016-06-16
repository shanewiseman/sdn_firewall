from router.models import *
import iptc
import hashlib

def insert_forward( data, token):

    hashParams = hashlib.sha1("forward" + data['data']['srcaddress'] + ":" + data['data']['srcport'] + ":" + \
            data['data']['dstaddress'] + ":" + data['data']['dstport'] + ":" + data['data']['proto'] ).hexdigest()[0:20]

    #make sure we dont duplicate
    for chain in iptc.Table(iptc.Table.FILTER).chains:
        if chain.name == hashParams:
            raise ValueError("Chain Already Exists")


    # create the chain
    ForwardEntry(entry_id = hashParams, token = Token.objects.get( token_id = token ), dstaddress = data['data']['dstaddress'], dstport = data['data']['dstport'], srcaddress = data['data']['srcaddress'], srcport = data['data']['srcport'], proto =  data['data']['proto'], dsthost = data['data']['dsthost'] ).save()

    chain = iptc.Table( iptc.Table.FILTER ).create_chain( hashParams )

    #insert default
    rule = iptc.Rule()
    rule.in_interface = "eth0"
    rule.out_interface = "eth1"
    rule.create_target("DROP")
    chain.insert_rule( rule )

    #insert standard rules
    rule = iptc.Rule()

    rule.in_interface = "eth0"
    rule.out_interface = "eth1"
    rule.protocol = data['data']['proto']
    rule.create_match("tcp").dport = data['data']['dstport']
    rule.create_match("tcp").syn = ""
    rule.create_match("conntrack").ctstate = "NEW"
    rule.create_target("ACCEPT")

    iptc.Chain(iptc.Table(iptc.Table.FILTER), hashParams).insert_rule( rule )

    rule = iptc.Rule()

    rule.in_interface = "eth0"
    rule.out_interface = "eth1"
    rule.protocol = data['data']['proto']
    rule.create_match("tcp").dport = data['data']['dstport']
    rule.create_match("conntrack").ctstate = "ESTABLISHED,RELATED"
    rule.create_target("ACCEPT")

    iptc.Chain(iptc.Table(iptc.Table.FILTER), hashParams).insert_rule( rule )


    # create the nat rule
    rule = iptc.Rule()
    rule.protocol = data['data']['proto']
    rule.src      = data['data']['srcaddress']
    rule.dst      = data['data']['dstaddress']
    rule.in_interface = "eth0"
    rule.create_match("tcp").dport = data['data']['dstport']
    rule.create_match("tcp").sport = data['data']['srcport']
    rule.create_target('DNAT').to_destination = data['data']['dsthost']

    iptc.Chain(iptc.Table(iptc.Table.NAT), 'PREROUTING' ).insert_rule( rule )

    # create the foward rule
    rule = iptc.Rule()
    rule.protocol = data['data']['proto']
    rule.src      = data['data']['srcaddress']
    rule.dst      = data['data']['dsthost']

    #TODO These need to be abstracted
    rule.in_interface = "eth0"
    rule.out_interface = "eth1"

    rule.create_match("tcp").dport = data['data']['dstport']
    rule.create_match("tcp").sport = data['data']['srcport']
    rule.create_target( hashParams )

    iptc.Chain(iptc.Table(iptc.Table.FILTER), 'FORWARD' ).insert_rule( rule )

    return { 'forwarder' : hashParams }
#endfunction
def get_forward( data, token ):

    True
#endfunction
def delete_forward( data , token ):
    True
#endfunction
