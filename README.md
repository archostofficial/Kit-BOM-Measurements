# Kit BOM Measurements Module Installation Guide

This module automatically calculates the weight and volume of kit BOMs (phantom BOMs) based on their components and updates the parent product's measurements accordingly.

## Installation Steps

1. **Download the module files**
   - Save all the provided code files maintaining the directory structure as shown below:

   ```
   kit_bom_measurements/
   ├── __init__.py
   ├── __manifest__.py
   ├── models/
   │   ├── __init__.py
   │   └── product.py
   ├── views/
   │   └── product_views.xml
   └── security/
       └── ir.model.access.csv
   ```

2. **Place the module in your Odoo addons directory**
   - Copy the entire `kit_bom_measurements` folder to your Odoo server's addons directory
   - This is typically located at `/usr/lib/python3/dist-packages/odoo/addons/` or a custom addons path you've configured

3. **Update the Odoo apps list**
   - Go to Apps menu
   - Click "Update Apps List" in the menu
   - Confirm by clicking "Update"

4. **Install the module**
   - Search for "Kit BOM Measurements" in the Apps list
   - Click "Install" on the module

5. **Verify installation**
   - Go to a product that has a kit/phantom BOM
   - Check the Inventory tab to ensure you can see the new fields and button

## How It Works

After installation, the module will:

1. Automatically identify products with kit (phantom) BOMs
2. Calculate their total weight and volume based on the components
3. Update the product's actual weight and volume fields (if auto-update is enabled)
4. Provide a manual update button for on-demand recalculation

## Settings and Options

- **Auto-update Measurements**: When enabled (default), the product's weight and volume will be automatically updated whenever its kit components change
- **Calculated Weight/Volume**: Shows the computed values from components (for reference)
- **Update From Kit Components**: Button to manually trigger an update

## Troubleshooting

If the values are not updating automatically:

1. Ensure the product has a phantom (kit) BOM type
2. Verify all components have weight and volume values set
3. Check that the "Auto-update Measurements" option is enabled
4. Try using the manual update button
5. Restart the Odoo server if necessary to ensure all code is properly loaded

## Fix for Odoo 18 Error with attrs and states

If you encounter an error about "attrs" and "states" attributes no longer being used in Odoo 18, this is already fixed in the current version. The module uses visibility groups instead of conditional attributes to control field visibility.

For any other issues, check the Odoo server logs for error messages.
