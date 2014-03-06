function toggleTag(caller, tag) { /* Adds or removes a tag to the query on the page */
    query = $("#id_q").val();
    quotedTag = '"' + tag + '"';
    if (query.indexOf(quotedTag) >= 0) {
        $("#id_q").val(query.replace(quotedTag, ""));
        $(caller).removeClass("query");
    }
    else {
        $("#id_q").val(query + " " + quotedTag);
        $(caller).addClass("query");
    }
}
