from odoo import models, fields, api

class ProductTemplate(models.Model):
    _inherit = 'product.template'
    
    is_kit = fields.Boolean(string='Is Kit Product', compute='_compute_is_kit', store=True)
    calculated_weight = fields.Float(string='Calculated Weight', compute='_compute_kit_measurements', store=True)
    calculated_volume = fields.Float(string='Calculated Volume', compute='_compute_kit_measurements', store=True)
    update_measurements = fields.Boolean(string='Auto-update Measurements', default=True,
                                        help="If checked, weight and volume will be automatically updated from kit components")
    
    @api.depends('bom_ids', 'bom_ids.type')
    def _compute_is_kit(self):
        for product in self:
            kit_boms = self.env['mrp.bom'].search([
                ('product_tmpl_id', '=', product.id),
                ('type', '=', 'phantom')
            ])
            product.is_kit = bool(kit_boms)
    
    @api.depends('bom_ids', 'bom_ids.bom_line_ids', 'bom_ids.bom_line_ids.product_id', 
                 'bom_ids.bom_line_ids.product_qty', 'is_kit', 'update_measurements')
    def _compute_kit_measurements(self):
        for product in self:
            if not product.is_kit:
                product.calculated_weight = product.weight
                product.calculated_volume = product.volume
                continue
                
            kit_boms = self.env['mrp.bom'].search([
                ('product_tmpl_id', '=', product.id),
                ('type', '=', 'phantom')
            ], limit=1)
            
            if not kit_boms:
                product.calculated_weight = product.weight
                product.calculated_volume = product.volume
                continue
                
            total_weight = 0.0
            total_volume = 0.0
            
            for line in kit_boms.bom_line_ids:
                total_weight += line.product_id.weight * line.product_qty
                total_volume += line.product_id.volume * line.product_qty
                
            product.calculated_weight = total_weight
            product.calculated_volume = total_volume
            
            # Update actual weight and volume fields if auto-update is enabled
            if product.update_measurements:
                if total_weight > 0:
                    product.weight = total_weight
                if total_volume > 0:
                    product.volume = total_volume
    
    def action_update_kit_measurements(self):
        """Manual button to update measurements from kit components"""
        for product in self:
            kit_boms = self.env['mrp.bom'].search([
                ('product_tmpl_id', '=', product.id),
                ('type', '=', 'phantom')
            ], limit=1)
            
            if not kit_boms:
                continue
                
            total_weight = 0.0
            total_volume = 0.0
            
            for line in kit_boms.bom_line_ids:
                total_weight += line.product_id.weight * line.product_qty
                total_volume += line.product_id.volume * line.product_qty
                
            if total_weight > 0:
                product.weight = total_weight
            if total_volume > 0:
                product.volume = total_volume
                
        return True

class MrpBomLine(models.Model):
    _inherit = 'mrp.bom.line'
    
    @api.model_create_multi
    def create(self, vals_list):
        lines = super(MrpBomLine, self).create(vals_list)
        # Trigger recomputation of kit measurements when BOM lines are created
        for line in lines:
            if line.bom_id.type == 'phantom':
                line.bom_id.product_tmpl_id._compute_kit_measurements()
        return lines
    
    def write(self, vals):
        result = super(MrpBomLine, self).write(vals)
        # Trigger recomputation of kit measurements when BOM lines are updated
        if 'product_id' in vals or 'product_qty' in vals:
            for line in self:
                if line.bom_id.type == 'phantom':
                    line.bom_id.product_tmpl_id._compute_kit_measurements()
        return result
    
    def unlink(self):
        phantom_product_tmpls = self.env['product.template']
        for line in self:
            if line.bom_id.type == 'phantom':
                phantom_product_tmpls |= line.bom_id.product_tmpl_id
        
        result = super(MrpBomLine, self).unlink()
        
        # Trigger recomputation after deletion
        if phantom_product_tmpls:
            phantom_product_tmpls._compute_kit_measurements()
        
        return result
