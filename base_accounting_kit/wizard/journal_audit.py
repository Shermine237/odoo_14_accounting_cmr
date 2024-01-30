#    (LGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################

from odoo import fields, models


class AccountPrintJournal(models.TransientModel):
    _inherit = "account.journal"
    _name = "account.print.journal"
    _description = "Account Print Journal"


    name = fields.Char(string="Journal Audit", default="Journal Audit", required=True, translate=True)
    sort_selection = fields.Selection(
        [('date', 'Date'), ('move_name', 'Journal Entry Number')],
        'Entries Sorted by', required=True, default='move_name')
    journal_ids = fields.Many2many('account.journal', string='Journals',
                                   required=True,
                                   default=lambda self: self.env[
                                       'account.journal'].search(
                                       [('type', 'in', ['sale', 'purchase'])]))
    
    account_control_ids = fields.Many2many(
        comodel_name='account.account',
        relation='print_journal_account_control_rel',
        column1='print_journal_id',
        column2='account_control_id',
        string='Account Controls'
    )

    def _print_report(self, data):
        data = self.pre_print_report(data)
        data['form'].update({'sort_selection': self.sort_selection})
        return self.env.ref(
            'base_accounting_kit.action_report_journal').with_context(
            landscape=True).report_action(self, data=data)