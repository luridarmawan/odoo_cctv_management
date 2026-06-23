from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class CctvNvr(models.Model):
    _name = "cctv.nvr"
    _description = "CCTV NVR/DVR"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "id desc"

    DEVICE_TYPE = [
        ("nvr", "NVR"),
        ("dvr", "DVR"),
    ]

    STATUS = [
        ("draft", "Draft"),
        ("active", "Active"),
        ("maintenance", "Maintenance"),
        ("offline", "Offline"),
        ("retired", "Retired"),
    ]

    name = fields.Char(
        string="Name",
        required=True,
        tracking=True,
    )
    asset_code = fields.Char(
        string="Asset Code",
        copy=False,
        tracking=True,
        help="Optional. Unique asset code; leave blank to auto-generate.",
    )
    device_type = fields.Selection(
        selection=DEVICE_TYPE,
        string="Device Type",
        required=True,
        default="nvr",
    )
    status = fields.Selection(
        selection=STATUS,
        string="Status",
        required=True,
        default="draft",
        tracking=True,
    )
    brand = fields.Char(string="Brand")
    model = fields.Char(string="Model")
    device_domain = fields.Char(
        string="Device Domain",
        help="Device domain, hostname, or management URL (e.g. nvr.example.com "
             "or https://nvr.example.com)",
    )
    serial_number = fields.Char(string="Serial Number", copy=False)
    ip_address = fields.Char(
        string="IP Address",
        help="Internal/LAN IP address of the NVR/DVR device",
    )
    port = fields.Char(
        string="Port",
        help="Network port used to access the device on the internal network "
             "(e.g. 80, 8080, 554)",
    )
    ip_address_public = fields.Char(
        string="Public IP / Hostname",
        help="Public IP address or DDNS hostname used to access this device "
             "from outside the office network",
    )
    port_public = fields.Char(
        string="Public Port",
        help="Public-facing port exposed on the firewall/router for remote "
             "access to this device (1-65535). Leave blank if not used.",
    )
    mac_address = fields.Char(string="MAC Address")
    installation_date = fields.Date(string="Installation Date")
    warranty_end_date = fields.Date(string="Warranty End Date")
    channel_count = fields.Integer(
        string="Channel Count",
        help="Number of camera channels supported by this device",
    )
    storage_capacity_tb = fields.Float(
        string="Storage Capacity (TB)",
        help="Total storage capacity in Terabytes",
    )
    used_storage_tb = fields.Float(
        string="Used Storage (TB)",
        help="Currently used storage in Terabytes",
    )
    access_url = fields.Char(
        string="Access URL",
        compute="_compute_access_url",
        help="Click to access the device via browser (http://ip:port)",
    )
    access_url_public = fields.Char(
        string="Public Access URL",
        compute="_compute_access_url_public",
        help="Click to access the device publicly via browser (http://ip:port)",
    )
    firmware_version = fields.Char(string="Firmware Version")
    lokasi_ids = fields.Many2many(
        comodel_name="cctv.location.tag",
        string="Locations",
        help="Location tags for where this device is deployed",
    )
    notes = fields.Text(string="Notes")
    rtsp_url = fields.Char(string="RTSP URL")
    stream_url = fields.Char(string="Stream URL")
    resolution = fields.Char(
        string="Resolution",
        help="e.g. 1920x1080",
    )
    frame_rate = fields.Integer(string="Frame Rate (fps)")
    codec = fields.Char(string="Codec")

    camera_ids = fields.One2many(
        comodel_name="cctv.camera",
        inverse_name="nvr_id",
        string="Cameras",
    )
    camera_count = fields.Integer(
        string="Camera Count",
        compute="_compute_camera_count",
    )

    maintenance_ids = fields.One2many(
        comodel_name="cctv.nvr.maintenance",
        inverse_name="nvr_id",
        string="Maintenance History",
    )
    maintenance_count = fields.Integer(
        string="Maintenance Count",
        compute="_compute_maintenance_count",
    )
    last_maintenance_date = fields.Date(
        string="Last Maintenance Date",
        compute="_compute_last_maintenance_date",
        store=True,
    )

    _sql_constraints = [
        (
            "asset_code_unique",
            "UNIQUE(asset_code)",
            "Asset code must be unique across all devices.",
        ),
    ]

    @api.depends("camera_ids")
    def _compute_camera_count(self):
        for record in self:
            record.camera_count = len(record.camera_ids)

    @api.depends("ip_address", "port")
    def _compute_access_url(self):
        for record in self:
            if record.ip_address:
                url = f"http://{record.ip_address}"
                if record.port and record.port not in ('80', '0'):
                    url += f":{record.port}"
                record.access_url = url
            else:
                record.access_url = False

    @api.depends("ip_address_public", "port_public")
    def _compute_access_url_public(self):
        for record in self:
            if record.ip_address_public:
                url = f"http://{record.ip_address_public}"
                if record.port_public and record.port_public not in ('80', '0'):
                    url += f":{record.port_public}"
                record.access_url_public = url
            else:
                record.access_url_public = False

    @api.depends("maintenance_ids")
    def _compute_maintenance_count(self):
        for record in self:
            record.maintenance_count = len(record.maintenance_ids)

    @api.depends("maintenance_ids.date", "maintenance_ids.status")
    def _compute_last_maintenance_date(self):
        for record in self:
            done_maintenances = record.maintenance_ids.filtered(
                lambda m: m.status == "done"
            )
            if done_maintenances:
                record.last_maintenance_date = max(
                    done_maintenances.mapped("date") or [False]
                )
            else:
                record.last_maintenance_date = False

    def action_view_maintenance(self):
        self.ensure_one()
        return {
            "name": _("Maintenance History"),
            "type": "ir.actions.act_window",
            "res_model": "cctv.nvr.maintenance",
            "view_mode": "list,form",
            "domain": [("nvr_id", "=", self.id)],
            "context": {"default_nvr_id": self.id},
        }

    @api.constrains("ip_address")
    def _check_ip_address(self):
        for record in self:
            if record.ip_address:
                if record.ip_address.count(".") != 3:
                    raise ValidationError(
                        _("IP Address must be a valid IPv4 format (e.g. 192.168.1.1)")
                    )

    @api.constrains("ip_address_public")
    def _check_ip_address_public(self):
        for record in self:
            if record.ip_address_public:
                if record.ip_address_public.count(".") != 3:
                    raise ValidationError(
                        _(
                            "Public IP/Hostname must be a valid IPv4 format "
                            "(e.g. 203.0.113.10)"
                        )
                    )

    @api.constrains("port_public")
    def _check_port_public(self):
        for record in self:
            if record.port_public:
                if not record.port_public.isdigit():
                    raise ValidationError(
                        _("Public Port must be a numeric value between 1 and 65535.")
                    )
                port_value = int(record.port_public)
                if not (1 <= port_value <= 65535):
                    raise ValidationError(
                        _("Public Port must be between 1 and 65535.")
                    )

    @api.constrains("storage_capacity_tb", "used_storage_tb")
    def _check_storage(self):
        for record in self:
            if (
                record.used_storage_tb
                and record.storage_capacity_tb
                and record.used_storage_tb > record.storage_capacity_tb
            ):
                raise ValidationError(
                    _("Used storage cannot exceed total storage capacity.")
                )
