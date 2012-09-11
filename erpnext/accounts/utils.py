# ERPNext - web based ERP (http://erpnext.com)
# Copyright (C) 2012 Web Notes Technologies Pvt Ltd
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import webnotes
import webnotes.model
	
def get_balance_on(session, account, dt):
	acc = session.db.get_value('Account', account, \
		['lft', 'rgt', 'debit_or_credit', 'is_pl_account'], as_dict=1)
	cond = ""
	if acc.is_pl_account == 'Yes':
		year_start_date = session.db.sql("select year_start_date from `tabFiscal Year` \
			where year_start_date < %s order by year_start_date limit 1", dt)
		year_start_date = year_start_date and year_start_date[0][0] or ''
		cond += " and posting_date >= %s" % year_start_date
		
	bal = session.db.sql("""
		SELECT sum(ifnull(debit, 0)) - sum(ifnull(credit, 0)) 
		FROM `tabGL Entry`
		WHERE account in (select name from `tabAccount` where lft >= %s and rgt <= %s) 
		AND posting_date <= %s %s
	""", (acc['lft'], acc['rgt'], dt, cond))[0][0]
	
	if acc['debit_or_credit'] == 'Credit':
		bal = -bal
	return bal
