# Router VM(Which has more than 1 interface)
# Highly Recommend that the VM which plays the role of router has a static ip ending in ".2", like "*.*.*.2"
# rather the one ending in ".1", like "*.*.*.1"
# Because, the Host Adapter vboxnet[N] often goes with ip ending in ".1" which should be better not attach to a VM.
# So that we don't need to run "sudo ifconfig down vboxnet[N]" for the host node.
# By default, the Router VM is configured net.ipv4.ip_forward = 1

# Default Gateway
# We assume, only vboxnet1 with ip endinng in ".1" can be set in VM's default gateway
# For others, vboxnet[2,3,...,N], the ip ending in ".1" is attached to host node while the one ending in ".2" is attached to VM
# In general, one Virtual Machine has 1 interface, so default gateway:
    # if only one hostonly interface 172.16.1.*, default gw is that 172.16.1.2
    # if only one internal interface 172.16.1.*, default gw is that 172.16.1.2
# If a Virtual Machine has more than 1 interface, so default gateway:
    # We assume this VM is Router VM
    # By default, default gateway is regarding the first hostonly interface:
    # e.g., if both hostonly&internal interface 172.16.1.*, 172.16.2.* & 172.16.3.*, that VM's default gw is
    # 172.16.1.1(vboxnet1)
    # 172.16.1.2(vboxnet[2,3,...,N])

sudo route del default
# It may be a router VM
sudo route add default gw 172.16.1.1
sudo sed -i 's/#net.ipv4.ip_forward=1/net.ipv4.ip_forward=1/g' /etc/sysctl.conf
sudo sysctl -p /etc/sysctl.conf
# Other network router
# NAT configuration
