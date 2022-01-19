#!/usr/bin/env python
'''The program read json file [input file] of network topology diagram, and write
out network definition jason file to [output file].
'''
import json


def usage(program_name):
    '''The func show how to use the program.'''
    print
    '''{0} ns [input file]
The program read json file [input file] of network topology diagram, and write
out nsfile .

{0} [input file] [output file]
The program read json file [input file] of network topology diagram, and write
out network definition json file to [output file].

{0} project [input file]
Product all project files at /proj/TEAM_NAME/EXP_NAME/, including vagrantfile,
bash scripts, etc.

{0} test
Self test.'''.format(program_name)


# from __future__ import print_function
ROUTER_TYPE = 'router'
CLOUD_TYPE = 'cloud_filled'
NODE_TYPE = 'asa'
EXP_NAME_TYPE = 'cloud_filled'

TYPE2OS = {"web_server": 'WIN10VM',
           "layer_3_switch": "WIN7VM",
           "workstation": "UBUNTUVM",
           "laptop": "KALIVM",
           ROUTER_TYPE: "UBUNTUVM",
           NODE_TYPE: '',
           CLOUD_TYPE: ''}

ROUTER_OS = "UBUNTUVM"
BOX_LIST = {"WIN10VM": "senglin/win-10-enterprise-vs2015community",
            'WIN7VM': "senglin/win-7-enterprise",
            'UBUNTUVM': "bento/ubuntu-16.04",
            'KALIVM': "kali.2018"}
MAX_NODE_NAME_LEN = 25


def validate_str(astr):
    '''The func validate if astr is a validate annotation.'''
    if len(astr) > MAX_NODE_NAME_LEN:
        return False
    import re
    if re.match("^[A-Za-z0-9_.-]*$", astr):
        return True
    return False


def validate_ip(astr):
    '''The func validate if astr is a validate IP address/validate IP address + " bridge".  '''
    alist = astr.split('.')
    if len(alist) != 4:
        return False
    for item in alist:
        if not item.isdigit():
            return False
        i = int(item)
        if i < 0 or i > 255:
            return False
    return True


def get_from_list_by_id(alist, aid):
    '''The func search in alist which include a list of dictionary
    with key 'aid' 's value is aid. '''
    for item in alist:
        if item['id'] == aid:
            return item
    return {}


def get_from_lan_by_id(lan_list, aid):
    '''The func find lan from lan_list by id. lan_list looks like
    [[[node_name, port_ip, port_id],[...]],[[...],[...]]].'''
    for lan in lan_list:
        for item in lan:
            if item[2] == aid:
                return lan
    return []


def add_connection2lan(lan_list, sitem, ditem):
    '''The func add a connection between sitem to ditem to lan_list by port_id.'''
    slan = get_from_lan_by_id(lan_list, sitem[2])
    tlan = get_from_lan_by_id(lan_list, ditem[2])
    if (slan == []) and (tlan == []):
        # create a new lan
        lan = []
        lan.append(sitem)
        lan.append(ditem)
        lan_list.append(lan)
    elif slan == []:
        # add source to tlan.
        tlan.append(sitem)
    elif tlan == []:
        slan.append(ditem)
    else:
        # combine slan and tlan.
        if slan != tlan:
            # If there already have just return, or combine.
            slan = slan + tlan
            lan_list.remove(tlan)
    return lan_list


def get_lans_from_lan_list(lan_list):
    '''The func convert from lan_list to LAN structure.'''
    lans = []
    for lan in lan_list:
        subnet = ''
        lan_def = {}
        for item in lan:
            node_name = item[0]['Name']
            node_ip = item[1]
            if node_ip == '':
                node_subnet = ''
                node_ip_last = ''
            else:
                node_subnet = node_ip[:node_ip.rfind('.') + 1]
                node_ip_last = node_ip[node_ip.rfind('.') + 1:]
            if lan_def == {}:
                # first node
                subnet = node_subnet
                lan_def['Subnet'] = subnet
                lan_def['LAN'] = []
                lan_def['LAN'].append([node_name, node_ip_last])
            elif subnet == node_subnet:
                lan_def['LAN'].append([node_name, node_ip_last])
            else:
                print
                "Error:Node[%s] connected with other nodes with " \
                "different subnet[%s].ConnectNodes[%s]." % \
                (node_name, node_subnet, str(lan))
                continue
        lans.append(lan_def)
    return lans


def vm_net_from_lan_list(vm_lan_list):
    '''The func handle vm network defination from vm_lan_list.'''
    VM_NET_NAME_PREFIX = 'VN'
    netnum = 0
    for lan in vm_lan_list:
        netnum += 1
        lan_def = {}
        for item in lan:
            vm_conf = item[0]
            nlist = item[1].split(';')
            nat_list = []
            ntype = ''
            port_ip = ''
            for npart in nlist:
                npart = npart.strip()
                if npart.startswith('NAT:'):
                    print
                    'vm_net_from_lan_list [%s]' % npart
                    nat_list.append(npart[4:].strip())
                    continue
                elif npart == 'NAT':
                    nat_list.append('')
                    continue
                # First part should be "IP[ bridge]"
                if npart.find('bridge') != -1:
                    ntype = 'bridge'
                    port_ip = npart[:npart.find('bridge')].strip()
                    if not validate_vm_bridge_ip(port_ip, vm_conf):
                        print
                        "Warn: VM[%s]'s bridge IP[%s] doesn't in the same " \
                        "subnet with node." % (vm_conf['Name'], port_ip)
                else:
                    port_ip = npart
                if (port_ip != '') and (not validate_ip(port_ip)):
                    print
                    "Error:" + "The port annotation [%s] should" \
                               " be IP address or IP+'bridge' for bridge mode." % \
                    (item[1])
                    continue
            net_conf = {}
            if port_ip != '':
                net_conf['IP'] = port_ip
            # test
            if len(vm_lan_list) == 1:
                ntype = 'internal'
                if port_ip == '':
                    # compatible to the old version, only one lan, use the manage network.
                    continue
            else:
                ntype = VM_NET_NAME_PREFIX + str(netnum)
            net_conf['NetType'] = ntype
            if nat_list != []:
                net_conf['NAT'] = nat_list
            if not vm_conf.has_key('Nets'):
                vm_conf['Nets'] = []
            else:
                # Have 2 networks, need forward.
                vm_conf['Forward'] = 1
            vm_conf['Nets'].append(net_conf)


def get_item_by_portid(alist, tid):
    '''The func get item from a list which have key ports include one port
    with id tid.'''
    for item in alist:
        for port in item['ports']:
            if port['id'] == tid:
                if port.has_key('IP'):
                    return item, port['IP']
                else:
                    return item, ''
    return {}, ''


def add_vm2node(vm_conf, node):
    '''The func add a vm_conf to node['VMs'].'''
    if vm_conf['connect2'] != {}:
        if vm_conf['connect2']['id'] == node['id']:
            # the same node. multi connection or the multi round.
            return
        print
        "Error:" + "VM is only allowed to connect to one " \
                   "node. VM[%s] connected with [%s] and [%s].\n" % \
        (vm_conf['Name'], vm_conf['connect2']['Name'], node["Name"])
        return
    vm_conf['connect2'] = node
    if not node.has_key('VMs'):
        node['VMs'] = []
    tmpvm = get_from_list_by_id(node['VMs'], vm_conf['id'])
    if tmpvm != {}:
        # Already added.
        print
        "Warning:Multi-connection between [%s] and [%s].\n" % \
        (tmpvm['Name'], node["Name"])
    else:
        node['VMs'].append(vm_conf)


def set_port_ip(tip, port_id, port_list):
    '''The func set ip to the port from the port_list.'''
    found = False
    for port in port_list:
        if port['id'] == port_id:
            port['IP'] = tip
            found = True
    if not found:
        print
        "Error:" + "JSON file corrupt? annotation[%s]for no port.\n" % tip


def handle_figure_annotation(figure):
    '''The func handle a figure's annotation part.'''
    name = ''
    for annotation in figure['annotations']:
        if annotation['text'] == '':
            continue
        if annotation['for'] == figure['id']:
            # annotation for the figure
            name = annotation['text']
        else:
            # annotation for port, should be IP
            vm_ip = annotation['text']
            # record to port
            set_port_ip(vm_ip, annotation['for'], figure['ports'])
    return name


def handle_annotation(annotation, conf):
    '''The func handle annotation which can have node_name;
    install.soft parameter; run: command; run:command; forward.'''
    nlist = annotation.split(';')
    conf["Name"] = ''
    cmd_list = []
    install_list = []
    for npart in nlist:
        npart = npart.strip()
        if npart.startswith('install.'):
            install_list.append(npart)
        elif npart.startswith('run:'):
            cmd_list.append(npart[4:].strip())
        elif npart.startswith('box:'):
            conf['OS'] = npart[4:].strip()
        elif npart.lower() == 'forward':
            conf['Forward'] = 1
        else:
            # name?
            if conf["Name"] == '':
                if not validate_str(npart):
                    print
                    "Error: Annotation[%s] only is allowed maxim %s char" \
                    "and only include alpha/number." % (npart, MAX_ANNOTATION_LEN)
                conf["Name"] = npart
            else:
                print
                "Error: can not recognize [%s] from annotation[%s]" % \
                (npart, annotation)
                print
                conf
    if cmd_list != []:
        conf['run'] = cmd_list
    if install_list != []:
        conf['install'] = install_list
    if conf["Name"] == '':
        print
        "Error:" + 'Every item [%s] need a name annotation.\n' % annotation
    return conf


def handle_exp_annotation(annotation):
    """The func handle experiment annotation which can have experiment name;
    reserve"""
    nlist = annotation.split(';')
    name = ''
    reserve_list = ''
    for npart in nlist:
        npart = npart.strip()
        if npart.startswith('reserve:'):
            reserve_list = npart[8:].strip()
        else:
            # name?
            if name == '':
                if not validate_str(npart):
                    print
                    "Error: Annotation[%s] only is allowed maxim %s char" \
                    "and only include alpha/number." % (npart, MAX_ANNOTATION_LEN)
                elif npart.endswith('.ncl.sg') and npart.count('.') == 3:
                    name = npart
                elif npart.count('.') == 1:
                    name = npart + '.ncl.sg'
                else:
                    print
                    "Error: experiment name[%s] should be experiment.team. annotation[%s]" % \
                    (npart, annotation)
            else:
                print
                "Error: cloud annotation can only have one experiment name [%s] from annotation[%s]" % (
                npart, annotation)
    return name, reserve_list


def get_item_from_draw(net_draw):
    '''The func identify all items(node, VM, Cloud) from the draw.'''
    vm_list = []
    node_list = []
    cloud_list = []
    exp_name = ''
    if not net_draw.has_key("figures"):
        print
        "Error:" + "Input file is corrupt for it doesn't have key 'figures'.\n"
        return [], [], [], ''
    for figure in net_draw['figures']:
        figure_id = figure['id']
        ftype = figure['subtype']
        conf = {}
        conf['id'] = figure_id
        conf['ports'] = figure['ports']  # temp save
        annotation = handle_figure_annotation(figure)
        if ftype == EXP_NAME_TYPE:
            # right now, we use CLOUD_TYPE, but use another name at future.
            exp_name = annotation
        if ftype == CLOUD_TYPE:
            cloud_list.append(conf)
            continue
        conf = handle_annotation(annotation, conf)
        if ftype == NODE_TYPE:
            if get_from_list_by_id(node_list, figure_id) == {}:
                # if not added, add it. For duplicate.
                node_list.append(conf)
        elif TYPE2OS.has_key(ftype):
            if get_from_list_by_id(vm_list, figure_id) == {}:
                # annotation may have set box?
                if not conf.has_key('OS'):
                    conf['OS'] = BOX_LIST[TYPE2OS[ftype]]
                conf['connect2'] = {}
                vm_list.append(conf)
        else:
            print
            "Error:" + "Unknown icon type [%s],please only use the following icons: %s" % \
            (ftype, str(TYPE2OS.keys()))
    return node_list, cloud_list, vm_list, exp_name


def connection_cloud2node(cloud_list, node_list):
    '''The func hanle connections from cloud to nodes.'''
    for cloud in cloud_list:
        for port in cloud['ports']:
            for connection in port['connections']:
                tid = connection['target']
                (node, tip) = get_item_by_portid(node_list, tid)
                if node == {}:
                    print
                    "Error: Cloud Icon can only connect to nodes. Only " \
                    "nodes can access the internet."
                    continue
                node['Type'] = 'Gateway'
                if tip != '':
                    print
                    "Warn: IP(%s) of the port connectted to cloud is " \
                    "unused for the IP is fixed and can not be changed." % tip


def validate_vm_bridge_ip(port_ip, vm_conf):
    '''The func validate vm_conf's bridge IP with node's IP. OK return true,
    or return false'''
    # bridge mode IP should have the same subnet to the node.
    if vm_conf['connect2'] != {}:
        node_conf = vm_conf['connect2']
        same_subnet = False
        for port in node_conf['ports']:
            if port.has_key('IP'):
                node_ip = port['IP']
                node_subnet = node_ip[:node_ip.rfind('.') + 1]
                subnet = port_ip[0:port_ip.rfind('.') + 1]
                if subnet == node_subnet:
                    same_subnet = True
        if not same_subnet:
            return False
    return True


def test_validate_vm_bridge_ip():
    '''The func test validate_vm_bridge_ip.'''
    vm_conf = {'connect2': {'ports': [{'IP': '172.16.10.5'}, {'IP': '172.16.4.4'}]}}
    assert validate_vm_bridge_ip('172.16.1.2', vm_conf) is False
    assert validate_vm_bridge_ip('172.16.4.2', vm_conf) is True


def handle_vm_port_ip(vm_conf, port):
    '''handle vm 's port IP definition. Add net into the VM only
    if have connection from VM 2 node. VM 2VM connection will be handled
    in vm_net_from_lan_list().'''
    if port.has_key('IP'):
        handle_vm_port_ip1(vm_conf, port['IP'])


def handle_vm_port_ip1(vm_conf, annotation):
    '''handle vm 's port IP definition. Add net into the VM.'''
    if annotation == '':
        return
    nlist = annotation.split(';')
    nat_list = []
    ntype = 'internal'
    port_ip = ''
    for npart in nlist:
        npart = npart.strip()
        if npart.startswith('NAT:'):
            nat_list.append(npart[4:].strip())
            continue
        elif npart == 'NAT':
            nat_list.append('')
            continue
        # First part should be "IP[ bridge]"
        if npart.find('bridge') != -1:
            ntype = 'bridge'
            port_ip = npart[:npart.find('bridge')].strip()
            if not validate_vm_bridge_ip(port_ip, vm_conf):
                print
                "Warn: VM[%s]'s bridge IP[%s] doesn't in the same " \
                "subnet with node." % (vm_conf['Name'], port_ip)
        else:
            port_ip = npart
    net_conf = {}
    if port_ip != '':
        if not validate_ip(port_ip):
            print
            "Error:" + "The port annotation [%s] should" \
                       " be IP address or IP+'bridge' for bridge mode." % \
            (port_ip)
            return
        net_conf['IP'] = port_ip
        # test
        net_conf['NetType'] = ntype
    if nat_list != []:
        net_conf['NAT'] = nat_list
    if net_conf != {}:
        if not vm_conf.has_key('Nets'):
            vm_conf['Nets'] = []
        else:
            # Have 2 networks, need forward.
            vm_conf['Forward'] = 1
        vm_conf['Nets'].append(net_conf)
    return vm_conf


