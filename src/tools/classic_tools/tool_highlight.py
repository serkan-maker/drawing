# tool_highlight.py
#
# Copyright 2018-2021 Romain F. T.
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

import cairo
from .tool_pencil import ToolPencil
from .utilities_paths import utilities_smooth_path
from .abstract_classic_tool import AbstractClassicTool

class ToolHighlighter(ToolPencil):
	__gtype_name__ = 'ToolHighlighter'

	def __init__(self, window, **kwargs):
		super().__init__(window)
		# Context: this is the name of a tool, a thick pencil dedicated to
		# highlight text, for example in screenshots
		AbstractClassicTool.__init__(self, 'highlight', _("Highlighter"), \
		                                      'tool-highlight-symbolic', window)
		self.add_tool_action_enum('highlight-bg', 'light')
		self.add_tool_action_boolean('highlight-alpha', True)

	def get_editing_tips(self):
		self._bg_type = self.get_option_value('highlight-bg')
		self._force_alpha = self.get_option_value('highlight-alpha')

		label_options = self.label + " - "
		if self._bg_type == 'light':
			label_options += _("Dark text on light background")
			label_modifier_shift = _("Press <Shift> to temporarily highlight" + \
			                                      " on dark background instead")
		else:
			label_options += _("Light text on dark background")
			label_modifier_shift = _("Press <Shift> to temporarily highlight" + \
			                                     " on light background instead")
		if self.get_image().get_mouse_is_pressed():
			label_modifier_shift = None

		full_list = [label_options, label_modifier_shift]
		return list(filter(None, full_list))

	def get_options_label(self):
		return _("Highlighter options")

	############################################################################

	def on_press_on_area(self, event, surface, event_x, event_y):
		super().on_press_on_area(event, surface, event_x, event_y)

		if 'SHIFT' in self._modifier_keys:
			if self._bg_type == 'light':
				self._bg_type = 'dark'
			else:
				self._bg_type = 'light'

	############################################################################

	def build_operation(self):
		operation = {
			'tool_id': self.id,
			'rgba': self.main_color,
			'width': self.tool_width,
			'path': self._path,
			'bg-type': self._bg_type,
			'halpha': self._force_alpha
		}
		return operation

	def do_tool_operation(self, operation):
		self.start_tool_operation(operation)
		if operation['path'] is None:
			return
		ccontext = self.get_context()
		ccontext.set_line_cap(cairo.LineCap.SQUARE)
		ccontext.set_line_join(cairo.LineJoin.ROUND)
		ccontext.set_line_width(operation['width'])

		if operation['bg-type'] == 'light':
			operator = cairo.Operator.MULTIPLY
		else:
			operator = cairo.Operator.SCREEN
		ccontext.set_operator(operator)

		main_color = operation['rgba']
		if operation['halpha']:
			main_color[3] = 0.5
		ccontext.set_source_rgba(*main_color)

		utilities_smooth_path(ccontext, operation['path'])
		ccontext.stroke()

	############################################################################
################################################################################

