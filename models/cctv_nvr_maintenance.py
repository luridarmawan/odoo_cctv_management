from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class CctvNvrMaintenance(models.Model):
    _name = "cctv.nvr.maintenance"
    _description = "CCTV NVR/DVR Maintenance History"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "date desc, id desc"
    _rec_name = "name"

    MAINTENANCE_TYPE = [
        ("preventive", "Preventive"),
        ("corrective", "Corrective"),
        ("inspection", "Inspection"),
        ("firmware_update", "Firmware Update"),
        ("hardware_replacement", "Hardware Replacement"),
        ("cleaning", "Cleaning"),
        ("configuration", "Configuration"),
        ("other", "Other"),
    ]

    STATUS = [
        ("scheduled", "Scheduled"),
        ("in_progress", "In Progress"),
        ("done", "Done"),
        ("cancelled", "Cancelled"),
    ]

    PRIORITY = [
        ("0", "Low"),
        ("1", "Normal"),
        ("2", "High"),
        ("3", "Urgent"),
    ]

    name = fields.Char(
        string="Reference",
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: _("New"),
    )
    nvr_id = fields.Many2one(
        comodel_name="cctv.nvr",
        string="NVR/DVR",
        required=True,
        ondelete="cascade",
        index=True,
        tracking=True,
    )
    device_type = fields.Selection(
        related="nvr_id.device_type",
        string="Device Type",
        store=True,
    )
    date = fields.Date(
        string="Maintenance Date",
        required=True,
        default=fields.Date.context_today,
        tracking=True,
    )
    type = fields.Selection(
        selection=MAINTENANCE_TYPE,
        string="Type",
        required=True,
        default="preventive",
        tracking=True,
    )
    status = fields.Selection(
        selection=STATUS,
        string="Status",
        required=True,
        default="scheduled",
        tracking=True,
    )
    priority = fields.Selection(
        selection=PRIORITY,
        string="Priority",
        default="1",
    )
    technician_id = fields.Many2one(
        comodel_name="res.users",
        string="Technician",
        tracking=True,
        help="User responsible for performing the maintenance",
    )
    duration_hours = fields.Float(
        string="Duration (hours)",
        help="Total time spent on the maintenance activity",
    )
    cost = fields.Float(
        string="Cost",
        digits="Product Price",
        help="Total cost incurred (parts, services, etc.)",
    )
    currency_id = fields.Many2one(
        comodel_name="res.currency",
        string="Currency",
        related="company_id.currency_id",
    )
    company_id = fields.Many2one(
        comodel_name="res.company",
        string="Company",
        default=lambda self: self.env.company,
    )
    parts_replaced = fields.Text(
        string="Parts Replaced",
        help="List of parts/components replaced during maintenance",
    )
    next_maintenance_date = fields.Date(
        string="Next Maintenance Date",
        help="Recommended date for the next maintenance",
    )
    description = fields.Text(
        string="Description",
        help="Describe the issue, action taken, and outcome",
    )
    result = fields.Text(
        string="Result / Resolution",
        help="Outcome of the maintenance, follow-up actions needed",
    )
    downtime_minutes = fields.Integer(
        string="Downtime (minutes)",
        help="Service downtime caused by this maintenance",
    )

    _check_duration_non_negative = models.Constraint(
        "CHECK(duration_hours >= 0)",
        "Duration cannot be negative.",
    )
    _check_cost_non_negative = models.Constraint(
        "CHECK(cost >= 0)",
        "Cost cannot be negative.",
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("name", _("New")) == _("New"):
                vals["name"] = self.env["ir.sequence"].next_by_code(
                    "cctv.nvr.maintenance"
                ) or _("New")
            if vals.get("duration_hours") is not None and vals["duration_hours"] < 0:
                raise ValidationError(_("Duration cannot be negative."))
            if vals.get("cost") is not None and vals["cost"] < 0:
                raise ValidationError(_("Cost cannot be negative."))
        records = super().create(vals_list)
        records._validate_non_stored_fields()
        return records

    def write(self, vals):
        result = super().write(vals)
        self._validate_non_stored_fields()
        return result

    def _validate_non_stored_fields(self):
        for record in self:
            if (
                record.date
                and record.next_maintenance_date
                and record.next_maintenance_date < record.date
            ):
                raise ValidationError(
                    _(
                        "Next maintenance date cannot be earlier than the "
                        "maintenance date."
                    )
                )

    @api.constrains("date", "next_maintenance_date")
    def _check_dates(self):
        self._validate_non_stored_fields()

    def action_mark_done(self):
        for record in self:
            record.status = "done"

    def action_mark_cancelled(self):
        for record in self:
            record.status = "cancelled"

    def action_set_in_progress(self):
        for record in self:
            record.status = "in_progress"