def connection_node(node_list, vm_list, cloud_list):
    '''The func handle connections from nodes to other items.
    Return: possible subnet list.
    # all nodes with port connected each other will be in the same subnet.
    # every connection has two ports of two nodes. put two ports with node info
    # and other ports already connected to that port into the sam subnet.
    '''
    lan_list = []
    for node in node_list:
        for port in node['ports']:
            for connection in port['connections']:
                if port['id'] != connection['source']:
                    print
                    "Error:" + "Router[%s] port[%s] connection source[%s] is " \
                               "not port id.\n" % (node["Name"], port['id'], connection['source'])
                    continue
                tid = connection['target']
                (vm_conf, vm_ip) = get_item_by_portid(vm_list, tid)
                if vm_conf != {}:
                    # vm_conf connect to node.
                    add_vm2node(vm_conf, node)
                    handle_vm_port_ip1(vm_conf, vm_ip)
                    continue
                # connect to other node/router
                (tnode, tip) = get_item_by_portid(node_list, tid)
                if tnode != {}:
                    if port.has_key('IP'):
                        port_ip = port['IP']
                    else:
                        port_ip = ''
                    add_connection2lan(lan_list, [node, port_ip, port['id']],
                                       [tnode, tip, tid])
                    continue
                # connect to cloud?
                (cloud, _) = get_item_by_portid(cloud_list, tid)
                if cloud != {}:
                    node['Type'] = 'Gateway'
                else:
                    print
                    "Error: Node[%s]'s connection from id[%d] is not to" \
                    " node/vm/cloud." % (node["Name"], tid)
    return lan_list


def connect_vm2nodes(vm_list, node_list):
    '''The func handle connections from VMs to other items.'''
    vm_no_conect2 = 0
    for i in range(10):
        vm_no_conect2 = 0
        for conf in vm_list:
            for port in conf['ports']:
                for connection in port['connections']:
                    tid = connection['target']
                    # connect to node?
                    if (conf['connect2'] == {}):
                        (node, _) = get_item_by_portid(node_list, tid)
                        if node != {}:
                            add_vm2node(conf, node)
                            continue

                    # Connect to vm? allow vm - vm - node. After run one round ,it
                    # should have connect2.
                    (rvm, tip) = get_item_by_portid(vm_list, tid)
                    if rvm == {}:
                        continue
                    if rvm['connect2'] != {}:
                        if (conf['connect2'] == {}):
                            add_vm2node(conf, rvm['connect2'])
                    else:
                        if conf['connect2'] != {}:
                            # add rvm to node
                            add_vm2node(rvm, conf['connect2'])
                        else:
                            # 2vms connected but all did not connected to node?.
                            continue
                # handle ip after handle connections for we need vm's node to validate
                if conf['connect2'] == {}:
                    vm_no_conect2 += 1
        if vm_no_conect2 == 0:
            break
    return vm_no_conect2


def connection_vm(vm_list, node_list):
    '''The func handle connections from VMs to other items.'''
    vm_no_connect2 = connect_vm2nodes(vm_list, node_list)
    if vm_no_connect2 != 0:
        # not all vms connected to nodes?.
        print("Error:There are still %d VMs which do not connect to nodes or" \
              " too many net layers." % vm_no_connect2)
    vm_lan_list = []
    for conf in vm_list:
        name = conf['Name']
        for port in conf['ports']:
            port_id = port['id']

            for connection in port['connections']:
                if port_id != connection['source']:
                    print
                    "Error:" + "vm[%s] port[%s] connection source[%s] is not " \
                               "port id.\n" % (name, port_id, connection['source'])
                    continue
                tid = connection['target']
                # connect to node?
                (node, _) = get_item_by_portid(node_list, tid)
                if node != {}:
                    handle_vm_port_ip(conf, port)
                    continue

                # Connect to vm? allow vm - vm - node. After run one round ,it
                # should have connect2.
                (rvm, tip) = get_item_by_portid(vm_list, tid)
                if rvm == '':
                    print
                    "Error: VM[%s]'s connection from port id[%d] can " \
                    "only connect to node/vm." % (name, tid)
                    continue
                if port.has_key('IP'):
                    port_ip = port['IP']
                else:
                    port_ip = ''
                    print
                    'Warn: No IP at the port from VM[%s] to VM[%s]' % \
                    (name, rvm['Name'])
                add_connection2lan(vm_lan_list, [conf, port_ip, port_id],
                                   [rvm, tip, tid])

            # handle ip after handle connections for we need vm's node to validate
    return vm_lan_list


def draw2netdef(net_draw):
    '''The func transform the net_draw json def to network def jason.'''
    (node_list, cloud_list, vm_list, exp_anno) = get_item_from_draw(net_draw)
    # handle the connection between items.
    connection_cloud2node(cloud_list, node_list)

    lan_list = connection_node(node_list, vm_list, cloud_list)
    lans = get_lans_from_lan_list(lan_list)

    vm_lan_list = connection_vm(vm_list, node_list)
    vm_net_from_lan_list(vm_lan_list)
    # lans = get_lans_from_lan_list(vm_lan_list)

    # delete unused data.
    for node in node_list:
        del node['ports']
        del node['id']
    # "LANs":[{"Subnet":"172.16.20.", "LAN":[["n1","1"],["n2","2"],["n3","3"],
    # ["n4","4"],["n5","100"],["n6","6"]]},

    for vm_conf in vm_list:
        if vm_conf['connect2'] == {}:
            print
            "Error:" + "VM[%s] need connect to a router.\n" % (vm_conf['Name'])
        del vm_conf['connect2']
        del vm_conf['ports']
        del vm_conf['id']
    vnetwork = {}
    exp_name = ''
    reserve_list = ''
    if exp_anno != '':
        (exp_name, reserve_list) = handle_exp_annotation(exp_anno)
        vnetwork['ExperimentDomainName'] = exp_name
        if reserve_list != '':
            vnetwork['Reserve'] = reserve_list
    vnetwork['Nodes'] = node_list
    vnetwork['LANs'] = lans
    # handle annotation 's install.xxx;run:command .

    return vnetwork


def test_basic():
    '''The func test some basic func.'''
    assert validate_str('n1')
    assert validate_str('1')
    assert validate_str('abc.edf')
    assert validate_str('')
    assert not validate_str('n\1')
    assert not validate_str('n2345678901234567890123456')

    assert validate_ip("1.1.1.1")
    assert validate_ip("255.255.255.255")
    assert validate_ip("172.16.1.1")
    assert not validate_ip("abc")
    assert not validate_ip("1.1.1")

    alist = [{'id': '23'}, {'id': '25'}]
    assert get_from_list_by_id(alist, '1') == {}
    assert get_from_list_by_id(alist, '23') == {'id': '23'}
    # handle_annotation
    annotation = 'n1'
    assert handle_annotation(annotation, {}) == {'Name': 'n1'}
    assert handle_annotation('n1;install.web', {}) == {'Name': 'n1', 'install': ['install.web']}
    assert handle_annotation('n1;install.snort 172.16.3.2', {}) == \
           {'Name': 'n1', 'install': ['install.snort 172.16.3.2']}
    assert handle_annotation('n1;install.web; install.snort 172.16.3.2; run:ls', {}) == \
           {'Name': 'n1', 'install': ['install.web', 'install.snort 172.16.3.2'], 'run': ['ls']}
    assert handle_annotation('n1; run:ls; run: hostname', {}) == \
           {'Name': 'n1', 'run': ['ls', 'hostname']}
    assert handle_annotation('n1; box: my.box', {}) == \
           {'Name': 'n1', 'OS': 'my.box'}

    assert handle_annotation('n1; forward', {}) == \
           {'Name': 'n1', 'Forward': 1}

    # handle experiment annotation
    assert handle_exp_annotation('') == ('', '')
    assert handle_exp_annotation('exp.team') == ('exp.team.ncl.sg', '')
    assert handle_exp_annotation('exp.team.ncl.sg') == ('exp.team.ncl.sg', '')
    assert handle_exp_annotation('p1.exp.team') == ('', '')
    assert handle_exp_annotation('exp.team; reserve: pc18h, pc4a') == ('exp.team.ncl.sg', 'pc18h, pc4a')

    assert handle_vm_port_ip1({}, '172.16.1.2') == \
           {'Nets': [{'IP': '172.16.1.2', 'NetType': 'internal'}]}
    assert handle_vm_port_ip1({}, '172.16.1.2; NAT') == \
           {'Nets': [{'IP': '172.16.1.2', 'NetType': 'internal', 'NAT': ['']}]}
    assert handle_vm_port_ip1({}, '172.16.1.2; NAT: abc') == \
           {'Nets': [{'IP': '172.16.1.2', 'NetType': 'internal', 'NAT': ['abc']}]}
    assert handle_vm_port_ip1({}, '172.16.1.2; NAT: abc; NAT: efg') == \
           {'Nets': [{'IP': '172.16.1.2', 'NetType': 'internal', 'NAT': ['abc', 'efg']}]}


def test_lan():
    '''The func test lan related func.'''
    lan0 = []
    assert get_from_lan_by_id([], '1') == []
    assert get_from_lan_by_id([[]], '1') == []
    assert get_from_lan_by_id([[], []], '1') == []
    lan_list = add_connection2lan(lan0, [{'Name': 'name'}, "172.16.1.3", "3"],
                                  [{'Name': 'name'}, "172.16.1.2", "2"])
    assert lan_list == [[[{'Name': 'name'}, '172.16.1.3', '3'], [{'Name': 'name'}, '172.16.1.2', '2']]]
    assert get_lans_from_lan_list(lan0) == \
           [{'Subnet': '172.16.1.', 'LAN': [['name', '3'], ['name', '2']]}]
    assert add_connection2lan(lan0, [{'Name': 'name'}, "172.16.1.3", "3"],
                              [{'Name': 'name'}, "172.16.1.4", "4"]) == \
           [[[{'Name': 'name'}, '172.16.1.3', '3'], [{'Name': 'name'}, '172.16.1.2', '2'],
             [{'Name': 'name'}, '172.16.1.4', '4']]]
    assert get_lans_from_lan_list(lan0) == \
           [{'Subnet': '172.16.1.', 'LAN': [['name', '3'], ['name', '2'],
                                            ['name', '4']]}]
    assert add_connection2lan(lan0, [{'Name': 'name'}, "172.16.1.3", "3"],
                              [{'Name': 'name'}, "172.16.1.4", "4"]) == \
           [[[{'Name': 'name'}, '172.16.1.3', '3'], [{'Name': 'name'}, '172.16.1.2', '2'],
             [{'Name': 'name'}, '172.16.1.4', '4']]]

    lan = [[["name", "172.16.1.1", "1"]]]
    assert get_from_lan_by_id(lan, '1') == [["name", "172.16.1.1", "1"]]
    assert get_from_lan_by_id(lan, '2') == []
    assert get_lans_from_lan_list([]) == []

    # for no IP
    lan0 = []
    lan_list = add_connection2lan(lan0, [{'Name': "name1"}, "", "1"],
                                  [{'Name': "name2"}, "", "2"])
    assert lan_list == [[[{'Name': 'name1'}, '', '1'], [{'Name': 'name2'}, '', '2']]]
    assert get_lans_from_lan_list(lan0) == \
           [{'Subnet': '', 'LAN': [['name1', ''], ['name2', '']]}]
    lan_list = add_connection2lan(lan0, [{'Name': "name3"}, "", "3"],
                                  [{'Name': "name2"}, "", "2"])
    assert lan_list == [[[{'Name': 'name1'}, '', '1'], [{'Name': 'name2'}, '', '2'],
                         [{'Name': 'name3'}, '', '3']]]
    assert get_lans_from_lan_list(lan0) == \
           [{'Subnet': '', 'LAN': [['name1', ''], ['name2', ''], ['name3', '']]}]
    assert add_connection2lan(lan0, [{'Name': 'name2'}, "", "2"], [{'Name': 'name3'}, "", "3"]) == \
           [[[{'Name': 'name1'}, '', '1'], [{'Name': 'name2'}, '', '2'], [{'Name': 'name3'}, '', '3']]]


def test_link():
    node_list = [{'Name': 'n1', 'ports': [{'id': 'n1'}]}]
    vm_list = [
        {'Name': 'v1', 'id': 'v1', 'connect2': {}, 'ports': [{'id': 'v1p1', 'connections': [{'target': 'v2p1'}]}]},
        {'Name': 'v2', 'id': 'v2', 'connect2': {}, 'ports': [{'id': 'v2p1', 'connections': [{'target': 'v3p1'}]}]},
        {'Name': 'v3', 'id': 'v3', 'connect2': {}, 'ports': [{'id': 'v3p1', 'connections': [{'target': 'v4p1'}]}]},
        {'Name': 'v4', 'id': 'v4', 'connect2': {}, 'ports': [{'id': 'v4p1', 'connections': [{'target': 'v5p1'}]}]},
        {'Name': 'v5', 'id': 'v5', 'connect2': {}, 'ports': [{'id': 'v5p1', 'connections': [{'target': 'v6p1'}]}]},
        {'Name': 'v6', 'id': 'v6', 'connect2': {}, 'ports': [{'id': 'v6p1', 'connections': [{'target': 'v7p1'}]}]},
        {'Name': 'v7', 'id': 'v7', 'connect2': {}, 'ports': [{'id': 'v7p1', 'connections': [{'target': 'v8p1'}]}]},
        {'Name': 'v8', 'id': 'v8', 'connect2': {}, 'ports': [{'id': 'v8p1', 'connections': [{'target': 'n1'}]}]}]
    assert connect_vm2nodes(vm_list, node_list) == 0


