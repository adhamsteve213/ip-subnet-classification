from django.test import TestCase

from subnetcalc.services import calculate_subnet


class SubnetServiceTests(TestCase):
    def test_ipv4_subnet(self):
        result = calculate_subnet("192.168.10.44/24")

        self.assertEqual(result.network, "192.168.10.0")
        self.assertEqual(result.broadcast_address, "192.168.10.255")
        self.assertEqual(result.first_host, "192.168.10.1")
        self.assertEqual(result.last_host, "192.168.10.254")
        self.assertEqual(result.usable_hosts, 254)

    def test_ipv6_subnet(self):
        result = calculate_subnet("2001:db8::1/64")

        self.assertEqual(result.version, 6)
        self.assertEqual(result.network, "2001:db8::")
        self.assertIsNone(result.broadcast_address)


class SubnetViewTests(TestCase):
    def test_get_page(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "IP Subnet Calculator")

    def test_post_valid_cidr(self):
        response = self.client.post("/", data={"cidr": "10.0.0.1/24"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "10.0.0.0")

    def test_post_invalid_cidr(self):
        response = self.client.post("/", data={"cidr": "not-an-ip"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Input must include prefix length")

