function toggleTag(caller, tag) { /* Adds or removes a tag to the query on the page */
    tagsInput = $("#id_tags")
    query = tagsInput.val();
    if (query.indexOf(tag) >= 0) {
        tagsInput.val(query.replace(tag, ""));
        $(caller).removeClass("query");
    }
    else {
        if (query !== "") {
            query = query + ", "
        }
        tagsInput.val(query + tag);
        $(caller).addClass("query");
    }
}
