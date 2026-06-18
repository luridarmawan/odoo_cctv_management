from odoo import fields
from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError


class TestCctvNvrMaintenance(TransactionCase):
    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)
        self.Nvr = self.env["cctv.nvr"]
        self.Maintenance = self.env["cctv.nvr.maintenance"]

        self.nvr = self.Nvr.create(
            {
                "name": "NVR Test",
                "asset_code": "NVR-MNT-TEST",
                "device_type": "nvr",
                "status": "active",
            }
        )

    def test_create_maintenance(self):
        m = self.Maintenance.create(
            {
                "nvr_id": self.nvr.id,
                "date": "2026-01-15",
                "type": "preventive",
                "description": "Routine check",
                "duration_hours": 1.5,
                "cost": 250000.0,
            }
        )
        self.assertEqual(m.nvr_id, self.nvr)
        self.assertEqual(m.type, "preventive")
        self.assertEqual(m.status, "scheduled")
        self.assertNotEqual(m.name, "New")
        self.assertTrue(m.name.startswith("MNT/"))

    def test_description_optional(self):
        m = self.Maintenance.create(
            {
                "nvr_id": self.nvr.id,
                "date": "2026-01-15",
                "type": "preventive",
            }
        )
        self.assertFalse(m.description)
        self.assertEqual(m.type, "preventive")

    def test_sequence_unique(self):
        m1 = self.Maintenance.create(
            {
                "nvr_id": self.nvr.id,
                "date": "2026-02-01",
                "type": "inspection",
                "description": "First",
            }
        )
        m2 = self.Maintenance.create(
            {
                "nvr_id": self.nvr.id,
                "date": "2026-02-02",
                "type": "inspection",
                "description": "Second",
            }
        )
        self.assertNotEqual(m1.name, m2.name)

    def test_maintenance_count(self):
        self.assertEqual(self.nvr.maintenance_count, 0)
        self.Maintenance.create(
            {
                "nvr_id": self.nvr.id,
                "date": "2026-03-01",
                "type": "preventive",
                "description": "A",
            }
        )
        self.Maintenance.create(
            {
                "nvr_id": self.nvr.id,
                "date": "2026-03-02",
                "type": "corrective",
                "description": "B",
            }
        )
        self.assertEqual(self.nvr.maintenance_count, 2)

    def test_last_maintenance_date(self):
        self.assertFalse(self.nvr.last_maintenance_date)
        self.Maintenance.create(
            {
                "nvr_id": self.nvr.id,
                "date": "2026-04-01",
                "type": "preventive",
                "description": "Older",
                "status": "done",
            }
        )
        newer = self.Maintenance.create(
            {
                "nvr_id": self.nvr.id,
                "date": "2026-05-15",
                "type": "corrective",
                "description": "Newer",
                "status": "done",
            }
        )
        self.assertEqual(
            self.nvr.last_maintenance_date,
            fields.Date.from_string("2026-05-15"),
        )
        # non-done maintenance should be ignored
        self.Maintenance.create(
            {
                "nvr_id": self.nvr.id,
                "date": "2099-01-01",
                "type": "preventive",
                "description": "Scheduled",
                "status": "scheduled",
            }
        )
        self.assertEqual(
            self.nvr.last_maintenance_date,
            fields.Date.from_string("2026-05-15"),
        )

    def test_action_mark_done(self):
        m = self.Maintenance.create(
            {
                "nvr_id": self.nvr.id,
                "date": "2026-01-10",
                "type": "preventive",
                "description": "X",
            }
        )
        m.action_mark_done()
        self.assertEqual(m.status, "done")

    def test_action_mark_cancelled(self):
        m = self.Maintenance.create(
            {
                "nvr_id": self.nvr.id,
                "date": "2026-01-10",
                "type": "preventive",
                "description": "X",
            }
        )
        m.action_mark_cancelled()
        self.assertEqual(m.status, "cancelled")

    def test_invalid_next_date(self):
        with self.assertRaises(ValidationError):
            self.Maintenance.create(
                {
                    "nvr_id": self.nvr.id,
                    "date": "2026-06-01",
                    "type": "preventive",
                    "description": "Bad",
                    "next_maintenance_date": "2026-05-01",
                }
            )

    def test_negative_duration(self):
        with self.assertRaises(ValidationError):
            self.Maintenance.create(
                {
                    "nvr_id": self.nvr.id,
                    "date": "2026-06-01",
                    "type": "preventive",
                    "description": "Bad",
                    "duration_hours": -1,
                }
            )

    def test_action_view_maintenance(self):
        action = self.nvr.action_view_maintenance()
        self.assertEqual(action["res_model"], "cctv.nvr.maintenance")
        self.assertIn(("nvr_id", "=", self.nvr.id), action["domain"])

