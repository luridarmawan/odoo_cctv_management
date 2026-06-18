from odoo import fields, models


class CctvLocationTag(models.Model):
    _name = "cctv.location.tag"
    _description = "CCTV Location Tag"
    _order = "name"

    name = fields.Char(string="Name", required=True, translate=True)
    color = fields.Integer(string="Color")
    parent_id = fields.Many2one(
        comodel_name="cctv.location.tag",
        string="Parent Tag",
    )
    child_ids = fields.One2many(
        comodel_name="cctv.location.tag",
        inverse_name="parent_id",
        string="Child Tags",
    )
