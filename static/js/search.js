function addTag(caller, tag) { /* Adds a tag to the query on the page */
    $(caller).addClass("query");
    $("#id_q").val($("#id_q").val() + ' "' + tag + '"');
}
