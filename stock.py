# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import fields
from trytond.pyson import Eval
from trytond.pool import Pool, PoolMeta
from trytond.transaction import Transaction

__all__ = ['Lot']
__metaclass__ = PoolMeta


class Lot:
    __name__ = 'stock.lot'

    supplier_ref = fields.Char('Supplier Reference')

    @classmethod
    def __setup__(cls):
        super(Lot, cls).__setup__()
        cls._sql_constraints += [
            ('unique_lot_supplier_ref', 'UNIQUE(number, supplier_ref)',
                'Supplier ref per lot must be unique'),
            ]

    def get_rec_name(self, name):
        res = super(Lot, self).get_rec_name(name)
        if self.supplier_ref and len(self.supplier_ref) > 0:
            res += '/%s' % (self.supplier_ref)
        return res

    @classmethod
    def search_rec_name(cls, name, clause):
        lots = cls.search([('supplier_ref',) + tuple(clause[1:])], order=[])
        if lots:
            lots += cls.search([('number',) + tuple(clause[1:])], order=[])

            return [('id', 'in', [lot.id for lot in lots])]
        return [('number',) + tuple(clause[1:])]
