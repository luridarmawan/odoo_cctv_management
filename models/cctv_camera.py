from odoo import fields, models


class CctvCamera(models.Model):
    _name = "cctv.camera"
    _description = "CCTV Camera"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "id desc"

    nvr_id = fields.Many2one(
        comodel_name="cctv.nvr",
        string="NVR/DVR",
        required=True,
        ondelete="cascade",
    )
    name = fields.Char(
        string="Name",
        required=True,
        tracking=True,
    )
    channel = fields.Integer(
        string="Channel",
        help="Channel number on the NVR/DVR",
    )
    status = fields.Selection(
        selection=[
            ("draft", "Draft"),
            ("active", "Active"),
            ("maintenance", "Maintenance"),
            ("offline", "Offline"),
            ("retired", "Retired"),
        ],
        string="Status",
        required=True,
        default="draft",
        tracking=True,
    )
    ip_address = fields.Char(string="IP Address")
    rtsp_url = fields.Char(string="RTSP URL")
    stream_url = fields.Char(string="Stream URL")
    resolution = fields.Char(string="Resolution")
    frame_rate = fields.Integer(string="Frame Rate (fps)")
    codec = fields.Char(string="Codec")
    lokasi_ids = fields.Many2many(
        comodel_name="cctv.location.tag",
        string="Locations",
    )
    notes = fields.Text(string="Notes")
