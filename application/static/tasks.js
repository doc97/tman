$(function() {
    $(".task").click(function(event) {
        jsonData = JSON.stringify({ task_id: event.target.id }, null, '\t');
        $.ajax({
            type: "POST",
            url: "/complete_task",
            data: jsonData,
            contentType: 'application/json;charset=UTF-8',
            success: function(redirect_url) {
                window.location.href = redirect_url;
            }
        });
    });
});
