/**
 * Created by david on 7/20/15.
 */
function humanize(str) {
  var frags = str.split('_');
  for (i=0; i<frags.length; i++) {
    frags[i] = frags[i].charAt(0).toUpperCase() + frags[i].slice(1);
  }
  return frags.join(' ');
}

String.prototype.format = function() {
  var num = arguments.length;
  var str = this;
  for (var i = 0; i < num; i++) {
    var pattern = "\\{" + i + "\\}";
    var re = new RegExp(pattern, "g");
    str = str.replace(re, arguments[i]);
  }
  return str;
}