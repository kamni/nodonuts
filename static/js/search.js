function toggleTag(caller, tag) { /* Adds or removes a tag to the query on the page */
    tagsInput = $("#id_tags")
    query = tagsInput.val();
    if (query.indexOf(tag) >= 0) {
        tagsInput.val(query.replace(tag, "").replace(/\s+/g, ' ').replace(/(^\s+|\s+$)/g, ''));
        $(caller).removeClass("query");
    }
    else {
        if (query !== "") {
            query = query + " "
        }
        tagsInput.val(query + tag);
        $(caller).addClass("query");
    }
}