def test():
    '''The func test all funcs.'''
    test_basic()
    test_lan()
    test_link()
    test_validate_vm_bridge_ip()
    netdef = draw2netdef({"figures": []})
    assert netdef == {"Nodes": [], "LANs": []}
    net_draw = {"figures": [{
        "subtype": "asa",
        "annotations": [{"text": "n1", "for": "QT4UuSgNnC"},
                        {"text": "172.16.1.2", "for": "H6kvJA7HZk"}],
        "id": "QT4UuSgNnC",
        "ports": [{"connections": [], "id": "CDPkfwlgse"},
                  {"connections": [], "id": "rHSmmbeoAB"},
                  {"connections": [], "id": "H6kvJA7HZk"},
                  {"connections": [], "id": "GTETCPM7ib"}]}]}
    netdef = draw2netdef(net_draw)
    # print str(netdef)
    # print str({"Nodes": [{"Name": "n1"}], "LANs": []})
    assert netdef == {"Nodes": [{"Name": "n1"}], "LANs": []}
    net_draw = {"figures": [
        {"subtype": "asa",
         "annotations": [{"text": "n1", "for": "QT4UuSgNnC", },
                         {"text": "172.16.1.2", "for": "owFLlO7zef", }],
         "id": "QT4UuSgNnC",
         "ports": [{
             "connections": [{"source": "owFLlO7zef", "target": "2QNt4T4xFT"}],
             "id": "owFLlO7zef"},
             {"connections": [], "id": "rHSmmbeoAB"},
             {"connections": [], "id": "H6kvJA7HZk"},
             {"connections": [], "id": "GTETCPM7ib"}]},
        {
            "subtype": "asa",
            "annotations": [{"text": "n2", "for": "QT4UuSgNnC1", },
                            {"text": "172.16.1.3", "for": "2QNt4T4xFT", }],
            "id": "QT4UuSgNnC1",
            "ports": [{"connections": [], "id": "2QNt4T4xFT"},
                      {"connections": [], "id": "rHSmmbeoAB"},
                      {"connections": [], "id": "H6kvJA7HZk"},
                      {"connections": [], "id": "GTETCPM7ib"}]}]}
    netdef = draw2netdef(net_draw)
    assert netdef == {"Nodes": [{"Name": "n1"}, {"Name": "n2"}],
                      "LANs": [{"Subnet": "172.16.1.",
                                "LAN": [["n1", "2"], ["n2", "3"]]}]}

    net_draw = {"figures": [
        {"id": "4onRN0sott", "type": "DiagramFigure", "subtype": "asa", "pic": "icons/asa.png", "x": 472, "y": 342,
         "width": 59, "height": 66, "ports": [
            {"connections": [{"source": "CXOEGoZk1E", "target": "5KkffMqtfC", "color": "128,128,255"}], "x": 0, "y": 33,
             "id": "CXOEGoZk1E"}, {"connections": [], "x": 29.5, "y": 0, "id": "ZPWm1bsTle"},
            {"connections": [], "x": 59, "y": 33, "id": "5xmlUfGKX1"},
            {"connections": [], "x": 29.5, "y": 66, "id": "7AiJDaOtTa"},
            {"connections": [], "x": 59, "y": 66, "id": "iMXMA5weDZ"},
            {"connections": [], "x": 0, "y": 66, "id": "T8zbzuDPsa"},
            {"connections": [], "x": 59, "y": 0, "id": "fekBNGnJ9o"},
            {"connections": [], "x": 0, "y": 0, "id": "pSctSd0hVR"}],
         "annotations": [{"text": "n1", "x": 473, "y": 413, "for": "4onRN0sott"}]},
        {"id": "0O0VITUXG4", "type": "DiagramFigure", "subtype": "cloud_filled", "pic": "icons/cloud_filled.png",
         "x": 642, "y": 345, "width": 84, "height": 56, "ports": [
            {"connections": [{"source": "Cl0CqB22cD", "target": "5xmlUfGKX1", "color": "128,128,255"}], "x": 0, "y": 28,
             "id": "Cl0CqB22cD"}, {"connections": [], "x": 42, "y": 0, "id": "JMAbzV4yqu"},
            {"connections": [], "x": 84, "y": 28, "id": "9p9T5GfL7K"},
            {"connections": [], "x": 42, "y": 56, "id": "NHg9JSOs4U"},
            {"connections": [], "x": 84, "y": 56, "id": "Mp6HWtwJtz"},
            {"connections": [], "x": 0, "y": 56, "id": "oRUzrZTqll"},
            {"connections": [], "x": 84, "y": 0, "id": "ofPz77ZIop"},
            {"connections": [], "x": 0, "y": 0, "id": "px5tWoH1ww"}],
         "annotations": [{"text": "exp.team", "x": 643, "y": 406, "for": "0O0VITUXG4"}]},
        {"id": "quEq5MLf8v", "type": "DiagramFigure", "subtype": "router", "pic": "icons/router.png", "x": 283,
         "y": 331, "width": 66, "height": 45, "ports": [{"connections": [], "x": 0, "y": 22.5, "id": "BLW5tQBTdf"},
                                                        {"connections": [], "x": 33, "y": 0, "id": "TENAonPT4P"},
                                                        {"connections": [], "x": 66, "y": 22.5, "id": "5KkffMqtfC"},
                                                        {"connections": [], "x": 33, "y": 45, "id": "0ozlNxRzdM"},
                                                        {"connections": [], "x": 66, "y": 45, "id": "3UsByDne5x"},
                                                        {"connections": [], "x": 0, "y": 45, "id": "wsMTmJ4LRM"},
                                                        {"connections": [], "x": 66, "y": 0, "id": "TUOUqfbp7R"},
                                                        {"connections": [], "x": 0, "y": 0, "id": "gvzmLuFmrC"}],
         "annotations": [{"text": "routern1; forward", "x": 284, "y": 381, "for": "quEq5MLf8v"},
                         {"text": "", "x": 349, "y": 353.5, "for": "5KkffMqtfC"}]}]}
    netdef = draw2netdef(net_draw)
    assert netdef == {
        "ExperimentDomainName": "exp.team.ncl.sg",
        "Nodes": [
            {
                "Name": "n1",
                "Type": "Gateway",
                "VMs": [
                    {
                        "Name": "routern1",
                        "OS": "bento/ubuntu-16.04",
                        "Forward": 1
                    }
                ]
            }
        ],
        "LANs": []
    }

    # n1--n2
    json_diagram = '{"figures":[{"id":"KR9mTZZDct", "type":"DiagramFigure", "subtype":"asa", "pic":"icons/asa.png", "x":623, "y":156, "width":59, "height":66, "ports":[{"connections":[], "x":0, "y":33, "id":"pJJBblgOwp"},{"connections":[], "x":29.5, "y":0, "id":"GuegVv1dQ3"},{"connections":[], "x":59, "y":33, "id":"Kxwoo0s9iV"},{"connections":[], "x":29.5, "y":66, "id":"HNngk6haeF"}], "annotations":[{"text":"n1", "x":624, "y":227, "for":"KR9mTZZDct"},{"text":"172.16.1.1", "x":652.5, "y":222, "for":"HNngk6haeF"}]},{"id":"xwqTVJipnc", "type":"DiagramFigure", "subtype":"asa", "pic":"icons/asa.png", "x":615, "y":343, "width":59, "height":66, "ports":[{"connections":[], "x":0, "y":33, "id":"8zopmOLvtH"},{"connections":[{"source":"IPe8wZ65HC", "target":"HNngk6haeF", "color":"128,128,255"}], "x":29.5, "y":0, "id":"IPe8wZ65HC"},{"connections":[], "x":59, "y":33, "id":"g9IenQmfvq"},{"connections":[], "x":29.5, "y":66, "id":"m7it0TWS80"}], "annotations":[{"text":"n2", "x":616, "y":414, "for":"xwqTVJipnc"},{"text":"172.16.1.2", "x":644.5, "y":343, "for":"IPe8wZ65HC"}]}]}'
    netdef = draw2netdef(json.loads(json_diagram))
    assert netdef == {"Nodes": [{"Name": "n1"}, {"Name": "n2"}],
                      "LANs": [{"Subnet": "172.16.1.",
                                "LAN": [["n2", "2"], ["n1", "1"]]}]}
    import vagrantfile
    vagrantfile.build_exp_nsfile(netdef)
    json_diagram = '{"figures":[{"id":"KR9mTZZDct", "type":"DiagramFigure", "subtype":"asa", "pic":"icons/asa.png", "x":627, "y":121, "width":59, "height":66, "ports":[{"connections":[], "x":0, "y":33, "id":"pJJBblgOwp"},{"connections":[], "x":29.5, "y":0, "id":"GuegVv1dQ3"},{"connections":[], "x":59, "y":33, "id":"Kxwoo0s9iV"},{"connections":[], "x":29.5, "y":66, "id":"HNngk6haeF"}], "annotations":[{"text":"n1", "x":628, "y":192, "for":"KR9mTZZDct"},{"text":"172.16.1.1", "x":656.5, "y":187, "for":"HNngk6haeF"}]},{"id":"xwqTVJipnc", "type":"DiagramFigure", "subtype":"asa", "pic":"icons/asa.png", "x":616, "y":339, "width":59, "height":66, "ports":[{"connections":[{"source":"8zopmOLvtH", "target":"gpDLDCGBr8", "color":"128,128,255"}], "x":0, "y":33, "id":"8zopmOLvtH"},{"connections":[{"source":"IPe8wZ65HC", "target":"HNngk6haeF", "color":"128,128,255"},{"source":"IPe8wZ65HC", "target":"vKxXhQV0zO", "color":"128,128,255"}], "x":29.5, "y":0, "id":"IPe8wZ65HC"},{"connections":[], "x":59, "y":33, "id":"g9IenQmfvq"},{"connections":[], "x":29.5, "y":66, "id":"m7it0TWS80"}], "annotations":[{"text":"n2", "x":617, "y":410, "for":"xwqTVJipnc"},{"text":"172.16.1.100", "x":645.5, "y":339, "for":"IPe8wZ65HC"},{"text":"172.16.2.100", "x":589, "y":382, "for":"8zopmOLvtH"}]},{"id":"aNu6wDfOoP", "type":"DiagramFigure", "subtype":"asa", "pic":"icons/asa.png", "x":385, "y":339, "width":59, "height":66, "ports":[{"connections":[{"source":"BV8RIauTwr", "target":"bOMTTmOemB", "color":"128,128,255"},{"source":"BV8RIauTwr", "target":"yy20iIn1mF", "color":"128,128,255"}], "x":0, "y":33, "id":"BV8RIauTwr"},{"connections":[], "x":29.5, "y":0, "id":"WmBZasF8s2"},{"connections":[], "x":59, "y":33, "id":"gpDLDCGBr8"},{"connections":[], "x":29.5, "y":66, "id":"EHcHn56sTP"}], "annotations":[{"text":"n3", "x":386, "y":410, "for":"aNu6wDfOoP"},{"text":"172.16.2.2", "x":444, "y":372, "for":"gpDLDCGBr8"},{"text":"172.16.3.100", "x":385, "y":339, "for":"BV8RIauTwr"}]},{"id":"JyZM2wzgnl", "type":"DiagramFigure", "subtype":"asa", "pic":"icons/asa.png", "x":428, "y":123, "width":59, "height":66, "ports":[{"connections":[], "x":0, "y":33, "id":"5EX3DWZc4G"},{"connections":[], "x":29.5, "y":0, "id":"874Lv4PuMH"},{"connections":[], "x":59, "y":33, "id":"piKtWDDbgr"},{"connections":[], "x":29.5, "y":66, "id":"vKxXhQV0zO"}], "annotations":[{"text":"n4", "x":429, "y":194, "for":"JyZM2wzgnl"},{"text":"172.16.1.3", "x":457.5, "y":189, "for":"vKxXhQV0zO"}]},{"id":"HFIlDJor6t", "type":"DiagramFigure", "subtype":"asa", "pic":"icons/asa.png", "x":204, "y":210, "width":59, "height":66, "ports":[{"connections":[], "x":0, "y":33, "id":"eq4lxtzEqa"},{"connections":[], "x":29.5, "y":0, "id":"qLMowD4wUh"},{"connections":[], "x":59, "y":33, "id":"FMtc9kTf1K"},{"connections":[], "x":29.5, "y":66, "id":"bOMTTmOemB"}], "annotations":[{"text":"n5", "x":205, "y":281, "for":"HFIlDJor6t"},{"text":"172.16.3.2", "x":233.5, "y":276, "for":"bOMTTmOemB"}]},{"id":"RmKmAlTvaP", "type":"DiagramFigure", "subtype":"asa", "pic":"icons/asa.png", "x":203, "y":464, "width":59, "height":66, "ports":[{"connections":[], "x":0, "y":33, "id":"xfTcESkXWn"},{"connections":[], "x":29.5, "y":0, "id":"yy20iIn1mF"},{"connections":[], "x":59, "y":33, "id":"xZBy9TT0iG"},{"connections":[], "x":29.5, "y":66, "id":"NBSzKG3A0U"}], "annotations":[{"text":"n6", "x":204, "y":535, "for":"RmKmAlTvaP"},{"text":"172.16.3.3", "x":232.5, "y":464, "for":"yy20iIn1mF"}]}]}'
    netdef = draw2netdef(json.loads(json_diagram))
    assert netdef == {"Nodes": [{"Name": "n1"}, {"Name": "n2"}, {"Name": "n3"},
                                {"Name": "n4"}, {"Name": "n5"}, {"Name": "n6"}],
                      "LANs": [{"Subnet": "172.16.2.",
                                "LAN": [["n2", "100"], ["n3", "2"]]},
                               {"Subnet": "172.16.1.",
                                "LAN": [["n2", "100"], ["n1", "1"],
                                        ["n4", "3"]]},
                               {"Subnet": "172.16.3.",
                                "LAN": [["n3", "100"], ["n5", "2"],
                                        ["n6", "3"]]}]}
    vagrantfile.build_exp_nsfile(netdef)
    # have duplicated nodes and no ip port
    json_diagram = '{"figures":[{"id":"KR9mTZZDct", "type":"DiagramFigure", "subtype":"asa", "pic":"icons/asa.png", "x":627, "y":121, "width":59, "height":66, "ports":[{"connections":[], "x":0, "y":33, "id":"pJJBblgOwp"},{"connections":[], "x":29.5, "y":0, "id":"GuegVv1dQ3"},{"connections":[], "x":59, "y":33, "id":"Kxwoo0s9iV"},{"connections":[], "x":29.5, "y":66, "id":"HNngk6haeF"}], "annotations":[{"text":"n1", "x":628, "y":192, "for":"KR9mTZZDct"},{"text":"172.16.1.1", "x":657, "y":187, "for":"HNngk6haeF"}]},{"id":"xwqTVJipnc", "type":"DiagramFigure", "subtype":"asa", "pic":"icons/asa.png", "x":616, "y":339, "width":59, "height":66, "ports":[{"connections":[{"source":"8zopmOLvtH", "target":"gpDLDCGBr8", "color":"128,128,255"}], "x":0, "y":33, "id":"8zopmOLvtH"},{"connections":[{"source":"IPe8wZ65HC", "target":"HNngk6haeF", "color":"128,128,255"},{"source":"IPe8wZ65HC", "target":"vKxXhQV0zO", "color":"128,128,255"}], "x":29.5, "y":0, "id":"IPe8wZ65HC"},{"connections":[], "x":59, "y":33, "id":"g9IenQmfvq"},{"connections":[], "x":29.5, "y":66, "id":"m7it0TWS80"}], "annotations":[{"text":"n2", "x":617, "y":410, "for":"xwqTVJipnc"},{"text":"172.16.1.100", "x":645.5, "y":339, "for":"IPe8wZ65HC"},{"text":"172.16.2.100", "x":589, "y":382, "for":"8zopmOLvtH"}]},{"id":"aNu6wDfOoP", "type":"DiagramFigure", "subtype":"asa", "pic":"icons/asa.png", "x":385, "y":339, "width":59, "height":66, "ports":[{"connections":[{"source":"BV8RIauTwr", "target":"bOMTTmOemB", "color":"128,128,255"},{"source":"BV8RIauTwr", "target":"yy20iIn1mF", "color":"128,128,255"}], "x":0, "y":33, "id":"BV8RIauTwr"},{"connections":[], "x":29.5, "y":0, "id":"WmBZasF8s2"},{"connections":[], "x":59, "y":33, "id":"gpDLDCGBr8"},{"connections":[{"source":"EHcHn56sTP", "target":"GH61GE37y7", "color":"128,128,255"}], "x":29.5, "y":66, "id":"EHcHn56sTP"}], "annotations":[{"text":"n3", "x":386, "y":410, "for":"aNu6wDfOoP"},{"text":"172.16.2.2", "x":444, "y":372, "for":"gpDLDCGBr8"},{"text":"172.16.3.100", "x":385, "y":339, "for":"BV8RIauTwr"},{"text":"", "x":414.5, "y":405, "for":"EHcHn56sTP"}]},{"id":"JyZM2wzgnl", "type":"DiagramFigure", "subtype":"asa", "pic":"icons/asa.png", "x":428, "y":123, "width":59, "height":66, "ports":[{"connections":[], "x":0, "y":33, "id":"5EX3DWZc4G"},{"connections":[], "x":29.5, "y":0, "id":"874Lv4PuMH"},{"connections":[], "x":59, "y":33, "id":"piKtWDDbgr"},{"connections":[], "x":29.5, "y":66, "id":"vKxXhQV0zO"}], "annotations":[{"text":"n4", "x":429, "y":194, "for":"JyZM2wzgnl"},{"text":"172.16.1.3", "x":457.5, "y":189, "for":"vKxXhQV0zO"}]},{"id":"HFIlDJor6t", "type":"DiagramFigure", "subtype":"asa", "pic":"icons/asa.png", "x":204, "y":210, "width":59, "height":66, "ports":[{"connections":[], "x":0, "y":33, "id":"eq4lxtzEqa"},{"connections":[], "x":29.5, "y":0, "id":"qLMowD4wUh"},{"connections":[], "x":59, "y":33, "id":"FMtc9kTf1K"},{"connections":[], "x":30, "y":65, "id":"bOMTTmOemB"}], "annotations":[{"text":"n5", "x":205, "y":281, "for":"HFIlDJor6t"},{"text":"172.16.3.2", "x":234, "y":275, "for":"bOMTTmOemB"},{"text":"", "x":263, "y":243, "for":"FMtc9kTf1K"}]},{"id":"RmKmAlTvaP", "type":"DiagramFigure", "subtype":"asa", "pic":"icons/asa.png", "x":203, "y":464, "width":59, "height":66, "ports":[{"connections":[], "x":0, "y":33, "id":"xfTcESkXWn"},{"connections":[], "x":29.5, "y":0, "id":"yy20iIn1mF"},{"connections":[], "x":59, "y":33, "id":"xZBy9TT0iG"},{"connections":[], "x":29.5, "y":66, "id":"NBSzKG3A0U"}], "annotations":[{"text":"n6", "x":204, "y":535, "for":"RmKmAlTvaP"},{"text":"172.16.3.3", "x":232.5, "y":464, "for":"yy20iIn1mF"}]},{"id":"KR9mTZZDct", "type":"DiagramFigure", "subtype":"asa", "pic":"icons/asa.png", "x":627, "y":121, "width":59, "height":66, "ports":[{"connections":[], "x":0, "y":33, "id":"pJJBblgOwp"},{"connections":[], "x":29.5, "y":0, "id":"GuegVv1dQ3"},{"connections":[], "x":59, "y":33, "id":"Kxwoo0s9iV"},{"connections":[], "x":29.5, "y":66, "id":"HNngk6haeF"}], "annotations":[{"text":"n1", "x":628, "y":192, "for":"KR9mTZZDct"},{"text":"", "x":657, "y":187, "for":"HNngk6haeF"}]},{"id":"xwqTVJipnc", "type":"DiagramFigure", "subtype":"asa", "pic":"icons/asa.png", "x":616, "y":339, "width":59, "height":66, "ports":[{"connections":[{"source":"8zopmOLvtH", "target":"gpDLDCGBr8", "color":"128,128,255"}], "x":0, "y":33, "id":"8zopmOLvtH"},{"connections":[{"source":"IPe8wZ65HC", "target":"HNngk6haeF", "color":"128,128,255"},{"source":"IPe8wZ65HC", "target":"vKxXhQV0zO", "color":"128,128,255"}], "x":29.5, "y":0, "id":"IPe8wZ65HC"},{"connections":[], "x":59, "y":33, "id":"g9IenQmfvq"},{"connections":[], "x":29.5, "y":66, "id":"m7it0TWS80"}], "annotations":[{"text":"n2", "x":617, "y":410, "for":"xwqTVJipnc"},{"text":"", "x":645.5, "y":339, "for":"IPe8wZ65HC"},{"text":"172.16.2.100", "x":589, "y":382, "for":"8zopmOLvtH"}]},{"id":"aNu6wDfOoP", "type":"DiagramFigure", "subtype":"asa", "pic":"icons/asa.png", "x":385, "y":339, "width":59, "height":66, "ports":[{"connections":[{"source":"BV8RIauTwr", "target":"bOMTTmOemB", "color":"128,128,255"},{"source":"BV8RIauTwr", "target":"yy20iIn1mF", "color":"128,128,255"}], "x":0, "y":33, "id":"BV8RIauTwr"},{"connections":[], "x":29.5, "y":0, "id":"WmBZasF8s2"},{"connections":[], "x":59, "y":33, "id":"gpDLDCGBr8"},{"connections":[], "x":29.5, "y":66, "id":"EHcHn56sTP"}], "annotations":[{"text":"n3", "x":386, "y":410, "for":"aNu6wDfOoP"},{"text":"", "x":444, "y":372, "for":"gpDLDCGBr8"},{"text":"", "x":385, "y":339, "for":"BV8RIauTwr"},{"text":"", "x":414.5, "y":405, "for":"EHcHn56sTP"}]},{"id":"JyZM2wzgnl", "type":"DiagramFigure", "subtype":"asa", "pic":"icons/asa.png", "x":428, "y":123, "width":59, "height":66, "ports":[{"connections":[], "x":0, "y":33, "id":"5EX3DWZc4G"},{"connections":[], "x":29.5, "y":0, "id":"874Lv4PuMH"},{"connections":[], "x":59, "y":33, "id":"piKtWDDbgr"},{"connections":[], "x":29.5, "y":66, "id":"vKxXhQV0zO"}], "annotations":[{"text":"n4", "x":429, "y":194, "for":"JyZM2wzgnl"},{"text":"", "x":457.5, "y":189, "for":"vKxXhQV0zO"}]},{"id":"HFIlDJor6t", "type":"DiagramFigure", "subtype":"asa", "pic":"icons/asa.png", "x":204, "y":210, "width":59, "height":66, "ports":[{"connections":[], "x":0, "y":33, "id":"eq4lxtzEqa"},{"connections":[], "x":29.5, "y":0, "id":"qLMowD4wUh"},{"connections":[], "x":59, "y":33, "id":"FMtc9kTf1K"},{"connections":[], "x":30, "y":65, "id":"bOMTTmOemB"}], "annotations":[{"text":"n5", "x":205, "y":281, "for":"HFIlDJor6t"},{"text":"", "x":234, "y":275, "for":"bOMTTmOemB"},{"text":"", "x":263, "y":243, "for":"FMtc9kTf1K"}]},{"id":"RmKmAlTvaP", "type":"DiagramFigure", "subtype":"asa", "pic":"icons/asa.png", "x":203, "y":464, "width":59, "height":66, "ports":[{"connections":[], "x":0, "y":33, "id":"xfTcESkXWn"},{"connections":[], "x":29.5, "y":0, "id":"yy20iIn1mF"},{"connections":[], "x":59, "y":33, "id":"xZBy9TT0iG"},{"connections":[], "x":29.5, "y":66, "id":"NBSzKG3A0U"}], "annotations":[{"text":"n6", "x":204, "y":535, "for":"RmKmAlTvaP"},{"text":"", "x":232.5, "y":464, "for":"yy20iIn1mF"}]},{"id":"4gD3sCLHdh", "type":"DiagramFigure", "subtype":"asa", "pic":"icons/asa.png", "x":368, "y":537, "width":59, "height":66, "ports":[{"connections":[], "x":0, "y":33, "id":"RGSn6FIZTa"},{"connections":[], "x":29.5, "y":0, "id":"GH61GE37y7"},{"connections":[], "x":59, "y":33, "id":"CJaXUWqNbh"},{"connections":[], "x":29.5, "y":66, "id":"TpyxxFT6VF"}], "annotations":[{"text":"n7", "x":369, "y":608, "for":"4gD3sCLHdh"}]}]}'
    netdef = draw2netdef(json.loads(json_diagram))
    assert netdef == {
        "Nodes": [{"Name": "n1"}, {"Name": "n2"}, {"Name": "n3"},
                  {"Name": "n4"}, {"Name": "n5"}, {"Name": "n6"}, {"Name": "n7"}],
        "LANs": [{"Subnet": "172.16.2.", "LAN": [["n2", "100"], ["n3", "2"]]},
                 {"Subnet": "172.16.1.",
                  "LAN": [["n2", "100"], ["n1", "1"], ["n4", "3"]]},
                 {"Subnet": "172.16.3.",
                  "LAN": [["n3", "100"], ["n5", "2"], ["n6", "3"]]},
                 {"Subnet": "",
                  "LAN": [["n3", ""], ["n7", ""]]}]}
    vagrantfile.build_exp_nsfile(netdef)

    # one node with 3 VMs with internet
    json_diagram = '{"figures":[{"id":"prvrLHUsst", "type":"DiagramFigure", "subtype":"web_server", "pic":"icons/web_server.png", "x":350, "y":564, "width":53, "height":55, "ports":[{"connections":[], "x":0, "y":27.5, "id":"eD1JupWal5"},{"connections":[{"source":"Zn8HfsSF8t", "target":"Ka3p7pqkpx", "color":"128,128,255"}], "x":26.5, "y":0, "id":"Zn8HfsSF8t"},{"connections":[], "x":53, "y":27.5, "id":"Ae3uhMU4KO"},{"connections":[], "x":26.5, "y":55, "id":"LzXz4DHJuS"}], "annotations":[{"text":"win10n1", "x":351, "y":624, "for":"prvrLHUsst"}]},{"id":"DQ21G2oHHb", "type":"DiagramFigure", "subtype":"workstation", "pic":"icons/workstation.png", "x":451, "y":562, "width":64, "height":53, "ports":[{"connections":[], "x":0, "y":26.5, "id":"gc6MWHf93v"},{"connections":[{"source":"0NIXTO0xfy", "target":"Ka3p7pqkpx", "color":"128,128,255"}], "x":32, "y":0, "id":"0NIXTO0xfy"},{"connections":[], "x":64, "y":26.5, "id":"eClmwIuic1"},{"connections":[], "x":32, "y":53, "id":"BeZ06lCRvO"}], "annotations":[{"text":"win10n1", "x":452, "y":620, "for":"DQ21G2oHHb"}]},{"id":"kKlSRtf6F7", "type":"DiagramFigure", "subtype":"laptop", "pic":"icons/laptop.png", "x":163, "y":560, "width":85, "height":64, "ports":[{"connections":[], "x":0, "y":32, "id":"uygzaablwq"},{"connections":[], "x":42.5, "y":0, "id":"rqKDQpEotw"},{"connections":[], "x":85, "y":32, "id":"Dmrb7SOcBo"},{"connections":[], "x":42.5, "y":64, "id":"lszVAuM35q"}], "annotations":[{"text":"kaililinuxn1", "x":164, "y":629, "for":"kKlSRtf6F7"}]},{"id":"54qh4xgF77", "type":"DiagramFigure", "subtype":"cloud_filled", "pic":"icons/cloud_filled.png", "x":543, "y":447, "width":84, "height":56, "ports":[{"connections":[{"source":"gB5Gmx1C3K", "target":"Q3ZT4ulnfp", "color":"128,128,255"}], "x":0, "y":28, "id":"gB5Gmx1C3K"},{"connections":[], "x":42, "y":0, "id":"mdoA7sbMKT"},{"connections":[], "x":84, "y":28, "id":"w0FbFTLw2m"},{"connections":[], "x":42, "y":56, "id":"hAwV0CFSKS"}], "annotations":[]},{"id":"Tba7FybRZh", "type":"DiagramFigure", "subtype":"asa", "pic":"icons/asa.png", "x":358, "y":442, "width":59, "height":66, "ports":[{"connections":[], "x":0, "y":33, "id":"1b9bx9kUSc"},{"connections":[], "x":29.5, "y":0, "id":"wzSWmDiPWZ"},{"connections":[], "x":59, "y":33, "id":"Q3ZT4ulnfp"},{"connections":[{"source":"Ka3p7pqkpx", "target":"rqKDQpEotw", "color":"128,128,255"}], "x":29.5, "y":66, "id":"Ka3p7pqkpx"}], "annotations":[{"text":"n1", "x":359, "y":513, "for":"Tba7FybRZh"}]}]}'

    netdef = draw2netdef(json.loads(json_diagram))
    assert netdef == {
        "Nodes": [
            {"Name": "n1", "Type": "Gateway",
             "VMs": [
                 {"Name": "kaililinuxn1", "OS": "kali.2018"},
                 {"Name": "win10n1",
                  "OS": "senglin/win-10-enterprise-vs2015community"},
                 {"Name": "win10n1", "OS": "bento/ubuntu-16.04"}]}], "LANs": []}

    json_diagram = '{"figures":[{"id":"prvrLHUsst", "type":"DiagramFigure", "subtype":"web_server", "pic":"icons/web_server.png", "x":345, "y":678, "width":53, "height":55, "ports":[{"connections":[], "x":0, "y":27.5, "id":"eD1JupWal5"},{"connections":[], "x":26.5, "y":0, "id":"Zn8HfsSF8t"},{"connections":[], "x":53, "y":27.5, "id":"Ae3uhMU4KO"},{"connections":[], "x":26.5, "y":55, "id":"LzXz4DHJuS"}], "annotations":[{"text":"win10n1", "x":346, "y":738, "for":"prvrLHUsst"}]},{"id":"DQ21G2oHHb", "type":"DiagramFigure", "subtype":"workstation", "pic":"icons/workstation.png", "x":355, "y":565, "width":64, "height":53, "ports":[{"connections":[], "x":0, "y":26.5, "id":"gc6MWHf93v"},{"connections":[{"source":"0NIXTO0xfy", "target":"Ka3p7pqkpx", "color":"128,128,255"}], "x":32, "y":0, "id":"0NIXTO0xfy"},{"connections":[], "x":64, "y":26.5, "id":"eClmwIuic1"},{"connections":[{"source":"BeZ06lCRvO", "target":"rqKDQpEotw", "color":"128,128,255"},{"source":"BeZ06lCRvO", "target":"Zn8HfsSF8t", "color":"128,128,255"}], "x":32, "y":53, "id":"BeZ06lCRvO"}], "annotations":[{"text":"routern1", "x":356, "y":623, "for":"DQ21G2oHHb"}]},{"id":"kKlSRtf6F7", "type":"DiagramFigure", "subtype":"laptop", "pic":"icons/laptop.png", "x":189, "y":678, "width":85, "height":64, "ports":[{"connections":[], "x":0, "y":32, "id":"uygzaablwq"},{"connections":[], "x":42.5, "y":0, "id":"rqKDQpEotw"},{"connections":[], "x":85, "y":32, "id":"Dmrb7SOcBo"},{"connections":[], "x":42.5, "y":64, "id":"lszVAuM35q"}], "annotations":[{"text":"kaililinuxn1", "x":190, "y":747, "for":"kKlSRtf6F7"}]},{"id":"54qh4xgF77", "type":"DiagramFigure", "subtype":"cloud_filled", "pic":"icons/cloud_filled.png", "x":543, "y":447, "width":84, "height":56, "ports":[{"connections":[{"source":"gB5Gmx1C3K", "target":"Q3ZT4ulnfp", "color":"128,128,255"}], "x":0, "y":28, "id":"gB5Gmx1C3K"},{"connections":[], "x":42, "y":0, "id":"mdoA7sbMKT"},{"connections":[], "x":84, "y":28, "id":"w0FbFTLw2m"},{"connections":[], "x":42, "y":56, "id":"hAwV0CFSKS"}], "annotations":[]},{"id":"Tba7FybRZh", "type":"DiagramFigure", "subtype":"asa", "pic":"icons/asa.png", "x":358, "y":442, "width":59, "height":66, "ports":[{"connections":[], "x":0, "y":33, "id":"1b9bx9kUSc"},{"connections":[], "x":29.5, "y":0, "id":"wzSWmDiPWZ"},{"connections":[], "x":59, "y":33, "id":"Q3ZT4ulnfp"},{"connections":[], "x":29.5, "y":66, "id":"Ka3p7pqkpx"}], "annotations":[{"text":"n1", "x":359, "y":513, "for":"Tba7FybRZh"}]},{"id":"S2i92ZuCmE", "type":"DiagramFigure", "subtype":"workstation", "pic":"icons/workstation.png", "x":446, "y":678, "width":64, "height":53, "ports":[{"connections":[], "x":0, "y":26.5, "id":"7M6mEQN7Uw"},{"connections":[{"source":"3yArcm4dlR", "target":"BeZ06lCRvO", "color":"128,128,255"}], "x":32, "y":0, "id":"3yArcm4dlR"},{"connections":[], "x":64, "y":26.5, "id":"yoKVowxXDy"},{"connections":[], "x":32, "y":53, "id":"58wIyzQAag"}], "annotations":[{"text":"ubuntu16n1", "x":447, "y":736, "for":"S2i92ZuCmE"}]}]}'

    netdef = draw2netdef(json.loads(json_diagram))
    assert netdef == {
        "Nodes": [{"Name": "n1", "Type": "Gateway",
                   "VMs": [
                       {"Name": "routern1", "OS": "bento/ubuntu-16.04"},
                       {"Name": "kaililinuxn1", "OS": "kali.2018"},
                       {"Name": "win10n1",
                        "OS": "senglin/win-10-enterprise-vs2015community"},
                       {"Name": "ubuntu16n1", "OS": "bento/ubuntu-16.04"}]}], "LANs": []}

    assert vagrantfile.build_exp_nsfile(netdef) == '''set ns [new Simulator]
source tb_compat.tcl

# Set node.
set n1 [$ns node]
tb-set-node-os $n1 Ubuntu16.04.3-amd64

# Set LAN.

# Set node ip.

# Go!
$ns run
'''
    # with IP and bridged network.
    json_diagram = '{"figures":[{"id":"prvrLHUsst", "type":"DiagramFigure", "subtype":"web_server", "pic":"icons/web_server.png", "x":345, "y":678, "width":53, "height":55, "ports":[{"connections":[], "x":0, "y":27.5, "id":"eD1JupWal5"},{"connections":[], "x":26.5, "y":0, "id":"Zn8HfsSF8t"},{"connections":[], "x":53, "y":27.5, "id":"Ae3uhMU4KO"},{"connections":[], "x":26.5, "y":55, "id":"LzXz4DHJuS"}], "annotations":[{"text":"win10n1", "x":346, "y":738, "for":"prvrLHUsst"},{"text":"172.16.1.3", "x":371.5, "y":678, "for":"Zn8HfsSF8t"}]},{"id":"DQ21G2oHHb", "type":"DiagramFigure", "subtype":"workstation", "pic":"icons/workstation.png", "x":355, "y":565, "width":64, "height":53, "ports":[{"connections":[], "x":0, "y":26.5, "id":"gc6MWHf93v"},{"connections":[{"source":"0NIXTO0xfy", "target":"Ka3p7pqkpx", "color":"128,128,255"}], "x":32, "y":0, "id":"0NIXTO0xfy"},{"connections":[], "x":64, "y":26.5, "id":"eClmwIuic1"},{"connections":[{"source":"BeZ06lCRvO", "target":"rqKDQpEotw", "color":"128,128,255"},{"source":"BeZ06lCRvO", "target":"Zn8HfsSF8t", "color":"128,128,255"}], "x":32, "y":53, "id":"BeZ06lCRvO"}], "annotations":[{"text":"routern1", "x":356, "y":623, "for":"DQ21G2oHHb"},{"text":"172.16.1.100", "x":387, "y":618, "for":"BeZ06lCRvO"},{"text":"172.16.10.2 bridge", "x":387, "y":565, "for":"0NIXTO0xfy"}]},{"id":"kKlSRtf6F7", "type":"DiagramFigure", "subtype":"laptop", "pic":"icons/laptop.png", "x":189, "y":678, "width":85, "height":64, "ports":[{"connections":[], "x":0, "y":32, "id":"uygzaablwq"},{"connections":[], "x":42.5, "y":0, "id":"rqKDQpEotw"},{"connections":[], "x":85, "y":32, "id":"Dmrb7SOcBo"},{"connections":[], "x":42.5, "y":64, "id":"lszVAuM35q"}], "annotations":[{"text":"kaililinuxn1", "x":190, "y":747, "for":"kKlSRtf6F7"},{"text":"172.16.1.2", "x":231.5, "y":678, "for":"rqKDQpEotw"}]},{"id":"54qh4xgF77", "type":"DiagramFigure", "subtype":"cloud_filled", "pic":"icons/cloud_filled.png", "x":543, "y":447, "width":84, "height":56, "ports":[{"connections":[{"source":"gB5Gmx1C3K", "target":"Q3ZT4ulnfp", "color":"128,128,255"}], "x":0, "y":28, "id":"gB5Gmx1C3K"},{"connections":[], "x":42, "y":0, "id":"mdoA7sbMKT"},{"connections":[], "x":84, "y":28, "id":"w0FbFTLw2m"},{"connections":[], "x":42, "y":56, "id":"hAwV0CFSKS"}], "annotations":[]},{"id":"Tba7FybRZh", "type":"DiagramFigure", "subtype":"asa", "pic":"icons/asa.png", "x":358, "y":442, "width":59, "height":66, "ports":[{"connections":[{"source":"1b9bx9kUSc", "target":"grhT9cL4Zc", "color":"128,128,255"}], "x":0, "y":33, "id":"1b9bx9kUSc"},{"connections":[], "x":29.5, "y":0, "id":"wzSWmDiPWZ"},{"connections":[], "x":59, "y":33, "id":"Q3ZT4ulnfp"},{"connections":[], "x":29, "y":65, "id":"Ka3p7pqkpx"}], "annotations":[{"text":"n1", "x":359, "y":513, "for":"Tba7FybRZh"},{"text":"", "x":417, "y":475, "for":"Q3ZT4ulnfp"},{"text":"", "x":387, "y":507, "for":"Ka3p7pqkpx"},{"text":"172.16.4.100", "x":358, "y":442, "for":"1b9bx9kUSc"}]},{"id":"S2i92ZuCmE", "type":"DiagramFigure", "subtype":"workstation", "pic":"icons/workstation.png", "x":446, "y":678, "width":64, "height":53, "ports":[{"connections":[], "x":0, "y":26.5, "id":"7M6mEQN7Uw"},{"connections":[{"source":"3yArcm4dlR", "target":"BeZ06lCRvO", "color":"128,128,255"}], "x":32, "y":0, "id":"3yArcm4dlR"},{"connections":[], "x":64, "y":26.5, "id":"yoKVowxXDy"},{"connections":[], "x":32, "y":53, "id":"58wIyzQAag"}], "annotations":[{"text":"ubuntu16n1", "x":447, "y":736, "for":"S2i92ZuCmE"},{"text":"172.16.1.4", "x":478, "y":678, "for":"3yArcm4dlR"}]},{"id":"2TpTGL0mnk", "type":"DiagramFigure", "subtype":"asa", "pic":"icons/asa.png", "x":244, "y":272, "width":59, "height":66, "ports":[{"connections":[], "x":0, "y":33, "id":"T52eLQ07lS"},{"connections":[], "x":29.5, "y":0, "id":"PchEn139lK"},{"connections":[], "x":59, "y":33, "id":"3hRn5mE9PR"},{"connections":[], "x":29.5, "y":66, "id":"grhT9cL4Zc"}], "annotations":[{"text":"n2", "x":245, "y":343, "for":"2TpTGL0mnk"},{"text":"172.16.4.2", "x":273.5, "y":338, "for":"grhT9cL4Zc"}]}]}'
    netdef = draw2netdef(json.loads(json_diagram))
    assert netdef == {
        "Nodes": [
            {"Name": "n1", "Type": "Gateway",
             "VMs": [{"Name": "routern1", "OS": "bento/ubuntu-16.04",
                      "Forward": 1,
                      "Nets": [{"IP": "172.16.10.2", "NetType": "bridge"},
                               {"IP": "172.16.1.100", "NetType": "internal"}]},
                     {"Name": "kaililinuxn1", "OS": "kali.2018",
                      "Nets": [{"IP": "172.16.1.2", "NetType": "internal"}]},
                     {"Name": "win10n1",
                      "OS": "senglin/win-10-enterprise-vs2015community",
                      "Nets": [{"IP": "172.16.1.3", "NetType": "internal"}]},
                     {"Name": "ubuntu16n1", "OS": "bento/ubuntu-16.04",
                      "Nets": [{"IP": "172.16.1.4", "NetType": "internal"}]}]},
            {"Name": "n2"}],
        "LANs": [{"Subnet": "172.16.4.", "LAN": [["n1", "100"], ["n2", "2"]]}]}
    assert vagrantfile.build_exp_nsfile(netdef) == '''set ns [new Simulator]
source tb_compat.tcl

# Set node.
set n1 [$ns node]
tb-set-node-os $n1 Ubuntu16.04.3-amd64
set n2 [$ns node]
tb-set-node-os $n2 Ubuntu16.04.3-amd64

# Set LAN.
set lan0 [$ns make-lan "$n1 $n2" 10Gb 0ms]

# Set node ip.
tb-set-ip-lan $n1 $lan0 172.16.4.100
tb-set-ip-lan $n2 $lan0 172.16.4.2

# Set route and adjust configure.
$ns rtproto Static
tb-set-node-startcmd $n1 "/share/ven/bin/install2local.sh 172.16.4.100 > /tmp/install2local.log 2>&1"
tb-set-node-startcmd $n2 "/share/ven/bin/install2local.sh 172.16.4.100 > /tmp/install2local.log 2>&1"

# Go!
$ns run
'''
    json_diagram = '{"figures":[{"id":"prvrLHUsst", "type":"DiagramFigure", "subtype":"web_server", "pic":"icons/web_server.png", "x":345, "y":678, "width":53, "height":55, "ports":[{"connections":[], "x":0, "y":27.5, "id":"eD1JupWal5"},{"connections":[], "x":26.5, "y":0, "id":"Zn8HfsSF8t"},{"connections":[], "x":53, "y":27.5, "id":"Ae3uhMU4KO"},{"connections":[], "x":26.5, "y":55, "id":"LzXz4DHJuS"}], "annotations":[{"text":"win10n1", "x":346, "y":738, "for":"prvrLHUsst"},{"text":"172.16.1.3", "x":371.5, "y":678, "for":"Zn8HfsSF8t"}]},{"id":"DQ21G2oHHb", "type":"DiagramFigure", "subtype":"workstation", "pic":"icons/workstation.png", "x":355, "y":565, "width":64, "height":53, "ports":[{"connections":[], "x":0, "y":26.5, "id":"gc6MWHf93v"},{"connections":[{"source":"0NIXTO0xfy", "target":"Ka3p7pqkpx", "color":"128,128,255"}], "x":32, "y":0, "id":"0NIXTO0xfy"},{"connections":[], "x":64, "y":26.5, "id":"eClmwIuic1"},{"connections":[{"source":"BeZ06lCRvO", "target":"rqKDQpEotw", "color":"128,128,255"},{"source":"BeZ06lCRvO", "target":"Zn8HfsSF8t", "color":"128,128,255"}], "x":32, "y":53, "id":"BeZ06lCRvO"}], "annotations":[{"text":"routern1", "x":356, "y":623, "for":"DQ21G2oHHb"},{"text":"172.16.1.100", "x":387, "y":618, "for":"BeZ06lCRvO"},{"text":"172.16.10.2 bridge", "x":387, "y":565, "for":"0NIXTO0xfy"}]},{"id":"kKlSRtf6F7", "type":"DiagramFigure", "subtype":"laptop", "pic":"icons/laptop.png", "x":189, "y":678, "width":85, "height":64, "ports":[{"connections":[], "x":0, "y":32, "id":"uygzaablwq"},{"connections":[], "x":42.5, "y":0, "id":"rqKDQpEotw"},{"connections":[], "x":85, "y":32, "id":"Dmrb7SOcBo"},{"connections":[], "x":42.5, "y":64, "id":"lszVAuM35q"}], "annotations":[{"text":"kaililinuxn1", "x":190, "y":747, "for":"kKlSRtf6F7"},{"text":"172.16.1.2", "x":231.5, "y":678, "for":"rqKDQpEotw"}]},{"id":"54qh4xgF77", "type":"DiagramFigure", "subtype":"cloud_filled", "pic":"icons/cloud_filled.png", "x":543, "y":447, "width":84, "height":56, "ports":[{"connections":[{"source":"gB5Gmx1C3K", "target":"Q3ZT4ulnfp", "color":"128,128,255"}], "x":0, "y":28, "id":"gB5Gmx1C3K"},{"connections":[], "x":42, "y":0, "id":"mdoA7sbMKT"},{"connections":[], "x":84, "y":28, "id":"w0FbFTLw2m"},{"connections":[], "x":42, "y":56, "id":"hAwV0CFSKS"}], "annotations":[]},{"id":"Tba7FybRZh", "type":"DiagramFigure", "subtype":"asa", "pic":"icons/asa.png", "x":358, "y":442, "width":59, "height":66, "ports":[{"connections":[{"source":"1b9bx9kUSc", "target":"grhT9cL4Zc", "color":"128,128,255"}], "x":0, "y":33, "id":"1b9bx9kUSc"},{"connections":[], "x":29.5, "y":0, "id":"wzSWmDiPWZ"},{"connections":[], "x":59, "y":33, "id":"Q3ZT4ulnfp"},{"connections":[], "x":29, "y":65, "id":"Ka3p7pqkpx"}], "annotations":[{"text":"n1", "x":359, "y":513, "for":"Tba7FybRZh"},{"text":"", "x":417, "y":475, "for":"Q3ZT4ulnfp"},{"text":"", "x":387, "y":507, "for":"Ka3p7pqkpx"},{"text":"172.16.4.100", "x":358, "y":442, "for":"1b9bx9kUSc"}]},{"id":"S2i92ZuCmE", "type":"DiagramFigure", "subtype":"workstation", "pic":"icons/workstation.png", "x":446, "y":678, "width":64, "height":53, "ports":[{"connections":[], "x":0, "y":26.5, "id":"7M6mEQN7Uw"},{"connections":[{"source":"3yArcm4dlR", "target":"BeZ06lCRvO", "color":"128,128,255"}], "x":32, "y":0, "id":"3yArcm4dlR"},{"connections":[], "x":64, "y":26.5, "id":"yoKVowxXDy"},{"connections":[], "x":32, "y":53, "id":"58wIyzQAag"}], "annotations":[{"text":"ubuntu16n1", "x":447, "y":736, "for":"S2i92ZuCmE"},{"text":"172.16.1.4", "x":478, "y":678, "for":"3yArcm4dlR"}]},{"id":"2TpTGL0mnk", "type":"DiagramFigure", "subtype":"asa", "pic":"icons/asa.png", "x":244, "y":272, "width":59, "height":66, "ports":[{"connections":[], "x":0, "y":33, "id":"T52eLQ07lS"},{"connections":[], "x":29.5, "y":0, "id":"PchEn139lK"},{"connections":[], "x":59, "y":33, "id":"3hRn5mE9PR"},{"connections":[], "x":29.5, "y":66, "id":"grhT9cL4Zc"}], "annotations":[{"text":"n2", "x":245, "y":343, "for":"2TpTGL0mnk"},{"text":"172.16.4.2", "x":273.5, "y":338, "for":"grhT9cL4Zc"}]}]}'
    # bug: more one net def for router VM.
    # node -> VM
    net_draw = {"figures": [{
        "subtype": "router",
        "annotations": [{"text": "v1n1", "for": "v1n1"},
                        {"text": "172.16.1.3 bridge", "for": "v1n1p1"},
                        {"text": "172.16.2.100", "for": "v1n1p2"}],
        "id": "v1n1",
        "ports": [{"connections": [], "id": "v1n1p1"},
                  {"connections": [{"source": "v1n1p2", "target": "v2n1p1"}],
                   "id": "v1n1p2"},
                  {"connections": [], "id": "v1n1p3"},
                  {"connections": [], "id": "v1n1p4"}]}, {"subtype": "asa",
                                                          "annotations": [{"text": "n1", "for": "n1"},
                                                                          {"text": "172.16.1.2", "for": "n1p3"}],
                                                          "id": "n1",
                                                          "ports": [{"connections": [], "id": "n1p1"},
                                                                    {"connections": [
                                                                        {"source": "n1p2", "target": "v1n1p1"}],
                                                                     "id": "n1p2"},
                                                                    {"connections": [], "id": "n1p3"},
                                                                    {"connections": [], "id": "n1p4"}]}, {
        "subtype": "workstation",
        "annotations": [{"text": "v2n1", "for": "v2n1"},
                        {"text": "172.16.2.2", "for": "v2n1p1"}],
        "id": "v2n1",
        "ports": [{"connections": [], "id": "v2n1p1"},
                  {"connections": [], "id": "v2n1p2"},
                  {"connections": [], "id": "v2n1p3"},
                  {"connections": [], "id": "v2n1p4"}]}]}
    netdef = draw2netdef(net_draw)
    assert netdef == {'Nodes': [
        {'Name': 'n1', 'VMs': [{'Name': 'v1n1', 'OS': 'bento/ubuntu-16.04',
                                'Forward': 1, 'Nets': [{'IP': '172.16.1.3', 'NetType': 'bridge'},
                                                       {'IP': '172.16.2.100', 'NetType': 'internal'}]},
                               {'Name': 'v2n1', 'OS': 'bento/ubuntu-16.04', 'Nets': [
                                   {'IP': '172.16.2.2', 'NetType': 'internal'}]}]}], 'LANs': []}
    json_diagram = {"figures": [
        {"id": "lEfpZPDAcJ", "type": "DiagramFigure", "subtype": "asa", "pic": "icons/asa.png", "x": 981, "y": 298,
         "width": 59, "height": 66, "ports": [
            {"connections": [{"source": "TzLzMdBsVm", "target": "dCQykgLqKM", "color": "128,128,255"}], "x": 0, "y": 33,
             "id": "TzLzMdBsVm"}, {"connections": [], "x": 29.5, "y": 0, "id": "K0qJfIPe7I"},
            {"connections": [], "x": 59, "y": 33, "id": "VPNWWLfPJf"},
            {"connections": [], "x": 29.5, "y": 66, "id": "c9IXpXDFQ0"}],
         "annotations": [{"text": "n1", "x": 982, "y": 369, "for": "lEfpZPDAcJ"}]},
        {"id": "AIbVnDVrVC", "type": "DiagramFigure", "subtype": "cloud_filled", "pic": "icons/cloud_filled.png",
         "x": 1112, "y": 303, "width": 84, "height": 56, "ports": [
            {"connections": [{"source": "SwdUa2ZF3p", "target": "VPNWWLfPJf", "color": "128,128,255"}], "x": 0, "y": 28,
             "id": "SwdUa2ZF3p"}, {"connections": [], "x": 42, "y": 0, "id": "8XwVq6tcZe"},
            {"connections": [], "x": 84, "y": 28, "id": "u83rLhZAZJ"},
            {"connections": [], "x": 42, "y": 56, "id": "JcmIX58xv0"}],
         "annotations": [{"text": "e1.teamname", "x": 1113, "y": 364, "for": "AIbVnDVrVC"}]},
        {"id": "waSTPwlodp", "type": "DiagramFigure", "subtype": "web_server", "pic": "icons/web_server.png", "x": 467,
         "y": 249, "width": 53, "height": 55, "ports": [{"connections": [], "x": 0, "y": 27.5, "id": "waC24D9HMF"},
                                                        {"connections": [], "x": 26.5, "y": 0, "id": "kbPPhzawpr"},
                                                        {"connections": [], "x": 53, "y": 27.5, "id": "KvfzIPL1yF"},
                                                        {"connections": [], "x": 26.5, "y": 55, "id": "NKxLHWaVmP"}],
         "annotations": [{"text": "win10", "x": 468, "y": 309, "for": "waSTPwlodp"},
                         {"text": "172.16.1.2", "x": 520, "y": 276.5, "for": "KvfzIPL1yF"}]},
        {"id": "AkbPLVpc4r", "type": "DiagramFigure", "subtype": "workstation", "pic": "icons/workstation.png",
         "x": 455, "y": 344, "width": 64, "height": 53,
         "ports": [{"connections": [], "x": 0, "y": 26.5, "id": "DhaDHbG63n"},
                   {"connections": [], "x": 32, "y": 0, "id": "h4k2uhH4LG"},
                   {"connections": [], "x": 64, "y": 26.5, "id": "SfbuEm5U3Z"},
                   {"connections": [], "x": 32, "y": 53, "id": "XgrMfguCLx"}],
         "annotations": [{"text": "ubuntu", "x": 456, "y": 402, "for": "AkbPLVpc4r"},
                         {"text": "172.16.1.3", "x": 519, "y": 370.5, "for": "SfbuEm5U3Z"}]},
        {"id": "3IIAhJS92D", "type": "DiagramFigure", "subtype": "workstation", "pic": "icons/workstation.png",
         "x": 633, "y": 504, "width": 64, "height": 53,
         "ports": [{"connections": [], "x": 0, "y": 26.5, "id": "sy76SdLSqB"},
                   {"connections": [], "x": 32, "y": 0, "id": "JLFU7ZdP7P"},
                   {"connections": [], "x": 64, "y": 26.5, "id": "lmILTLbFGq"},
                   {"connections": [], "x": 32, "y": 53, "id": "B0AprTpMTO"}],
         "annotations": [{"text": "db; install.db", "x": 634, "y": 562, "for": "3IIAhJS92D"},
                         {"text": "172.16.3.2", "x": 665, "y": 504, "for": "JLFU7ZdP7P"}]},
        {"id": "5rbdmr84Q0", "type": "DiagramFigure", "subtype": "workstation", "pic": "icons/workstation.png",
         "x": 762, "y": 505, "width": 64, "height": 53,
         "ports": [{"connections": [], "x": 0, "y": 26.5, "id": "p1l5PSKmzI"},
                   {"connections": [], "x": 32, "y": 0, "id": "khu8TurK0L"},
                   {"connections": [], "x": 64, "y": 26.5, "id": "S4pJe89i0d"},
                   {"connections": [], "x": 32, "y": 53, "id": "TMlV4xKdpq"}],
         "annotations": [{"text": "siem; install.splunk", "x": 763, "y": 563, "for": "5rbdmr84Q0"},
                         {"text": "172.16.3.3", "x": 794, "y": 505, "for": "khu8TurK0L"}]},
        {"id": "eCnmGlXr2t", "type": "DiagramFigure", "subtype": "workstation", "pic": "icons/workstation.png",
         "x": 592, "y": 108, "width": 64, "height": 53,
         "ports": [{"connections": [], "x": 0, "y": 26.5, "id": "ML8I5E7bAh"},
                   {"connections": [], "x": 32, "y": 0, "id": "aNhVmV58Ze"},
                   {"connections": [], "x": 64, "y": 26.5, "id": "22g6dRqTAA"},
                   {"connections": [], "x": 32, "y": 53, "id": "FXeMW4RIZQ"}],
         "annotations": [{"text": "web; install.web", "x": 593, "y": 166, "for": "eCnmGlXr2t"},
                         {"text": "172.16.2.2", "x": 624, "y": 161, "for": "FXeMW4RIZQ"}]},
        {"id": "Fdd4V6Qoyf", "type": "DiagramFigure", "subtype": "workstation", "pic": "icons/workstation.png",
         "x": 690, "y": 110, "width": 64, "height": 53,
         "ports": [{"connections": [], "x": 0, "y": 26.5, "id": "BEeeKQhvlM"},
                   {"connections": [], "x": 32, "y": 0, "id": "Bg6yRqsANB"},
                   {"connections": [], "x": 64, "y": 26.5, "id": "sWI6oW7kx0"},
                   {"connections": [], "x": 32, "y": 53, "id": "lxTUSJSm6D"}],
         "annotations": [{"text": "email", "x": 691, "y": 168, "for": "Fdd4V6Qoyf"},
                         {"text": "172.16.2.3", "x": 722, "y": 163, "for": "lxTUSJSm6D"}]},
        {"id": "q0lbQJLT6G", "type": "DiagramFigure", "subtype": "workstation", "pic": "icons/workstation.png",
         "x": 777, "y": 108, "width": 64, "height": 53,
         "ports": [{"connections": [], "x": 0, "y": 26.5, "id": "2Vp6MPP0Cn"},
                   {"connections": [], "x": 32, "y": 0, "id": "RlCnwlc7fT"},
                   {"connections": [], "x": 64, "y": 26.5, "id": "a9Z6cdqXHS"},
                   {"connections": [], "x": 32, "y": 53, "id": "7iDKoGfxyq"}],
         "annotations": [{"text": "dns", "x": 778, "y": 166, "for": "q0lbQJLT6G"},
                         {"text": "172.16.2.4", "x": 809, "y": 161, "for": "7iDKoGfxyq"}]},
        {"id": "zDFyeWPdmD", "type": "DiagramFigure", "subtype": "router", "pic": "icons/router.png", "x": 687,
         "y": 309, "width": 66, "height": 45, "ports": [{"connections": [
            {"source": "06Acbal21m", "target": "KvfzIPL1yF", "color": "128,128,255"},
            {"source": "06Acbal21m", "target": "SfbuEm5U3Z", "color": "128,128,255"}], "x": 0, "y": 22.5,
                                                         "id": "06Acbal21m"}, {"connections": [
            {"source": "Alun6vU20a", "target": "FXeMW4RIZQ", "color": "128,128,255"},
            {"source": "Alun6vU20a", "target": "lxTUSJSm6D", "color": "128,128,255"},
            {"source": "Alun6vU20a", "target": "7iDKoGfxyq", "color": "128,128,255"}], "x": 33, "y": 0,
                                                                               "id": "Alun6vU20a"}, {"connections": [
            {"source": "oPAUnksBvL", "target": "mL9v2Uyvo1", "color": "128,128,255"}], "x": 66, "y": 22.5,
                                                                                                     "id": "oPAUnksBvL"},
                                                        {"connections": [
                                                            {"source": "2KEiLTRGLR", "target": "JLFU7ZdP7P",
                                                             "color": "128,128,255"},
                                                            {"source": "2KEiLTRGLR", "target": "khu8TurK0L",
                                                             "color": "128,128,255"}], "x": 33, "y": 45,
                                                         "id": "2KEiLTRGLR"}],
         "annotations": [{"text": "gw; install.snort 172.16.3.3", "x": 688, "y": 359, "for": "zDFyeWPdmD"},
                         {"text": "172.16.1.100", "x": 636, "y": 344, "for": "06Acbal21m"},
                         {"text": "172.16.2.100", "x": 720, "y": 309, "for": "Alun6vU20a"},
                         {"text": "172.16.10.2", "x": 753, "y": 331.5, "for": "oPAUnksBvL"}]},
        {"id": "gLW5xKF2Oo", "type": "DiagramFigure", "subtype": "router", "pic": "icons/router.png", "x": 863,
         "y": 309, "width": 66, "height": 45, "ports": [{"connections": [], "x": 0, "y": 22.5, "id": "mL9v2Uyvo1"},
                                                        {"connections": [], "x": 33, "y": 0, "id": "P6RlbrJ9of"},
                                                        {"connections": [], "x": 66, "y": 22.5, "id": "dCQykgLqKM"},
                                                        {"connections": [], "x": 33, "y": 45, "id": "8fttHOi8xq"}],
         "annotations": [{"text": "172.16.10.100", "x": 863, "y": 309, "for": "mL9v2Uyvo1"},
                         {"text": "172.16.20.100", "x": 896, "y": 354, "for": "8fttHOi8xq"},
                         {"text": "gw2", "x": 864, "y": 359, "for": "gLW5xKF2Oo"}]},
        {"id": "cr9dnaTQdN", "type": "DiagramFigure", "subtype": "laptop", "pic": "icons/laptop.png", "x": 871,
         "y": 465, "width": 85, "height": 64, "ports": [{"connections": [], "x": 0, "y": 32, "id": "UACANDsxWL"}, {
            "connections": [{"source": "BSlivpgzWn", "target": "8fttHOi8xq", "color": "128,128,255"}], "x": 42.5,
            "y": 0, "id": "BSlivpgzWn"}, {"connections": [], "x": 85, "y": 32, "id": "RtJKoO7LO2"},
                                                        {"connections": [], "x": 42.5, "y": 64, "id": "OFfF9m3dlQ"}],
         "annotations": [{"text": "172.16.20.2", "x": 913.5, "y": 465, "for": "BSlivpgzWn"},
                         {"text": "kali", "x": 872, "y": 534, "for": "cr9dnaTQdN"}]}]}
    netdef = draw2netdef(json_diagram)
    assert netdef == \
           {'ExperimentDomainName': 'e1.teamname.ncl.sg', 'Nodes': [
               {'Name': 'n1', 'Type': 'Gateway',
                'VMs': [{'Name': 'gw2', 'OS': 'bento/ubuntu-16.04', 'Forward': 1,
                         'Nets': [{'IP': '172.16.10.100', 'NetType': 'VN3'},
                                  {'IP': '172.16.20.100', 'NetType': 'VN5'}]},
                        {'Name': 'gw', 'Nets': [{'IP': '172.16.1.100', 'NetType': 'VN1'},
                                                {'IP': '172.16.2.100', 'NetType': 'VN2'},
                                                {'IP': '172.16.10.2', 'NetType': 'VN3'},
                                                {'IP': '', 'NetType': 'VN4'}],
                         'install': ['install.snort 172.16.3.3'], 'Forward': 1, 'OS': 'bento/ubuntu-16.04'},
                        {'Name': 'db', 'Nets': [{'IP': '172.16.3.2', 'NetType': 'VN4'}],
                         'install': ['install.db'], 'OS': 'bento/ubuntu-16.04'},
                        {'Name': 'siem', 'Nets': [{'IP': '172.16.3.3', 'NetType': 'VN4'}],
                         'install': ['install.splunk'], 'OS': 'bento/ubuntu-16.04'},
                        {'Name': 'kali', 'OS': 'kali.2018',
                         'Nets': [{'IP': '172.16.20.2', 'NetType': 'VN5'}]},
                        {'Name': 'win10', 'OS': 'senglin/win-10-enterprise-vs2015community',
                         'Nets': [{'IP': '172.16.1.2', 'NetType': 'VN1'}]},
                        {'Name': 'ubuntu', 'OS': 'bento/ubuntu-16.04',
                         'Nets': [{'IP': '172.16.1.3', 'NetType': 'VN1'}]},
                        {'Name': 'web', 'Nets': [{'IP': '172.16.2.2', 'NetType': 'VN2'}],
                         'install': ['install.web'], 'OS': 'bento/ubuntu-16.04'},
                        {'Name': 'email', 'OS': 'bento/ubuntu-16.04',
                         'Nets': [{'IP': '172.16.2.3', 'NetType': 'VN2'}]},
                        {'Name': 'dns', 'OS': 'bento/ubuntu-16.04',
                         'Nets': [{'IP': '172.16.2.4', 'NetType': 'VN2'}]}]}],
            'LANs': []}

    json_diagram = {"figures": [
        {"id": "lEfpZPDAcJ", "type": "DiagramFigure", "subtype": "asa", "pic": "icons/asa.png", "x": 981, "y": 298,
         "width": 59, "height": 66, "ports": [
            {"connections": [{"source": "TzLzMdBsVm", "target": "dCQykgLqKM", "color": "128,128,255"}], "x": 0, "y": 33,
             "id": "TzLzMdBsVm"}, {"connections": [], "x": 29.5, "y": 0, "id": "K0qJfIPe7I"},
            {"connections": [], "x": 59, "y": 33, "id": "VPNWWLfPJf"},
            {"connections": [], "x": 29.5, "y": 66, "id": "c9IXpXDFQ0"}],
         "annotations": [{"text": "n1", "x": 982, "y": 369, "for": "lEfpZPDAcJ"}]},
        {"id": "AIbVnDVrVC", "type": "DiagramFigure", "subtype": "cloud_filled", "pic": "icons/cloud_filled.png",
         "x": 1112, "y": 303, "width": 84, "height": 56, "ports": [
            {"connections": [{"source": "SwdUa2ZF3p", "target": "VPNWWLfPJf", "color": "128,128,255"}], "x": 0, "y": 28,
             "id": "SwdUa2ZF3p"}, {"connections": [], "x": 42, "y": 0, "id": "8XwVq6tcZe"},
            {"connections": [], "x": 84, "y": 28, "id": "u83rLhZAZJ"},
            {"connections": [], "x": 42, "y": 56, "id": "JcmIX58xv0"}], "annotations": [
            {"text": "e1.teamname; reserve: pc3a, pc4b, pc17e, pc19d", "x": 1113, "y": 364, "for": "AIbVnDVrVC"}]},
        {"id": "waSTPwlodp", "type": "DiagramFigure", "subtype": "web_server", "pic": "icons/web_server.png", "x": 467,
         "y": 249, "width": 53, "height": 55, "ports": [{"connections": [], "x": 0, "y": 27.5, "id": "waC24D9HMF"},
                                                        {"connections": [], "x": 26.5, "y": 0, "id": "kbPPhzawpr"},
                                                        {"connections": [], "x": 53, "y": 27.5, "id": "KvfzIPL1yF"},
                                                        {"connections": [], "x": 26.5, "y": 55, "id": "NKxLHWaVmP"}],
         "annotations": [{"text": "win10", "x": 468, "y": 309, "for": "waSTPwlodp"},
                         {"text": "172.16.1.2", "x": 520, "y": 276.5, "for": "KvfzIPL1yF"}]},
        {"id": "AkbPLVpc4r", "type": "DiagramFigure", "subtype": "workstation", "pic": "icons/workstation.png",
         "x": 455, "y": 344, "width": 64, "height": 53,
         "ports": [{"connections": [], "x": 0, "y": 26.5, "id": "DhaDHbG63n"},
                   {"connections": [], "x": 32, "y": 0, "id": "h4k2uhH4LG"},
                   {"connections": [], "x": 64, "y": 26.5, "id": "SfbuEm5U3Z"},
                   {"connections": [], "x": 32, "y": 53, "id": "XgrMfguCLx"}],
         "annotations": [{"text": "ubuntu", "x": 456, "y": 402, "for": "AkbPLVpc4r"},
                         {"text": "172.16.1.3", "x": 519, "y": 370.5, "for": "SfbuEm5U3Z"}]},
        {"id": "3IIAhJS92D", "type": "DiagramFigure", "subtype": "workstation", "pic": "icons/workstation.png",
         "x": 633, "y": 504, "width": 64, "height": 53,
         "ports": [{"connections": [], "x": 0, "y": 26.5, "id": "sy76SdLSqB"},
                   {"connections": [], "x": 32, "y": 0, "id": "JLFU7ZdP7P"},
                   {"connections": [], "x": 64, "y": 26.5, "id": "lmILTLbFGq"},
                   {"connections": [], "x": 32, "y": 53, "id": "B0AprTpMTO"}],
         "annotations": [{"text": "db; install.db", "x": 634, "y": 562, "for": "3IIAhJS92D"},
                         {"text": "172.16.3.2", "x": 665, "y": 504, "for": "JLFU7ZdP7P"}]},
        {"id": "5rbdmr84Q0", "type": "DiagramFigure", "subtype": "workstation", "pic": "icons/workstation.png",
         "x": 762, "y": 505, "width": 64, "height": 53,
         "ports": [{"connections": [], "x": 0, "y": 26.5, "id": "p1l5PSKmzI"},
                   {"connections": [], "x": 32, "y": 0, "id": "khu8TurK0L"},
                   {"connections": [], "x": 64, "y": 26.5, "id": "S4pJe89i0d"},
                   {"connections": [], "x": 32, "y": 53, "id": "TMlV4xKdpq"}],
         "annotations": [{"text": "siem; install.splunk", "x": 763, "y": 563, "for": "5rbdmr84Q0"},
                         {"text": "172.16.3.3", "x": 794, "y": 505, "for": "khu8TurK0L"}]},
        {"id": "eCnmGlXr2t", "type": "DiagramFigure", "subtype": "workstation", "pic": "icons/workstation.png",
         "x": 592, "y": 108, "width": 64, "height": 53,
         "ports": [{"connections": [], "x": 0, "y": 26.5, "id": "ML8I5E7bAh"},
                   {"connections": [], "x": 32, "y": 0, "id": "aNhVmV58Ze"},
                   {"connections": [], "x": 64, "y": 26.5, "id": "22g6dRqTAA"},
                   {"connections": [], "x": 32, "y": 53, "id": "FXeMW4RIZQ"}],
         "annotations": [{"text": "web; install.web", "x": 593, "y": 166, "for": "eCnmGlXr2t"},
                         {"text": "172.16.2.2", "x": 624, "y": 161, "for": "FXeMW4RIZQ"}]},
        {"id": "Fdd4V6Qoyf", "type": "DiagramFigure", "subtype": "workstation", "pic": "icons/workstation.png",
         "x": 690, "y": 110, "width": 64, "height": 53,
         "ports": [{"connections": [], "x": 0, "y": 26.5, "id": "BEeeKQhvlM"},
                   {"connections": [], "x": 32, "y": 0, "id": "Bg6yRqsANB"},
                   {"connections": [], "x": 64, "y": 26.5, "id": "sWI6oW7kx0"},
                   {"connections": [], "x": 32, "y": 53, "id": "lxTUSJSm6D"}],
         "annotations": [{"text": "email", "x": 691, "y": 168, "for": "Fdd4V6Qoyf"},
                         {"text": "172.16.2.3", "x": 722, "y": 163, "for": "lxTUSJSm6D"}]},
        {"id": "q0lbQJLT6G", "type": "DiagramFigure", "subtype": "workstation", "pic": "icons/workstation.png",
         "x": 777, "y": 108, "width": 64, "height": 53,
         "ports": [{"connections": [], "x": 0, "y": 26.5, "id": "2Vp6MPP0Cn"},
                   {"connections": [], "x": 32, "y": 0, "id": "RlCnwlc7fT"},
                   {"connections": [], "x": 64, "y": 26.5, "id": "a9Z6cdqXHS"},
                   {"connections": [], "x": 32, "y": 53, "id": "7iDKoGfxyq"}],
         "annotations": [{"text": "dns", "x": 778, "y": 166, "for": "q0lbQJLT6G"},
                         {"text": "172.16.2.4", "x": 809, "y": 161, "for": "7iDKoGfxyq"}]},
        {"id": "zDFyeWPdmD", "type": "DiagramFigure", "subtype": "router", "pic": "icons/router.png", "x": 687,
         "y": 309, "width": 66, "height": 45, "ports": [{"connections": [
            {"source": "06Acbal21m", "target": "KvfzIPL1yF", "color": "128,128,255"},
            {"source": "06Acbal21m", "target": "SfbuEm5U3Z", "color": "128,128,255"}], "x": 0, "y": 22.5,
                                                         "id": "06Acbal21m"}, {"connections": [
            {"source": "Alun6vU20a", "target": "FXeMW4RIZQ", "color": "128,128,255"},
            {"source": "Alun6vU20a", "target": "lxTUSJSm6D", "color": "128,128,255"},
            {"source": "Alun6vU20a", "target": "7iDKoGfxyq", "color": "128,128,255"}], "x": 33, "y": 0,
                                                                               "id": "Alun6vU20a"}, {"connections": [
            {"source": "oPAUnksBvL", "target": "mL9v2Uyvo1", "color": "128,128,255"}], "x": 66, "y": 22.5,
                                                                                                     "id": "oPAUnksBvL"},
                                                        {"connections": [
                                                            {"source": "2KEiLTRGLR", "target": "JLFU7ZdP7P",
                                                             "color": "128,128,255"},
                                                            {"source": "2KEiLTRGLR", "target": "khu8TurK0L",
                                                             "color": "128,128,255"}], "x": 33, "y": 45,
                                                         "id": "2KEiLTRGLR"}],
         "annotations": [{"text": "gw; install.snort 172.16.3.3", "x": 688, "y": 359, "for": "zDFyeWPdmD"},
                         {"text": "172.16.1.100", "x": 636, "y": 344, "for": "06Acbal21m"},
                         {"text": "172.16.2.100", "x": 720, "y": 309, "for": "Alun6vU20a"},
                         {"text": "172.16.10.2", "x": 753, "y": 331.5, "for": "oPAUnksBvL"}]},
        {"id": "gLW5xKF2Oo", "type": "DiagramFigure", "subtype": "router", "pic": "icons/router.png", "x": 863,
         "y": 309, "width": 66, "height": 45, "ports": [{"connections": [], "x": 0, "y": 22.5, "id": "mL9v2Uyvo1"},
                                                        {"connections": [], "x": 33, "y": 0, "id": "P6RlbrJ9of"},
                                                        {"connections": [], "x": 66, "y": 22.5, "id": "dCQykgLqKM"},
                                                        {"connections": [], "x": 33, "y": 45, "id": "8fttHOi8xq"}],
         "annotations": [{"text": "172.16.10.100", "x": 863, "y": 309, "for": "mL9v2Uyvo1"},
                         {"text": "172.16.20.100", "x": 896, "y": 354, "for": "8fttHOi8xq"},
                         {"text": "gw2", "x": 864, "y": 359, "for": "gLW5xKF2Oo"}]},
        {"id": "cr9dnaTQdN", "type": "DiagramFigure", "subtype": "laptop", "pic": "icons/laptop.png", "x": 871,
         "y": 465, "width": 85, "height": 64, "ports": [{"connections": [], "x": 0, "y": 32, "id": "UACANDsxWL"}, {
            "connections": [{"source": "BSlivpgzWn", "target": "8fttHOi8xq", "color": "128,128,255"}], "x": 42.5,
            "y": 0, "id": "BSlivpgzWn"}, {"connections": [], "x": 85, "y": 32, "id": "RtJKoO7LO2"},
                                                        {"connections": [], "x": 42.5, "y": 64, "id": "OFfF9m3dlQ"}],
         "annotations": [{"text": "172.16.20.2", "x": 913.5, "y": 465, "for": "BSlivpgzWn"},
                         {"text": "kali", "x": 872, "y": 534, "for": "cr9dnaTQdN"}]}]}
    netdef = draw2netdef(json_diagram)
    assert netdef == \
           {'ExperimentDomainName': 'e1.teamname.ncl.sg', 'Nodes': [
               {'Name': 'n1', 'Type': 'Gateway',
                'VMs': [{'Name': 'gw2', 'OS': 'bento/ubuntu-16.04', 'Forward': 1,
                         'Nets': [{'IP': '172.16.10.100', 'NetType': 'VN3'},
                                  {'IP': '172.16.20.100', 'NetType': 'VN5'}]},
                        {'Name': 'gw', 'Nets': [{'IP': '172.16.1.100', 'NetType': 'VN1'},
                                                {'IP': '172.16.2.100', 'NetType': 'VN2'},
                                                {'IP': '172.16.10.2', 'NetType': 'VN3'},
                                                {'IP': '', 'NetType': 'VN4'}],
                         'install': ['install.snort 172.16.3.3'], 'Forward': 1, 'OS': 'bento/ubuntu-16.04'},
                        {'Name': 'db', 'Nets': [{'IP': '172.16.3.2', 'NetType': 'VN4'}],
                         'install': ['install.db'], 'OS': 'bento/ubuntu-16.04'},
                        {'Name': 'siem', 'Nets': [{'IP': '172.16.3.3', 'NetType': 'VN4'}],
                         'install': ['install.splunk'], 'OS': 'bento/ubuntu-16.04'},
                        {'Name': 'kali', 'OS': 'kali.2018',
                         'Nets': [{'IP': '172.16.20.2', 'NetType': 'VN5'}]},
                        {'Name': 'win10', 'OS': 'senglin/win-10-enterprise-vs2015community',
                         'Nets': [{'IP': '172.16.1.2', 'NetType': 'VN1'}]},
                        {'Name': 'ubuntu', 'OS': 'bento/ubuntu-16.04',
                         'Nets': [{'IP': '172.16.1.3', 'NetType': 'VN1'}]},
                        {'Name': 'web', 'Nets': [{'IP': '172.16.2.2', 'NetType': 'VN2'}],
                         'install': ['install.web'], 'OS': 'bento/ubuntu-16.04'},
                        {'Name': 'email', 'OS': 'bento/ubuntu-16.04',
                         'Nets': [{'IP': '172.16.2.3', 'NetType': 'VN2'}]},
                        {'Name': 'dns', 'OS': 'bento/ubuntu-16.04',
                         'Nets': [{'IP': '172.16.2.4', 'NetType': 'VN2'}]}]}],
            'LANs': [],
            'Reserve': 'pc3a, pc4b, pc17e, pc19d'}
    json_diagram = {"figures": [
        {"id": "lEfpZPDAcJ", "type": "DiagramFigure", "subtype": "asa", "pic": "icons/asa.png", "x": 981, "y": 298,
         "width": 59, "height": 66, "ports": [
            {"connections": [{"source": "TzLzMdBsVm", "target": "dCQykgLqKM", "color": "128,128,255"}], "x": 0, "y": 33,
             "id": "TzLzMdBsVm"}, {"connections": [], "x": 29.5, "y": 0, "id": "K0qJfIPe7I"},
            {"connections": [], "x": 59, "y": 33, "id": "VPNWWLfPJf"},
            {"connections": [], "x": 29.5, "y": 66, "id": "c9IXpXDFQ0"},
            {"connections": [], "x": 59, "y": 66, "id": "NAs5x4Dc24"},
            {"connections": [], "x": 0, "y": 66, "id": "cTJOe8wFBw"},
            {"connections": [], "x": 59, "y": 0, "id": "d5pW2VTtS7"},
            {"connections": [], "x": 0, "y": 0, "id": "wLC0yeFTVN"}],
         "annotations": [{"text": "n1", "x": 982, "y": 369, "for": "lEfpZPDAcJ"}]},
        {"id": "AIbVnDVrVC", "type": "DiagramFigure", "subtype": "cloud_filled", "pic": "icons/cloud_filled.png",
         "x": 1112, "y": 303, "width": 84, "height": 56, "ports": [
            {"connections": [{"source": "SwdUa2ZF3p", "target": "VPNWWLfPJf", "color": "128,128,255"}], "x": 0, "y": 28,
             "id": "SwdUa2ZF3p"}, {"connections": [], "x": 42, "y": 0, "id": "8XwVq6tcZe"},
            {"connections": [], "x": 84, "y": 28, "id": "u83rLhZAZJ"},
            {"connections": [], "x": 42, "y": 56, "id": "JcmIX58xv0"},
            {"connections": [], "x": 84, "y": 56, "id": "1JOhgwxk4e"},
            {"connections": [], "x": 0, "y": 56, "id": "mszJ7MuUlO"},
            {"connections": [], "x": 84, "y": 0, "id": "3xZ88pdeVb"},
            {"connections": [], "x": 0, "y": 0, "id": "sDGdQecmvP"}], "annotations": [
            {"text": "e1.teamname; reserve: pc3a, pc4b, pc17e, pc19d", "x": 1113, "y": 364, "for": "AIbVnDVrVC"}]},
        {"id": "waSTPwlodp", "type": "DiagramFigure", "subtype": "web_server", "pic": "icons/web_server.png", "x": 467,
         "y": 249, "width": 53, "height": 55, "ports": [{"connections": [], "x": 0, "y": 27.5, "id": "waC24D9HMF"},
                                                        {"connections": [], "x": 26.5, "y": 0, "id": "kbPPhzawpr"},
                                                        {"connections": [], "x": 53, "y": 27.5, "id": "KvfzIPL1yF"},
                                                        {"connections": [], "x": 26.5, "y": 55, "id": "NKxLHWaVmP"},
                                                        {"connections": [], "x": 53, "y": 55, "id": "Akv5SZoITk"},
                                                        {"connections": [], "x": 0, "y": 55, "id": "u8mT4sOmTt"},
                                                        {"connections": [], "x": 53, "y": 0, "id": "aK6cnsWWFs"},
                                                        {"connections": [], "x": 0, "y": 0, "id": "AMBTflAFTB"}],
         "annotations": [{"text": "win10", "x": 468, "y": 309, "for": "waSTPwlodp"},
                         {"text": "172.16.1.2", "x": 520, "y": 276.5, "for": "KvfzIPL1yF"}]},
        {"id": "AkbPLVpc4r", "type": "DiagramFigure", "subtype": "workstation", "pic": "icons/workstation.png",
         "x": 455, "y": 344, "width": 64, "height": 53,
         "ports": [{"connections": [], "x": 0, "y": 26.5, "id": "DhaDHbG63n"},
                   {"connections": [], "x": 32, "y": 0, "id": "h4k2uhH4LG"},
                   {"connections": [], "x": 64, "y": 26.5, "id": "SfbuEm5U3Z"},
                   {"connections": [], "x": 32, "y": 53, "id": "XgrMfguCLx"},
                   {"connections": [], "x": 64, "y": 53, "id": "5c8SIhbc1w"},
                   {"connections": [], "x": 0, "y": 53, "id": "NuIkT3ADR4"},
                   {"connections": [], "x": 64, "y": 0, "id": "yLZMwAKihG"},
                   {"connections": [], "x": 0, "y": 0, "id": "dnz8IqXW2I"}],
         "annotations": [{"text": "ubuntu", "x": 456, "y": 402, "for": "AkbPLVpc4r"},
                         {"text": "172.16.1.3", "x": 519, "y": 370.5, "for": "SfbuEm5U3Z"}]},
        {"id": "3IIAhJS92D", "type": "DiagramFigure", "subtype": "workstation", "pic": "icons/workstation.png",
         "x": 633, "y": 504, "width": 64, "height": 53,
         "ports": [{"connections": [], "x": 0, "y": 26.5, "id": "sy76SdLSqB"},
                   {"connections": [], "x": 32, "y": 0, "id": "JLFU7ZdP7P"},
                   {"connections": [], "x": 64, "y": 26.5, "id": "lmILTLbFGq"},
                   {"connections": [], "x": 32, "y": 53, "id": "B0AprTpMTO"},
                   {"connections": [], "x": 64, "y": 53, "id": "SuuvgyzB8q"},
                   {"connections": [], "x": 0, "y": 53, "id": "hTX8bB8FSc"},
                   {"connections": [], "x": 64, "y": 0, "id": "FHG6u5zyUi"},
                   {"connections": [], "x": 0, "y": 0, "id": "MqDH33yvot"}],
         "annotations": [{"text": "db; install.db", "x": 634, "y": 562, "for": "3IIAhJS92D"},
                         {"text": "172.16.3.2", "x": 665, "y": 504, "for": "JLFU7ZdP7P"}]},
        {"id": "5rbdmr84Q0", "type": "DiagramFigure", "subtype": "workstation", "pic": "icons/workstation.png",
         "x": 762, "y": 505, "width": 64, "height": 53,
         "ports": [{"connections": [], "x": 0, "y": 26.5, "id": "p1l5PSKmzI"},
                   {"connections": [], "x": 32, "y": 0, "id": "khu8TurK0L"},
                   {"connections": [], "x": 64, "y": 26.5, "id": "S4pJe89i0d"},
                   {"connections": [], "x": 32, "y": 53, "id": "TMlV4xKdpq"},
                   {"connections": [], "x": 64, "y": 53, "id": "RlOhqCSygb"},
                   {"connections": [], "x": 0, "y": 53, "id": "M7mmnGJhqM"},
                   {"connections": [], "x": 64, "y": 0, "id": "QVs0JpKk6h"},
                   {"connections": [], "x": 0, "y": 0, "id": "F2vVuuEmkT"}],
         "annotations": [{"text": "siem; install.splunk", "x": 763, "y": 563, "for": "5rbdmr84Q0"},
                         {"text": "172.16.3.3", "x": 794, "y": 505, "for": "khu8TurK0L"}]},
        {"id": "eCnmGlXr2t", "type": "DiagramFigure", "subtype": "workstation", "pic": "icons/workstation.png",
         "x": 592, "y": 108, "width": 64, "height": 53,
         "ports": [{"connections": [], "x": 0, "y": 26.5, "id": "ML8I5E7bAh"},
                   {"connections": [], "x": 32, "y": 0, "id": "aNhVmV58Ze"},
                   {"connections": [], "x": 64, "y": 26.5, "id": "22g6dRqTAA"},
                   {"connections": [], "x": 32, "y": 53, "id": "FXeMW4RIZQ"},
                   {"connections": [], "x": 64, "y": 53, "id": "EUk8kQOtVd"},
                   {"connections": [], "x": 0, "y": 53, "id": "sbaU8T7qhZ"},
                   {"connections": [], "x": 64, "y": 0, "id": "F1Tb1JFtoZ"},
                   {"connections": [], "x": 0, "y": 0, "id": "cw1UanAR2v"}],
         "annotations": [{"text": "web; install.web", "x": 593, "y": 166, "for": "eCnmGlXr2t"},
                         {"text": "172.16.2.2", "x": 624, "y": 161, "for": "FXeMW4RIZQ"}]},
        {"id": "Fdd4V6Qoyf", "type": "DiagramFigure", "subtype": "workstation", "pic": "icons/workstation.png",
         "x": 690, "y": 110, "width": 64, "height": 53,
         "ports": [{"connections": [], "x": 0, "y": 26.5, "id": "BEeeKQhvlM"},
                   {"connections": [], "x": 32, "y": 0, "id": "Bg6yRqsANB"},
                   {"connections": [], "x": 64, "y": 26.5, "id": "sWI6oW7kx0"},
                   {"connections": [], "x": 32, "y": 53, "id": "lxTUSJSm6D"},
                   {"connections": [], "x": 64, "y": 53, "id": "qOgRdsEOCf"},
                   {"connections": [], "x": 0, "y": 53, "id": "BRVKrShI1Q"},
                   {"connections": [], "x": 64, "y": 0, "id": "v64lqA0nD7"},
                   {"connections": [], "x": 0, "y": 0, "id": "IOmdxGb9No"}],
         "annotations": [{"text": "email", "x": 691, "y": 168, "for": "Fdd4V6Qoyf"},
                         {"text": "172.16.2.3", "x": 722, "y": 163, "for": "lxTUSJSm6D"}]},
        {"id": "q0lbQJLT6G", "type": "DiagramFigure", "subtype": "workstation", "pic": "icons/workstation.png",
         "x": 777, "y": 108, "width": 64, "height": 53,
         "ports": [{"connections": [], "x": 0, "y": 26.5, "id": "2Vp6MPP0Cn"},
                   {"connections": [], "x": 32, "y": 0, "id": "RlCnwlc7fT"},
                   {"connections": [], "x": 64, "y": 26.5, "id": "a9Z6cdqXHS"},
                   {"connections": [], "x": 32, "y": 53, "id": "7iDKoGfxyq"},
                   {"connections": [], "x": 64, "y": 53, "id": "ZgAL8vrdvG"},
                   {"connections": [], "x": 0, "y": 53, "id": "NmfiNxvwgF"},
                   {"connections": [], "x": 64, "y": 0, "id": "mdObxGD4M9"},
                   {"connections": [], "x": 0, "y": 0, "id": "EQNHKVAcll"}],
         "annotations": [{"text": "dns", "x": 778, "y": 166, "for": "q0lbQJLT6G"},
                         {"text": "172.16.2.4", "x": 809, "y": 161, "for": "7iDKoGfxyq"}]},
        {"id": "zDFyeWPdmD", "type": "DiagramFigure", "subtype": "router", "pic": "icons/router.png", "x": 687,
         "y": 309, "width": 66, "height": 45, "ports": [{"connections": [
            {"source": "06Acbal21m", "target": "KvfzIPL1yF", "color": "128,128,255"},
            {"source": "06Acbal21m", "target": "SfbuEm5U3Z", "color": "128,128,255"}], "x": 0, "y": 22.5,
                                                         "id": "06Acbal21m"}, {"connections": [
            {"source": "Alun6vU20a", "target": "FXeMW4RIZQ", "color": "128,128,255"},
            {"source": "Alun6vU20a", "target": "lxTUSJSm6D", "color": "128,128,255"},
            {"source": "Alun6vU20a", "target": "7iDKoGfxyq", "color": "128,128,255"}], "x": 33, "y": 0,
                                                                               "id": "Alun6vU20a"}, {"connections": [
            {"source": "oPAUnksBvL", "target": "mL9v2Uyvo1", "color": "128,128,255"}], "x": 66, "y": 22.5,
                                                                                                     "id": "oPAUnksBvL"},
                                                        {"connections": [
                                                            {"source": "2KEiLTRGLR", "target": "JLFU7ZdP7P",
                                                             "color": "128,128,255"},
                                                            {"source": "2KEiLTRGLR", "target": "khu8TurK0L",
                                                             "color": "128,128,255"}], "x": 33, "y": 45,
                                                         "id": "2KEiLTRGLR"},
                                                        {"connections": [], "x": 66, "y": 45, "id": "HTtoUVwuSo"},
                                                        {"connections": [], "x": 0, "y": 45, "id": "lcD5mOIMbI"},
                                                        {"connections": [], "x": 66, "y": 0, "id": "BWViFV5pAW"},
                                                        {"connections": [], "x": 0, "y": 0, "id": "aaB9g49BDC"}],
         "annotations": [{"text": "gw; install.snort 172.16.3.3", "x": 688, "y": 359, "for": "zDFyeWPdmD"},
                         {"text": "172.16.1.100", "x": 636, "y": 344, "for": "06Acbal21m"},
                         {"text": "172.16.2.100", "x": 720, "y": 309, "for": "Alun6vU20a"},
                         {"text": "172.16.10.2;NAT:abc", "x": 753, "y": 332, "for": "oPAUnksBvL"}]},
        {"id": "gLW5xKF2Oo", "type": "DiagramFigure", "subtype": "router", "pic": "icons/router.png", "x": 863,
         "y": 309, "width": 66, "height": 45, "ports": [{"connections": [], "x": 0, "y": 22.5, "id": "mL9v2Uyvo1"},
                                                        {"connections": [], "x": 33, "y": 0, "id": "P6RlbrJ9of"},
                                                        {"connections": [], "x": 66, "y": 22.5, "id": "dCQykgLqKM"},
                                                        {"connections": [], "x": 33, "y": 45, "id": "8fttHOi8xq"},
                                                        {"connections": [], "x": 66, "y": 45, "id": "yCTHC98TS8"},
                                                        {"connections": [], "x": 0, "y": 45, "id": "P9wsoELb6X"},
                                                        {"connections": [], "x": 66, "y": 0, "id": "Aw3Xfb7Ug9"},
                                                        {"connections": [], "x": 0, "y": 0, "id": "sGzmCT3FSu"}],
         "annotations": [{"text": "172.16.10.100", "x": 863, "y": 309, "for": "mL9v2Uyvo1"},
                         {"text": "172.16.20.100", "x": 896, "y": 354, "for": "8fttHOi8xq"},
                         {"text": "gw2", "x": 864, "y": 359, "for": "gLW5xKF2Oo"}]},
        {"id": "cr9dnaTQdN", "type": "DiagramFigure", "subtype": "laptop", "pic": "icons/laptop.png", "x": 871,
         "y": 465, "width": 85, "height": 64, "ports": [{"connections": [], "x": 0, "y": 32, "id": "UACANDsxWL"}, {
            "connections": [{"source": "BSlivpgzWn", "target": "8fttHOi8xq", "color": "128,128,255"}], "x": 42.5,
            "y": 0, "id": "BSlivpgzWn"}, {"connections": [], "x": 85, "y": 32, "id": "RtJKoO7LO2"},
                                                        {"connections": [], "x": 42.5, "y": 64, "id": "OFfF9m3dlQ"},
                                                        {"connections": [], "x": 85, "y": 64, "id": "NL3UbBU3Zc"},
                                                        {"connections": [], "x": 0, "y": 64, "id": "kPOHrSCCoa"},
                                                        {"connections": [], "x": 85, "y": 0, "id": "wxNyIZVqRv"},
                                                        {"connections": [], "x": 0, "y": 0, "id": "WB1XyT8xBi"}],
         "annotations": [{"text": "172.16.20.2", "x": 913.5, "y": 465, "for": "BSlivpgzWn"},
                         {"text": "kali", "x": 872, "y": 534, "for": "cr9dnaTQdN"}]}]}

    netdef = draw2netdef(json_diagram)
    assert netdef == \
           {'ExperimentDomainName': 'e1.teamname.ncl.sg', 'Nodes': [
               {'Name': 'n1', 'Type': 'Gateway',
                'VMs': [{'Name': 'gw2', 'OS': 'bento/ubuntu-16.04', 'Forward': 1,
                         'Nets': [{'IP': '172.16.10.100', 'NetType': 'VN3'},
                                  {'IP': '172.16.20.100', 'NetType': 'VN5'}]},
                        {'Name': 'gw', 'Nets': [{'IP': '172.16.1.100', 'NetType': 'VN1'},
                                                {'IP': '172.16.2.100', 'NetType': 'VN2'},
                                                {'IP': '172.16.10.2', 'NetType': 'VN3', 'NAT': ['abc']},
                                                {'IP': '', 'NetType': 'VN4'}],
                         'install': ['install.snort 172.16.3.3'], 'Forward': 1, 'OS': 'bento/ubuntu-16.04'},
                        {'Name': 'db', 'Nets': [{'IP': '172.16.3.2', 'NetType': 'VN4'}],
                         'install': ['install.db'], 'OS': 'bento/ubuntu-16.04'},
                        {'Name': 'siem', 'Nets': [{'IP': '172.16.3.3', 'NetType': 'VN4'}],
                         'install': ['install.splunk'], 'OS': 'bento/ubuntu-16.04'},
                        {'Name': 'kali', 'OS': 'kali.2018',
                         'Nets': [{'IP': '172.16.20.2', 'NetType': 'VN5'}]},
                        {'Name': 'win10', 'OS': 'senglin/win-10-enterprise-vs2015community',
                         'Nets': [{'IP': '172.16.1.2', 'NetType': 'VN1'}]},
                        {'Name': 'ubuntu', 'OS': 'bento/ubuntu-16.04',
                         'Nets': [{'IP': '172.16.1.3', 'NetType': 'VN1'}]},
                        {'Name': 'web', 'Nets': [{'IP': '172.16.2.2', 'NetType': 'VN2'}],
                         'install': ['install.web'], 'OS': 'bento/ubuntu-16.04'},
                        {'Name': 'email', 'OS': 'bento/ubuntu-16.04',
                         'Nets': [{'IP': '172.16.2.3', 'NetType': 'VN2'}]},
                        {'Name': 'dns', 'OS': 'bento/ubuntu-16.04',
                         'Nets': [{'IP': '172.16.2.4', 'NetType': 'VN2'}]}]}],
            'LANs': [],
            'Reserve': 'pc3a, pc4b, pc17e, pc19d'}


