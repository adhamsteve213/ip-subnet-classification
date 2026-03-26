from dataclasses import dataclass
from ipaddress import AddressValueError, IPv4Network, IPv6Address, ip_network


@dataclass
class SubnetResult:
    input_cidr: str
    version: int
    network: str
    prefix_length: int
    netmask: str
    wildcard_mask: str
    broadcast_address: str | None
    total_addresses: int
    usable_hosts: int
    first_host: str
    last_host: str


def _wildcard_mask(network: IPv4Network) -> str:
    octets = [str(255 - int(part)) for part in str(network.netmask).split(".")]
    return ".".join(octets)


def calculate_subnet(cidr: str) -> SubnetResult:
    text = cidr.strip()
    if "/" not in text:
        raise ValueError("Input must include prefix length, for example: 192.168.1.0/24")

    try:
        network = ip_network(text, strict=False)
    except (AddressValueError, ValueError) as exc:
        raise ValueError("Enter a valid IPv4/IPv6 network in CIDR notation") from exc

    total_addresses = network.num_addresses

    if network.version == 4:
        ipv4_network = network
        wildcard_mask = _wildcard_mask(ipv4_network)
        broadcast = str(ipv4_network.broadcast_address)

        if ipv4_network.prefixlen == 32:
            first_host = str(ipv4_network.network_address)
            last_host = first_host
            usable_hosts = 1
        elif ipv4_network.prefixlen == 31:
            first_host = str(ipv4_network.network_address)
            last_host = str(ipv4_network.broadcast_address)
            usable_hosts = 2
        else:
            first_host = str(ipv4_network.network_address + 1)
            last_host = str(ipv4_network.broadcast_address - 1)
            usable_hosts = max(total_addresses - 2, 0)
    else:
        wildcard_int = ((1 << network.max_prefixlen) - 1) ^ int(network.netmask)
        wildcard_mask = str(IPv6Address(wildcard_int))
        broadcast = None
        first_host = str(network.network_address)
        last_host = str(network.broadcast_address)
        usable_hosts = total_addresses

    return SubnetResult(
        input_cidr=text,
        version=network.version,
        network=str(network.network_address),
        prefix_length=network.prefixlen,
        netmask=str(network.netmask),
        wildcard_mask=wildcard_mask,
        broadcast_address=broadcast,
        total_addresses=total_addresses,
        usable_hosts=usable_hosts,
        first_host=first_host,
        last_host=last_host,
    )

