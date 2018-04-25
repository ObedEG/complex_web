from src.common.webtools.utils import Utils


class Xcat(object):
    @staticmethod
    def create_switch(switch, ip, vm):
        """
        Use this function to create and config a switch in a vm
        :param switch: switch name - hostname
        :param ip: This is the IP of the switch
        :param vm: this is the IP of the VM - Management node
        :return:
        """
        cmnds = list()
        cmnds.append('mkdef -t node {0} groups=switch ip={1}'.format(switch, ip))  # create switch node
        cmnds.append('makehosts {}'.format(switch))  # make hosts
        cmnds.append('confetty create /nodegroups/switch')  # make confluent
        cmnds.append('confetty create /nodes/{} groups=switch'.format(switch))
        # config confetty
        cmnds.append('confetty set /nodegroups/switch/attributes/current secret.hardwaremanagementpassword="RO"')
        cmnds.append('confetty set /nodegroups/everything/attributes/current discovery.policy=open')
        for cmd in cmnds:
            Utils.run_shell('ssh ' + vm + ' ' + cmd)

    @staticmethod
    def create_node(hostname, ip_os, ip_bmc, vm):
        """
        Use this function to create a node in xcat
        :param hostname: the name for the node
        :param ip_os: IP for the OS
        :param ip_bmc: IP defined for the node-bmc
        :param vm: it would be the IP of the VM
        :return:
        """
        cmnds = list()
        cmnds.append('mkdef -t node {0} groups=all,compute,ipmi mgt=ipmi '
                     'ip={1} netboot=xnba bmc={0}-xcc installnic=mac primarynic=mac'.format(hostname, ip_os))  # create node
        cmnds.append('mkdef -t node {0}-bmc groups=bmc ip={1}'.format(hostname, ip_bmc))  # create bmc
        cmnds.append('makehosts {0},{0}-bmc'.format(hostname))  # make hosts
        cmnds.append('makeconfluentcfg {}'.format(hostname))  # make confluent
        cmnds.append('nodeattrib {} console.method=ipmi'.format(hostname))  # config confetty
        for cmd in cmnds:
            Utils.run_shell('ssh ' + vm + ' ' + cmd)

    @staticmethod
    def set_node_switch(hostname, switch, switchport, vm):
        """
        Use this function to set switch/switchport definition,
        in order to test P2P requirements
        :param vm: Virtual Machine IP - '172.15.0.22'
        :return: 0 - if the final command ran well
        """
        create_node = ' chdef -t node {0} switch={1} switchport={2}'.format(hostname, switch, switchport)
        return Utils.run_shell('ssh ' + vm + create_node)

    @staticmethod
    def set_node_macs(hostname, macs, vm):
        """
        Use this function to set the MACs registered in xml, so it could be
        discovered by mac without switch/switchport definition
        :param vm: Virtual Machine IP - '172.15.0.22'
        :return: 0 - if the final command ran well
        """
        create_node = ' chdef -t node {} mac='.format(hostname) + "'" + macs + "'"
        return Utils.run_shell('ssh ' + vm + create_node)

    @staticmethod
    def restart_discovery_services(vm):
        cmnds = list()
        cmnds.append(' makedns - n')
        cmnds.append(' makedhcp -n')
        cmnds.append(' service dhcpd restart')
        cmnds.append(' service network restart')
        for cmd in cmnds:
            Utils.run_shell('ssh ' + vm + cmd)