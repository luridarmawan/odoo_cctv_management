{
    "name": "CCTV Management",
    "version": "19.0.1.5.0",
    "summary": "Manage CCTV infrastructure (NVR/DVR, cameras)",
    "description": """
        CCTV Management Module for Odoo 19.
        Manage NVR/DVR, CCTV cameras, and PoE switches infrastructure.
    """,
    "author": "IT Department",
    "website": "",
    "category": "Operations",
    "depends": ["base", "mail"],
    "data": [
        "security/cctv_security.xml",
        "security/ir.model.access.csv",
        "data/cctv_nvr_maintenance_sequence.xml",
        "views/cctv_location_tag_views.xml",
        "views/cctv_nvr_views.xml",
        "views/cctv_nvr_maintenance_views.xml",
        "views/cctv_menu.xml",
    ],
    "demo": [],
    "assets": {
        "web.assets_backend": [
            "cctv_management/static/src/**/*",
        ],
    },
    "license": "LGPL-3",
    "installable": True,
    "application": True,
    "auto_install": False,
}
