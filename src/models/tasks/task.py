import uuid

import src.models.tasks.constants as TasksConstants
from src.common.database import Database
from src.common.utils import Utils


class Task(object):

    def __init__(self, rack, category, description, started_at=None, start_user=None,
                 finished_at=None, finish_user=None, failure=None, status=None, _id=None):
        self.rack = rack
        self.category = category  # According to racktype... and Task...
        self.description = description  # Describe the step (Task, Failure or Fix)
        self.started_at = "" if started_at is None else started_at
        self.start_user = "" if start_user is None else start_user
        self.finished_at = "" if finished_at is None else finished_at
        self.finish_user = "" if finish_user is None else finish_user
        self.failure = "" if failure is None else failure  # if it fails here will be the failure._id
        self.status = "Waiting..." if status is None else status  # could be: Waiting..., Running, Debugging, Finished
        self._id = uuid.uuid1().hex if _id is None else _id

    def json(self):
        return {
            "rack": self.rack,
            "description": self.description,
            "started_at": self.started_at,
            "start_user": self.start_user,
            "finished_at": self.finished_at,
            "finish_user": self.finish_user,
            "category": self.category,
            "failure": self.failure,
            "status": self.status,
            "_id": self._id
        }

    @classmethod
    def get_tasks_by_racktype(cls, racktype, rack):
        task_list = []
        if racktype == "ryo":
            task_list.append(cls(rack=rack, category="Power on validation",
                                 description="PDUs power on (Apply power to rack)").save_task())
            task_list.append(cls(rack=rack, category="Power on validation",
                                 description="All devices power on (power on servers/devices)").save_task())
            task_list.append(cls(rack=rack, category="Power on validation",
                                  description="Validate that there are no error LED's on any devices").save_task())
            task_list.append(cls(rack=rack, category="Power redundancy check",
                                  description="Check if  the rack devices are wired in power redundant configuration").save_task())
            task_list.append(cls(rack=rack, category="Power redundancy check",
                                  description="Perform power redundancy test per  p-07918, if apply").save_task())
            task_list.append(cls(rack=rack, category="Power Cycle",
                                  description="Complete one AC power cycle").save_task())
            return task_list

        elif racktype == "ryo_nw":
            task_list.append(cls(rack=rack, category="Power on validation",
                                 description="PDUs power on (Apply power to rack)").save_task())
            task_list.append(cls(rack=rack, category="Power on validation",
                                 description="All devices power on (power on servers/devices)").save_task())
            task_list.append(cls(rack=rack, category="Power on validation",
                                 description="Validate that there are no error LED's on any devices").save_task())
            task_list.append(cls(rack=rack, category="Power redundancy check",
                                 description="Check if  the rack devices are wired in power redundant configuration").save_task())
            task_list.append(cls(rack=rack, category="Power redundancy check",
                                 description="Perform power redundancy test per  p-07918, if apply").save_task())
            task_list.append(cls(rack=rack, category="Network Validation",
                                 description="Connectivity validated to each connected network port").save_task())
            task_list.append(cls(rack=rack, category="Network Validation",
                                 description="Correct Port Speed validated").save_task())
            task_list.append(cls(rack=rack, category="Data Collect",
                                 description="Collect the port speed evidence of each switch. Login into the switch console and get the interfaces status, save the log into a text file").save_task())
            task_list.append(cls(rack=rack, category="Power Cycle",
                                 description="Complete one AC power cycle").save_task())
            return task_list

        elif racktype == "ic":
            task_list.append(cls(rack=rack, category="Power on validation",
                                 description="PDUs power on (Apply power to rack)").save_task())
            task_list.append(cls(rack=rack, category="Power on validation",
                                 description="All power supplies on").save_task())
            task_list.append(cls(rack=rack, category="Power on validation",
                                 description="Validate that there are no error LED's on any devices").save_task())
            task_list.append(cls(rack=rack, category="Power redundancy check",
                                 description="Check if  the rack devices are wired in power redundant configfuration").save_task())
            task_list.append(cls(rack=rack, category="Power redundancy check",
                                 description="Perform power redundancy test per  p-07918, if apply").save_task())
            task_list.append(cls(rack=rack, category="Network Validation",
                                 description="Connectivity validated to each connected network port").save_task())
            task_list.append(cls(rack=rack, category="Network Validation",
                                 description="Correct Port Speed validated").save_task())
            task_list.append(cls(rack=rack, category="Peripheral Set Up",
                                 description="Set up IP and hostname for 1G switches").save_task())
            task_list.append(cls(rack=rack, category="Peripheral Set Up",
                                 description="Set up IP and hostname for 10G switches").save_task())
            task_list.append(cls(rack=rack, category="Peripheral Set Up",
                                 description="Set Up IP/hostname/ & update firmware/image for HIGHSPEED Switches (IB Mellanox / OPA) if apply").save_task())
            task_list.append(cls(rack=rack, category="Peripheral Set Up",
                                 description="Verify switches image and update if required, save log of each switch").save_task())
            task_list.append(cls(rack=rack, category="Peripheral Set Up",
                                 description="Set up IP PDUs & save logs").save_task())
            task_list.append(cls(rack=rack, category="Storage Set up",
                                 description="Set up IP and RAID config, update image if apply on all storage devices").save_task())
            task_list.append(cls(rack=rack, category="Slave SWITCH set up",
                                 description="Connect the ethernet cables from the nodes to a captive switch, use a P2P defined in xcat-config in order to discover them").save_task())
            task_list.append(cls(rack=rack, category="Discovery",
                                 description="Turn on nodes/servers to discover macs (run xcat-genesis image)").save_task())
            task_list.append(cls(rack=rack, category="Discovery",
                                 description="Run netboot image and Verify NODES vs P2P, run in console:  for i in `nodels all`; do rbeacon $i on; sleep 1;done").save_task())
            task_list.append(cls(rack=rack, category="Discovery",
                                 description="Discovery FPC, run: configfpc -V -i ens5 --ip 192.168.0.100 ***ens5 could change on each Virtual Machine, verify ethernet device with 'ifconfig'").save_task())
            task_list.append(cls(rack=rack, category="Discovery",
                                 description="Verify FPC vs P2P (ping fpc, remove their ethernet cable, connect cable again)").save_task())
            task_list.append(cls(rack=rack, category="Firmware Check",
                                 description="Verify FW Levels of all servers (run in xcat >>> rinv all firm | xcoll), update FW if required according to current Best Recipe").save_task())
            task_list.append(cls(rack=rack, category="Firmware Check",
                                 description="Verify FW Levels of FPC, update FW if required according to current Best Recipe").save_task())
            task_list.append(cls(rack=rack, category="RAID set up",
                                 description="Set up a RAID 1, locate drives: storcli /call show all; then run: storcli /cX add vd type=raid1 drives=XX:X-X *** 'X' is the number related").save_task())
            task_list.append(cls(rack=rack, category="Run Image",
                                 description="Install and verify redhat image into HDD of all servers").save_task())
            task_list.append(cls(rack=rack, category="Run Image",
                                 description="Install and verify redhat image needed into Ramdisk of all servers [ Diskless install ]").save_task())
            task_list.append(cls(rack=rack, category="Update Mellanox Unmanaged switch image",
                                 description="Update image if apply according to current BR. <br> 1. Run mellanox-image into a node connected to the switch. <br> 2. From that node start the services: opensm and openibd. <br> 3. Run ibswitches and get the lid number. <br> 4. Flash the switch using the command format:  flint -d lid-28 -i fw-SwitchIB-rel-11_0200_0120-00KH883_00KH888_Ax.bin b <br> 5. Reboot the switch. <br> 6. Verify FW level with: flint -d lid-28 q <br> ").save_task())
            task_list.append(cls(rack=rack, category="Update Mellanox managed switch image",
                                 description="Update image if needed according to current BR. Use Web-GUI to accomplish it").save_task())
            task_list.append(cls(rack=rack, category="Linpack",
                                 description="Follow linpack procedure for Mellanox/OPA, save logs for Data Collection").save_task())
            task_list.append(cls(rack=rack, category="Power Cycle Test",
                                 description="Complete 4 AC power cycle").save_task())
            task_list.append(cls(rack=rack, category="Data Collect",
                                 description="Add RACK,CPOM,MFG info to xcat node's groups <br>(EXAMPLE, run in console: chdef all groups=all,compute,ipmi,RACKA1,CPOM201700063,MFGJ11E8PG) and run the script: /home/MAKEINFO/getinfo.sh").save_task())
            task_list.append(cls(rack=rack, category="Clear for ship",
                                 description="Clear IMM: /home/ALLEASY/clearIMM.sh").save_task())
            task_list.append(cls(rack=rack, category="Clear for ship",
                                 description="Clear FPC: /home/ALLEASY/clearFPC.sh").save_task())
            task_list.append(cls(rack=rack, category="Clear for ship",
                                 description="Clear Image in HDD: /home/ALLEASY/clearOS.sh").save_task())
            task_list.append(cls(rack=rack, category="Clear for ship",
                                 description="Clear RAID 1 on servers/nodes").save_task())
            task_list.append(cls(rack=rack, category="Clear for ship",
                                 description="Clear RAID on all storage devices").save_task())
            task_list.append(cls(rack=rack, category="CMOS settings",
                                 description="Select cmos config from >>> home/ALLEASY/cmos_settings ,using: pasu all batch *selected_cmos_settings*").save_task())
            task_list.append(cls(rack=rack, category="Customer settings",
                                 description="Apply changes to cover client requirements").save_task())
            return task_list

        elif racktype == "gss":
            task_list.append(cls(rack=rack, category="Power on validation",
                                 description="PDUs power on (Apply power to rack)").save_task())
            task_list.append(cls(rack=rack, category="Power on validation",
                                 description="Validate that there are no error LED's on any devices").save_task())
            task_list.append(cls(rack=rack, category="Power redundancy check",
                                 description="Check if  the rack devices are wired in power redundant configfuration").save_task())
            task_list.append(cls(rack=rack, category="Power redundancy check",
                                 description="Perform power redundancy test per  p-07918, if apply").save_task())
            task_list.append(cls(rack=rack, category="Network Validation",
                                 description="Connectivity validated to each connected network port").save_task())
            task_list.append(cls(rack=rack, category="Network Validation",
                                 description="Correct Port Speed validated").save_task())
            task_list.append(cls(rack=rack, category="Peripheral Setup",
                                 description="Set up IP and hostname for 1G switches").save_task())
            task_list.append(cls(rack=rack, category="Peripheral Setup",
                                 description="Set up IP and hostname for 10G switches").save_task())
            task_list.append(cls(rack=rack, category="Peripheral Setup",
                                 description="Set Up IP and hostname for HIGHSPEED Switches (IB Mellanox / OPA) if apply").save_task())
            task_list.append(cls(rack=rack, category="Peripheral Setup",
                                 description="Check switches image and update if required and save log of each switch").save_task())
            task_list.append(cls(rack=rack, category="Peripheral Setup",
                                 description="Set up IP PDUs & save logs").save_task())
            task_list.append(cls(rack=rack, category="Discovery",
                                 description="Turn on nodes/servers to discover macs (runinng xcat-genesis image)").save_task())
            task_list.append(cls(rack=rack, category="GSS Nodes Definition",
                                 description="1. GSS server node definition (define gss01 & gss02 in xcat tables)").save_task())
            task_list.append(cls(rack=rack, category="GSS Server FW Update",
                                 description="2.1 Perform GSS server firmware update <br> nodeset gss01, gss02 runimage=http://172.20.0.1/install/gss/runimages/firmware.tgz <br> rsetboot gss01,gss02 net -u<br> rpower gss01,gss02 boot").save_task())
            task_list.append(cls(rack=rack, category="GSS Raid Config",
                                 description="2.2 Perform GSS RAID config of the ServeRAID <br> nodeset gss01, gss02 runimage=http://172.20.0.1/install/gss/runimages/raid.tgz <br> rsetboot gss01,gss02 net -u<br> rpower gss01,gss02 boot").save_task())
            task_list.append(cls(rack=rack, category="GSS UEFI Settings",
                                 description="2.3 Perform GSS  server UEFI settings <br> nodeset gss01, gss02 runimage=http://172.20.0.1/install/gss/runimages/asu.tgz <br> rsetboot gss01,gss02 net -u<br> rpower gss01,gss02 boot <br>").save_task())
            task_list.append(cls(rack=rack, category="GSS Verify Nodes",
                                 description="2.4 Verify IMM <br> ping gss01-bmc<br> ping gss02-bmc <br> sleep 60<br> rpower gss state <br> At this stage the power state of the nodes should still be on because they are still in genesis boot mode.").save_task())
            task_list.append(cls(rack=rack, category="GSS Verify Nodes",
                                 description="2.5 Reboot and verify FW level <br> rinv gss01,gss02 firmware | xcoll <br> nodeset gss01,gss02 shell <br>rsetboot gss01,gss02 net -u <br>rpower gss01,gss02 boot").save_task())
            task_list.append(cls(rack=rack, category="GSS OS Installation",
                                 description="3. Install the OS on the GSS servers <br> nodeset gss01,gss02 osimage=gssServer_3.1 <br> rsetboot gss01,gss02 net -u <br> rpower gss01,gss02 boot").save_task())
            task_list.append(cls(rack=rack, category="GSS Turn on JBODs",
                                 description="4. Power On the GSS JBOD, verify status and Storage enclosure layout (see page 9 in GSS manual)").save_task())
            task_list.append(cls(rack=rack, category="GSS Quick check",
                                 description="5. Verify the PCI adapter placement. <br> cd /install/gss/setupTools <br> ./gss_storage_quick_check gss01,gss02").save_task())
            task_list.append(cls(rack=rack, category="GSS DiskTopology Topsummary",
                                 description="6. Verify the disk storage setup <br> ssh root@gss01 <br> cd /tmp <br> mmgetpdisktopology > mmgetpdisktopology.1.txt <br> cat mmgetpdisktopology.1.txt | topsummary | tee topsummary.1.txt <br> exit").save_task())
            task_list.append(cls(rack=rack, category="GSS FindMissingDisks",
                                 description="7. Run findMissingDisks <br> ssh root@172.20.0.1 <br> cd /install/gss/setupTools<br> ./findMissingDisks gss01,gss02 <br> If all disks are found, the script returns listing no missing disks").save_task())
            task_list.append(cls(rack=rack, category="GSS FindBadDisks",
                                 description="8. Run findBadDisks <br> ssh root@172.20.0.1 <br> cd /install/gss/setupTools <br>./findBadDisks -m r -T 60 gss01,gss02 # read test, 60sec").save_task())
            task_list.append(cls(rack=rack, category="GSS Create & Config Spectrum Scale",
                                 description="9.1 Create and configure a Spectrum Scale cluster. Run genGssCluster <br> ssh root@172.20.0.1 <br>cd /install/gss/setupTools <br> ./genGssCluster gss01,gss02 | tee /tmp/genGssCluster.log").save_task())
            task_list.append(cls(rack=rack, category="GSS Create & Config Spectrum Scale",
                                 description="9.2 Create and configure a Spectrum Scale cluster. Start Spectrum Scale <br> ssh root@gss01 <br> mmlscluster <br> mmlsconfig <br> mmgetstate -N gss01,gss02 <br> mmstartup -N gss01,gss02 ; mmgetstate -N gss01,gss02 <br> sleep 5 <br> mmgetstate -N gss01,gss02 <br> Verify mmdiag <br> mmdiag --version <br> ssh root@gss02 /usr/lpp/mmfs/bin/mmdiag --version").save_task())
            task_list.append(cls(rack=rack, category="GSS Firmware Upgrades",
                                 description="10.1 Firmware Upgrades. Stop Spectrum Scale on the GSS servers <br> ssh root@gss01 <br> mmgetstate -N gss01,gss02 <br> mmshutdown -N gss01,gss02 <br> mmgetstate -N gss01,gss02 # state should now be down <br> exit <br>").save_task())
            task_list.append(cls(rack=rack, category="GSS Firmware Upgrades",
                                 description="10.2 Firmware Upgrades. Verify SAS adapter firmware <br> ssh root@gss01 <br> /install/gss/opt/lenovo/gss/firmware/adapter/gsslsfw-lsi <br> exit <br> Verify in gss02 too: <br> ssh root@gss02 <br> /install/gss/opt/lenovo/gss/firmware/adapter/gsslsfw-lsi <br> exit").save_task())
            task_list.append(cls(rack=rack, category="GSS Firmware Upgrades",
                                 description="10.3 Firmware upgrades. Verify and upgrade storage enclosure firmware <br> mmchconfig nsdRAIDFirmwareDirectory=/opt/lenovo/gss/firmware <br>mmlsconfig nsdRAIDFirmwareDirectory <br> <br> TO FLASH RUN: <br> ssh root@gss01 <br> mmlsfirmware --type storage-enclosure <br>mmchfirmware --type storage-enclosure --fast-offline <br>mmlsfirmware --type storage-enclosure <br>sleep 300 <br>mmlsenclosure all --not-ok <br>exit").save_task())
            task_list.append(cls(rack=rack, category="GSS Firmware Upgrades",
                                 description="10.4 Firmware Upgrades. Verify and upgrade disk drive firmware <br> ssh root@gss01 <br> mmlsfirmware --type drive | less <br> mmchfirmware --type drive --fast-offline <br> mmlsfirmware --type drive | less <br> exit").save_task())
            task_list.append(cls(rack=rack, category="GSS Firmware Upgrades",
                                 description="10.5 Firmware Upgrades. Start Spectrum Scale again on the GSS servers <br> ssh root@gss01 <br> mmgetstate -N gss01,gss02 <br> mmstartup -N gss01,gss02 ; mmgetstate -N gss01,gss02 <br> sleep 5 <br> mmgetstate -N gss01,gss02 <br> exit").save_task())
            task_list.append(cls(rack=rack, category="GSS Config Spectrum Scale RAID",
                                 description="11. Configure Spectrum Scale RAID (RGs, DAs, and log vdisks) <br> ssh root@172.20.0.1 <br> cd /install/gss/setupTools <br> ./genClusterRgs gss01,gss02 <br> ssh root@gss01 <br> mmlsrecoverygroup # lists all RGs in the cluster <br> mmlsrecoverygroup gss01 <br> mmlsrecoverygroup gss02 <br> mmlsrecoverygroup gss01 -L | less <br> mmlsrecoverygroup gss02 -L | less <br> mmlsrecoverygroup gss01 -L --pdisk | less <br> mmlsrecoverygroup gss02 -L --pdisk | less <br> ").save_task())
            task_list.append(cls(rack=rack, category="GSS Config Spectrum Scale RAID",
                                 description="12.1 Create a Spectrum Scale filesystem. Define the data layout in a vdisk stanza file <br> ssh root@gss01 <br> cd /opt/lenovo/gss/setupTools/ <br> ./genGPFSVdisk vdisk.cfg <br> more vdisk.cfg <br> cp vdisk.cfg vdisk.orig").save_task())
            task_list.append(cls(rack=rack, category="GSS Spectrum Scale filesystem",
                                 description="12.2 Create a Spectrum Scale filesystem. Create vdisks. <br> mmcrvdisk -F vdisk.cfg <br> mmlsvdisk <br> <br> Create NSDs <br> mmcrnsd -F vdisk.cfg <br> mmlsnsd <br> <br> Create and mount Spectrum Scale file system(s) <br> mmcrfs gsstest1 -F vdisk.cfg -j scatter -T /gpfs/gsstest1 -B 16M --metadata-block-size 1M <br> <br> Policy engine: <br> echo ''rule 'default' set pool 'data' '' > policy.cfg <br> mmchpolicy gsstest1 policy.cfg <br><br> Mount file system: <br> mmmount gsstest1 -a <br> mmdf gsstest1").save_task())
            task_list.append(cls(rack=rack, category="GSS Stress Test (gss01)",
                                 description="# Test the local disk bandwidth on gss01: <br> ssh root@gss01 <br> mmchrecoverygroup gss02 --active gss01 # may run a few minutes... <br> gpfsperf create seq /gpfs/gsstest1/testfile1A -n 128G -r 16M -th 4 <br> gpfsperf read seq /gpfs/gsstest1/testfile1A -n 128G -r 16M -th 4 <br> mmchrecoverygroup gss02 --active gss02 # may run a few minutes... <br> exit").save_task())
            task_list.append(cls(rack=rack, category="GSS Stress Test (gss02)",
                                 description="# Test the local disk bandwidth on gss02: <br> ssh root@gss02 <br> mmchrecoverygroup gss01 --active gss02 # may run a few minutes... <br> gpfsperf create seq /gpfs/gsstest1/testfile1A -n 128G -r 16M -th 4 <br> gpfsperf read seq /gpfs/gsstest1/testfile1A -n 128G -r 16M -th 4 <br> mmchrecoverygroup gss01 --active gss01  # may run a few minutes... <br> exit").save_task())
            task_list.append(cls(rack=rack, category="GSS Populate Spectrum Scale Component Database",
                                 description="Updating component specifications. <br> ssh root@gss01<br> mmaddcompspec -F /opt/lenovo/gss/data/compSpec-Lenovo.stanza. <br><br> List component specification: <br> mmlscompspec # lists specs for all component types <br> mmlscompspec --type rack <br> mmlscompspec --type server <br> mmlscompspec --type storageEnclosure <br> mmlscompspec --type storageServer <br> ").save_task())
            task_list.append(cls(rack=rack, category="GSS Adding HardWare components",
                                 description="Add the listed hardware Components with: <br> mmdiscovercomp -N gss01,gss02 --dry-run <br> mmdiscovercomp -N gss01,gss02. <br><br> Add rack component like this example: <br> mmaddcomp 1410HPA --serial-number '23J4567' --name 'A1' <br> mmlscomp --type rack").save_task())
            task_list.append(cls(rack=rack, category="GSS Component rack location",
                                 description="Query the server and enclosure serial numbers like this example: <br> mmlscomp --type server <br> mmgetpdisktopology | topsummary | grep '(number ' <br> cd /root <br> cat > gss26_loc.stanza <<E_O_F <br> %compLoc: compId=SV12345006 containerId=A1 position=25 <br> %compLoc: compId=SV12345005 containerId=A1 position=21 <br> %compLoc: compId=SV12345004 containerId=A1 position=17 <br> %compLoc: compId=06D5678 containerId=A1 position=15 <br> %compLoc: compId=06D1234 containerId=A1 position=13 <br> %compLoc: compId=SV12345003 containerId=A1 position=9 <br> %compLoc: compId=SV12345002 containerId=A1 position=5 <br> %compLoc: compId=SV12345001 containerId=A1 position=1 <br> E_O_F <br> mmchcomploc -F ./gss26_loc.stanza <br> mmlscomploc --container-type rack <br> ").save_task())
            task_list.append(cls(rack=rack, category="GSS Enclosure display IDs",
                                 description="We can display the location in the enclosure ID like this: <br> cd /root <br> cat > gss26_displayid.stanza <<E_O_F <br> %compLoc: serialNumber=SV12345006 displayId=25 <br> %compLoc: serialNumber=SV12345005 displayId=21 <br> %compLoc: serialNumber=SV12345004 displayId=17 <br> %compLoc: serialNumber=SV12345003 displayId=09 <br> %compLoc: serialNumber=SV12345002 displayId=05 <br> %compLoc: serialNumber=SV12345001 displayId=01 <br> E_O_F <br> mmchcomp -F ./gss26_displayid.stanza <br> mmsyncdisplayid all <br> mmlscomp --type storageEnclosure <br>").save_task())
            task_list.append(cls(rack=rack, category="GSS Document the setup ",
                                 description="The Spectrum Scale/GSS related configuration can be collected by using the gpfs.snap command. <br> ssh root@gss01 <br>gpfs.snap <br> exit<br> <br> mkdir –p ~/mfg/gpfs <br> scp -p root@gss01:/path/to/snap ~/mfg/gpfs <br> <br> get the snapfile and include it to Data collection").save_task())
            task_list.append(cls(rack=rack, category="GSS Clean UP",
                                 description="1. ssh gss01 <br> 2. /usr/lpp/mmfs/bin/mmumount gsstest1 -a <br> 3. cd /opt/lenovo/gss/setupTools/ <br> 4. mmdelfs gsstest1 <br> 5. ssh root@172.20.0.1 <br> 6. cd /install/gss/setuptools <br> 7. ./delVdisks -c gss01 <br> 8. ./gnrDelsetup -c gss01 <br> 9. ssh gss01 <br> 10. /usr/lpp/mmfs/bin/mmshutdown -N gss01,gss02 <br> 11. /usr/lpp/mmfs/bin/mmdelnode -N gss01,gss02 <br> 12. mmlscluster <br> a) the command should report there is no cluster <br> b) also verify that /dev/gpfs0 is not present <br> 14. Do NOT remove the OS. The GSS servers ship with the OS installed").save_task())
            task_list.append(cls(rack=rack, category="Power Cycle Test",
                                 description="Complete 4 AC power cycle").save_task())
            task_list.append(cls(rack=rack, category="Data Collect",
                                 description="Add RACK,CPOM,MFG info to node's groups (EXAMPLE, run in console: chdef all groups=all,compute,ipmi,RACKA1,CPOM201700063,MFGJ11E8PG) and run the script: /home/MAKEINFO/getinfo.sh").save_task())
            task_list.append(cls(rack=rack, category="Clear for ship",
                                 description="Clear IMM: /home/ALLEASY/clearIMM.sh").save_task())
            return task_list
        else:
            return task_list

    #  [cls(**elem) for elem in Database.find(RacksConstants.COLLECTIONS, {})]
    def save_task(self):
        Database.insert(TasksConstants.COLLECTIONS, self.json())
        return self._id

    def update_to_mongo(self):
        Database.update(TasksConstants.COLLECTIONS, {"_id": self._id}, self.json())

    def save_to_mongo(self):
        Database.insert(TasksConstants.COLLECTIONS, self.json())

    def delete_task(self):
        Database.remove(TasksConstants.COLLECTIONS, {'_id': self._id})

    @classmethod
    def get_task_by_id(cls, task):
        return cls(**Database.find_one(TasksConstants.COLLECTIONS, {"_id": task}))

    @classmethod
    def get_current_task(cls, rack):
        return cls(**Database.find_one(TasksConstants.COLLECTIONS,
                                       {"rack": rack, "status": {"$in": ['Running', 'Debugging']}}))

    def start(self, user):
        self.status = "Running"
        self.started_at = Utils.get_utc_time()
        self.start_user = user
        self.update_to_mongo()

    def finish(self, user):
        self.status = "Finished"
        self.finished_at = Utils.get_utc_time()
        self.finish_user = user
        self.update_to_mongo()

    def failed(self, failure):
        self.failure = failure
        self.status = "Debugging"
        self.update_to_mongo()

    @staticmethod
    def get_passed_tasks(rack):
        return Database.count(TasksConstants.COLLECTIONS, {"status": "Finished", "rack": rack})

    @staticmethod
    def get_number_of_tasks(rack):
        return Database.count(TasksConstants.COLLECTIONS, {"rack": rack})

    @staticmethod
    def get_tasks_progress(rack):
        return Utils.percentage(Task.get_passed_tasks(rack),
                                Task.get_number_of_tasks(rack))
