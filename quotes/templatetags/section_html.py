from django import template
import re
from django.utils.html import escape, mark_safe

register = template.Library()

table_html = """
        <tbody id="{0}" class="section">
        <tr>
            <td>
                <label class="control-label  " for="id_{0}">{1}</label>
            </td>
            <td>
                <button id="{0}_remove" type="button" class="close" data-dismiss="alert" aria-label="Close">
                    <span aria-hidden="true">&times;</span>
                </button>
            </td>
        </tr>
        <tr>
            <td>Title:&nbsp;&nbsp;</td>
            <td><input class="ultext" type="hidden" id="id_{0}_title_hidden" name="{0}_title"
                       for="id_{0}_title" value="{2}"/>
                <input class="form-control" id="id_{0}_title" maxlength="512"
                       type="text" value=""/></td>
        </tr>
        <tr>
            <td>Content:&nbsp;&nbsp;</td>
            <td><input class="ultext" type="hidden" id="id_{0}_text_hidden" name="{0}_text"
                       for="id_{0}_text" value="{3}"/>
                <textarea rows="5" style="width:100%;" id="id_{0}_text"></textarea>
            </td>
        </tr>
        </tbody>
"""


def section_form_html(section_name, display_name, title_json, text_json):
    return mark_safe(table_html.format(escape(section_name), escape(display_name),
                                       escape(title_json), escape(text_json)))


@register.simple_tag
def section_form_javascript():
    """Returns a javascript string to be used with gallant.js's format function
    """
    return re.sub(r'(.*)', r"'\1' +", table_html.format('{0}', '{1}', '', '')) + "''"