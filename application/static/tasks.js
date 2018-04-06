$(function() {
    $(".complete-btn").click(function(event) {
        taskId = $(event.target).parent().parent().parent().parent().parent().attr("id");
        jsonData = JSON.stringify({ task_id: taskId }, null, '\t');
        $.ajax({
            type: "POST",
            url: "/tasks/complete",
            data: jsonData,
            contentType: "application/json;charset=UTF-8",
            success: function(redirect_url) {
                window.location.href = redirect_url;
            }
        });
    });

    $(".delete-btn").click(function(event) {
        taskId = $(event.target).parent().parent().parent().parent().parent().attr("id");
        jsonData = JSON.stringify({ task_id: taskId }, null, '\t');
        $.ajax({
            type: "POST",
            url: "/tasks/delete",
            data: jsonData,
            contentType: "application/json;charset=UTF-8",
            success: function(redirect_url) {
                window.location.href = redirect_url;
            }
        });
    });
});
