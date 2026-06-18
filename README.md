## CCTV Management

**Language:** [🇬🇧 English](README.md) | [🇮🇩 Indonesia](README-id.md)

Odoo 19 addon for IT company NVR/CCTV inventory and management.

Part of the [odoo-boilerplate](https://github.com/luridarmawan/odoo-boilerplate) project for Odoo 19.

## Features

### Current Capabilities (Phase 1)

- **NVR/DVR Inventory** — Complete inventory management for Network Video Recorders and Digital Video Recorders.
- **Device Identity** — Track each device with unique asset code, serial number, MAC address, and IP address.
- **Device Specifications** — Record brand, model, firmware version, channel count, storage capacity (TB), and used storage (TB).
- **Device Lifecycle** — Manage installation date, warranty end date, and device status (`draft`, `active`, `maintenance`, `offline`, `retired`).
- **Stream Configuration** — Store RTSP URL, stream URL, resolution, frame rate, and codec for each NVR.
- **Location Tagging** — Flexible tagging system for locations, since a single NVR may serve cameras across multiple locations.
- **Dashboard** — Overview list of NVR/DVR devices showing name, IP address, and location.
- **Security Groups** — Role-based access control with three levels:
  - **CCTV User** — View data and reports
  - **CCTV Supervisor** — Create, edit, and manage maintenance
  - **CCTV Administrator** — Full access
- **Scalable Design** — Engineered to support from tens to thousands of CCTV devices.

### Planned Capabilities (Phase 2 and Beyond)

- **CCTV Camera Inventory** — Full camera lifecycle management linked to parent NVR.
- **PoE Switch Inventory** — Network infrastructure tracking for PoE switches.
- **ONVIF Integration** — Automatic device discovery and configuration.
- **RTSP Integration** — Live stream retrieval and validation.
- **Location Map** — Geographic visualization of CCTV placement.
- **Floor Plan View** — Building/floor-level device layout.
- **Automated Monitoring** — Periodic health checks of NVR and cameras.
- **Storage Monitoring** — Real-time tracking of NVR storage capacity.
- **Alert Integrations**:
  - Telegram notifications
  - WhatsApp notifications
  - Email notifications
- **AI Analytics** — Event detection and smart alerts.
- **Face Recognition** — Identity-aware video analytics.
- **License Plate Recognition (LPR)** — Vehicle identification at entry/exit points.

### Module Structure

```
cctv_management/
├── models/      # ORM models (e.g., cctv.nvr)
├── views/       # Tree, form, search, and menu views
├── security/    # Access rights, security groups, record rules
├── data/        # Default and demo data
├── report/      # PDF and QWeb reports
├── wizard/      # Transient models for guided workflows
├── static/      # Assets (CSS, JS, images)
└── tests/       # Unit and integration tests
```

### Technical Highlights

- Built on **Odoo 19** using the **ORM** (no raw SQL).
- Constraints and validation for data integrity.
- Computed fields where appropriate.
- Help text on key fields for better UX.
- Selection fields for fixed enumerations.
- Forward-compatible schema to support all planned features without breaking changes.

## Screenshots

### Dashboard

![Dashboard](docs/home.png)

### NVR Detail

![NVR Detail](docs/nvr-detail.png)



## Installation

### Traditional Installation

1. Copy this folder to your Odoo addons directory:

```bash
cp -r device_management /path/to/odoo/addons/
```

2. Restart Odoo service:

```bash
sudo systemctl restart odoo
# or
sudo service odoo restart
```

3. Open Odoo, enable *Developer Mode* (Settings → Activate Developer Mode).

4. Go to **Apps → Update Apps List**.

5. Search for **Device Management**, then click **Install**.

### Alternative via Git Clone

```bash
cd /path/to/odoo/addons
git clone <repo-url> device_management
```

Proceed to steps 2-5 above.

### Docker Installation

If you are using the [odoo-boilerplate](https://github.com/luridarmawan/odoo-boilerplate) with Docker:

1. Clone this repository into the `addons/` directory:

```bash
cd /path/to/odoo-boilerplate/addons
git clone <repo-url> cctv_management
```

2. Restart the Docker containers:

```bash
docker compose restart
```

3. Open Odoo, enable *Developer Mode* (Settings → Activate Developer Mode).

4. Go to **Apps → Update Apps List**.

5. Search for **CCTV Management**, then click **Install**.


