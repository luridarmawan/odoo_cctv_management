from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError


class TestCctvNvr(TransactionCase):
    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)
        self.Nvr = self.env["cctv.nvr"]
        self.LocationTag = self.env["cctv.location.tag"]

        self.tag = self.LocationTag.create({"name": "Server Room A"})

    def test_create_nvr(self):
        nvr = self.Nvr.create(
            {
                "name": "Test NVR",
                "asset_code": "NVR-001",
                "device_type": "nvr",
                "status": "active",
                "ip_address": "192.168.1.100",
                "brand": "Hikvision",
                "model": "DS-7608",
                "lokasi_ids": [(4, self.tag.id)],
            }
        )
        self.assertEqual(nvr.name, "Test NVR")
        self.assertEqual(nvr.asset_code, "NVR-001")
        self.assertEqual(nvr.device_type, "nvr")
        self.assertEqual(nvr.status, "active")
        self.assertIn(self.tag, nvr.lokasi_ids)

    def test_asset_code_unique(self):
        self.Nvr.create(
            {
                "name": "NVR 1",
                "asset_code": "UNIQUE-001",
                "device_type": "nvr",
            }
        )
        with self.assertRaises(Exception):
            self.Nvr.create(
                {
                    "name": "NVR 2",
                    "asset_code": "UNIQUE-001",
                    "device_type": "nvr",
                }
            )

    def test_invalid_ip_address(self):
        with self.assertRaises(ValidationError):
            self.Nvr.create(
                {
                    "name": "NVR Test",
                    "asset_code": "NVR-IP-TEST",
                    "device_type": "nvr",
                    "ip_address": "invalid-ip",
                }
            )

    def test_storage_validation(self):
        with self.assertRaises(ValidationError):
            self.Nvr.create(
                {
                    "name": "NVR Storage",
                    "asset_code": "NVR-STO-TEST",
                    "device_type": "nvr",
                    "storage_capacity_tb": 10.0,
                    "used_storage_tb": 15.0,
                }
            )

    def test_default_status_draft(self):
        nvr = self.Nvr.create(
            {
                "name": "NVR Default",
                "asset_code": "NVR-DEF-TEST",
                "device_type": "nvr",
            }
        )
        self.assertEqual(nvr.status, "draft")

    def test_camera_count(self):
        nvr = self.Nvr.create(
            {
                "name": "NVR With Cameras",
                "asset_code": "NVR-CAM-TEST",
                "device_type": "nvr",
            }
        )
        self.assertEqual(nvr.camera_count, 0)

        Camera = self.env["cctv.camera"]
        Camera.create(
            {
                "name": "Camera 1",
                "nvr_id": nvr.id,
                "channel": 1,
            }
        )
        Camera.create(
            {
                "name": "Camera 2",
                "nvr_id": nvr.id,
                "channel": 2,
            }
        )
        self.assertEqual(nvr.camera_count, 2)

    def test_tracking(self):
        nvr = self.Nvr.create(
            {
                "name": "NVR Track",
                "asset_code": "NVR-TRK-TEST",
                "device_type": "nvr",
            }
        )
        nvr.write({"status": "active"})
        self.assertEqual(nvr.status, "active")

    def test_public_access_valid(self):
        nvr = self.Nvr.create(
            {
                "name": "NVR Public",
                "asset_code": "NVR-PUB-TEST",
                "device_type": "nvr",
                "ip_address_public": "203.0.113.10",
                "port_public": "8080",
            }
        )
        self.assertEqual(nvr.ip_address_public, "203.0.113.10")
        self.assertEqual(nvr.port_public, "8080")

    def test_public_access_optional(self):
        nvr = self.Nvr.create(
            {
                "name": "NVR Internal",
                "asset_code": "NVR-INT-TEST",
                "device_type": "nvr",
            }
        )
        self.assertFalse(nvr.ip_address_public)
        self.assertEqual(nvr.port_public, False)
        self.assertNotEqual(nvr.port_public, 0)

    def test_invalid_ip_address_public(self):
        with self.assertRaises(ValidationError):
            self.Nvr.create(
                {
                    "name": "NVR Bad Public",
                    "asset_code": "NVR-BADPUB-TEST",
                    "device_type": "nvr",
                    "ip_address_public": "not-an-ip",
                    "port_public": "8080",
                }
            )

    def test_invalid_port_public_range(self):
        with self.assertRaises(ValidationError):
            self.Nvr.create(
                {
                    "name": "NVR Bad Port",
                    "asset_code": "NVR-BADPRT-TEST",
                    "device_type": "nvr",
                    "ip_address_public": "203.0.113.10",
                    "port_public": "70000",
                }
            )

    def test_invalid_port_public_non_numeric(self):
        with self.assertRaises(ValidationError):
            self.Nvr.create(
                {
                    "name": "NVR Bad Port Type",
                    "asset_code": "NVR-BADPRT2-TEST",
                    "device_type": "nvr",
                    "ip_address_public": "203.0.113.10",
                    "port_public": "abc",
                }
            )

    def test_public_access_partial_ip_only(self):
        with self.assertRaises(ValidationError):
            self.Nvr.create(
                {
                    "name": "NVR Partial 1",
                    "asset_code": "NVR-PRT1-TEST",
                    "device_type": "nvr",
                    "ip_address_public": "203.0.113.10",
                }
            )

    def test_public_access_partial_port_only(self):
        with self.assertRaises(ValidationError):
            self.Nvr.create(
                {
                    "name": "NVR Partial 2",
                    "asset_code": "NVR-PRT2-TEST",
                    "device_type": "nvr",
                    "port_public": "8080",
                }
            )
