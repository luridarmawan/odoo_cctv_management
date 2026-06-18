/** @odoo-module **/
import { registry } from "@web/core/registry";
import { CharField, charField } from "@web/views/fields/char/char_field";

export class CctvNvrIPAddressField extends CharField {
    static template = "cctv_management.NonNavigableIPField";
}

export const cctvNvrIPAddressField = {
    ...charField,
    component: CctvNvrIPAddressField,
};

registry.category("fields").add("cctv.ip_address_no_nav", cctvNvrIPAddressField);
