/**
 * Created by david on 7/20/15.
 */
window.gallant = {
    humanize: function (str) {
        var frags = str.split('_');
        for (i = 0; i < frags.length; i++) {
            frags[i] = frags[i].charAt(0).toUpperCase() + frags[i].slice(1);
        }
        return frags.join(' ');
    },

    /**
     * Copy element val() into destination, based on selector.
     */
    copyElement: function (destination, source, selector) {
        var el = $(source).find(selector).first();
        var el_dest = $(destination).find(selector).first();

        if (el.attr('type') == 'checkbox') {
            $(el_dest).prop('checked', $(el).prop('checked'));
        } else {
            el_dest.val(el.val());
        }
    }
}

String.prototype.format = function () {
    var num = arguments.length;
    var str = this;
    for (var i = 0; i < num; i++) {
        var pattern = "\\{" + i + "\\}";
        var re = new RegExp(pattern, "g");
        str = str.replace(re, arguments[i]);
    }
    return str;
}