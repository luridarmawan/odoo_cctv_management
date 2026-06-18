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
