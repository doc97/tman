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

    $(".task-description").click(function(event) {
        elem = $(event.target).parent().parent().parent().parent().parent();
        elem.css("display", "none");

        htmlElem = "\
        <li class='task-edit task'> \
            <form> \
                <table style='width: 100%'> \
                    <tr> \
                        <td> \
                            <div id='edit-task-description' class='text-edit' autofocus contentEditable='true'></div> \
                        </td> \
                    </tr> \
                </table> \
                <table> \
                    </tr> \
                        <td><a href='#' id='task-edit-submit'>Save</a></td> \
                        <td><a href='#' id='task-edit-cancel' class='cancel'>Cancel</a></td> \
                    </tr> \
                </table> \
            </form> \
        </li> \
        ";
        elem.after(htmlElem);
        inputField = $("#edit-task-description");
        inputField.html($(event.target).text());
        inputField.focus();
        setEndOfContenteditable(inputField.get(0));

        $("#task-edit-submit").click(function(event) {
            editElem = $(event.target).parent().parent().parent().parent().parent().parent();
            dataElem = editElem.find("#edit-task-description");
            updatedElem = editElem.prev();
            updatedElem.css("display", "");

            jsonData = JSON.stringify({ task_id: updatedElem.attr("id"), desc: dataElem.text() }, null, '\t');
            $.ajax({
                type: "POST",
                url: "/tasks/update",
                data: jsonData,
                contentType: "application/json;charset=UTF-8",
                success: function(description) {
                    if (!!description)
                        updatedElem.find(".task-description").html(description);
                }
            });

            editElem.remove();
        });

        $("#task-edit-cancel").click(function(event) {
            editElem = $(event.target).parent().parent().parent().parent().parent().parent();
            editElem.prev().css("display", "");
            editElem.remove();
        });
    });

    // Source: https://stackoverflow.com/a/3866442
    function setEndOfContenteditable(contentEditableElement) {
        var range,selection;
        if(document.createRange) { //Firefox, Chrome, Opera, Safari, IE 9+
            range = document.createRange();//Create a range (a range is a like the selection but invisible)
            range.selectNodeContents(contentEditableElement);//Select the entire contents of the element with the range
            range.collapse(false);//collapse the range to the end point. false means collapse to end rather than the start
            selection = window.getSelection();//get the selection object (allows you to change selection)
            selection.removeAllRanges();//remove any selections already made
            selection.addRange(range);//make the range you have just created the visible selection
        } else if(document.selection) { //IE 8 and lower
            range = document.body.createTextRange();//Create a range (a range is a like the selection but invisible)
            range.moveToElementText(contentEditableElement);//Select the entire contents of the element with the range
            range.collapse(false);//collapse the range to the end point. false means collapse to end rather than the start
            range.select();//Select the range (make it the visible selection
        }
    }
});