def main():
    '''The func is the main func.'''
    import sys
    if (len(sys.argv) == 2) and (sys.argv[1] == "test"):
        test()
        print
        "Pass all test"
        exit()
    elif (len(sys.argv) == 4) and (sys.argv[1] == "project") and (sys.argv[2] == "netdef-input"):
        with open(sys.argv[3], 'r') as afile:
            file_content = afile.read()

        netdef = json.loads(file_content)
        import vagrantfile
        vagrantfile.produce_nsfile(netdef)
        vagrantfile.produce_vf(netdef)
        vagrantfile.produce_ansible(netdef)
        vagrantfile.produce_hostfile(netdef)
        vagrantfile.produce_runcmd(netdef)
    elif (len(sys.argv) == 4) and (sys.argv[1] == "ns") and (sys.argv[2] == "netdef-input"):
        with open(sys.argv[3], 'r') as afile:
            file_content = afile.read()

        netdef = json.loads(file_content)
        import vagrantfile
        vagrantfile.produce_nsfile(netdef)
    elif (len(sys.argv) == 3) and (sys.argv[1] == "project"):
        with open(sys.argv[2], 'r') as afile:
            file_content = afile.read()

        net_draw = json.loads(file_content)
        netdef = draw2netdef(net_draw)
        import vagrantfile_hk as vagrantfile
        # vagrantfile.produce_nsfile(netdef)
        # vagrantfile.produce_vf(netdef)
        # vagrantfile.produce_ansible(netdef)
        # vagrantfile.produce_hostfile(netdef)
        vagrantfile.produce_runcmd(netdef)
    elif (len(sys.argv) == 3) and (sys.argv[1] == "ns"):
        with open(sys.argv[2], 'r') as afile:
            file_content = afile.read()

        net_draw = json.loads(file_content)
        netdef = draw2netdef(net_draw)
        import vagrantfile
        vagrantfile.produce_nsfile(netdef)
    elif (len(sys.argv) == 3) and (sys.argv[1] == "runcmd"):
        with open(sys.argv[2], 'r') as afile:
            file_content = afile.read()

        net_draw = json.loads(file_content)
        netdef = draw2netdef(net_draw)
        import vagrantfile
        vagrantfile.produce_runcmd(netdef)
    elif len(sys.argv) == 2:
        with open(sys.argv[1], 'r') as afile:
            file_content = afile.read()

        net_draw = json.loads(file_content)
        netdef = draw2netdef(net_draw)
        print
        json.dumps(netdef, indent=4)  # , separators=(',', ': '))
    elif len(sys.argv) == 3:
        with open(sys.argv[1], 'r') as afile:
            file_content = afile.read()

        net_draw = json.loads(file_content)
        netdef = draw2netdef(net_draw)
        with open(sys.argv[2], 'w') as afile:
            afile.write(json.dumps(netdef, indent=4, separators=(',', ': ')))
    else:
        usage(sys.argv[0])


if __name__ == "__main__":
    main()
