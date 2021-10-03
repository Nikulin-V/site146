jQuery.fn.myAddClass = function (classTitle) {
    return this.each(function () {
        var oldClass = jQuery(this).attr("class");
        oldClass = oldClass ? oldClass : '';
        jQuery(this).attr("class", (oldClass + " " + classTitle).trim());
    });
}
jQuery.fn.myRemoveClass = function (classTitle) {
    return this.each(function () {
        var oldClassString = ' ' + jQuery(this).attr("class") + ' ';
        var newClassString = oldClassString.replace(new RegExp(' ' + classTitle + ' ', 'g'), ' ').trim()
        if (!newClassString)
            jQuery(this).removeAttr("class");
        else
            jQuery(this).attr("class", newClassString);
    });
}
$(window).load(function () {
    var svgobject = document.getElementById('floorplan');
    if ('contentDocument' in svgobject)
        var svgdom = svgobject.contentDocument;
});
$(svgdom.getElementsByClassName("room")).hover(
    function () {
        var id = $(this).attr("id");
        $("#" + id, svgdom).myAddClass("highlight");
    },
    function () {
        var id = $(this).attr("id");
        $("#" + id, svgdom).myRemoveClass("highlight");
    }
);