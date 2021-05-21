# -*- coding: utf-8 -*-
##############################################################################
#
#    This module you will be able to work whit the calculator within the odoo framework
#    itself without having to leave it.
#
#    Copyright (C) 2020- todooweb.com (https://www.todooweb.com)
#    @author ToDOO (https://www.linkedin.com/company/todooweb)
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################
{
    'name': "Integrated Calculator",
    'summary': """Integrated Calculator within the odoo framework""",
    'description': """Integrated Calculator within the odoo framework. Allows for multiple calculations. 
    """,
    'version': '14.0.0.0.1',
    'category': 'Tools',
    'license': 'LGPL-3',
    'author': "ToDOO (www.todooweb.com)",
    'website': "https://todooweb.com/",
    'contributors': [
        "Equipo Dev <devtodoo@gmail.com>",
        "Edgar Naranjo <edgarnaranjof@gmail.com>",
        "Tatiana Rosabal <tatianarosabal@gmail.com>",
        "Antonio Ruban <antoniodavid8@gmail.com>",
    ],
    'support': 'devtodoo@gmail.com',
    'depends': [
        'base',
        'web'
    ],
    'data': [
        'views/templates.xml',
    ],
    'qweb': ['static/src/xml/*.xml'],
    'images': [
        'static/description/screenshot_calculator.png'
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}