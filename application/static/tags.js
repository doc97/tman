$(function() {
    $(".edit-tag-btn").click(editTagBtnClick);
    $(".delete-tag-btn").click(deleteTagBtnClick);

    function editTagBtnClick(event) {
        tagId = $(this).parent().parent().parent().attr("id");
        window.location.href = "/tags/edit?tag=" + tagId;
    }

    function deleteTagBtnClick(event) {
        tagId = $(this).parent().parent().parent().attr("id");
        jsonData = JSON.stringify({ tag_id: tagId }, null, '\t');
        $.ajax({
            type: "POST",
            url: "/tags/delete",
            data: jsonData,
            contentType: "application/json;charset=UTF-8",
            success: function(redirect_url) {
                window.location.href = redirect_url;
            }
        });
    }
});
