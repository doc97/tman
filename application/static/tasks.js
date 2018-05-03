$(function() {
    $(".complete-task-btn").click(completeTaskBtnClick);
    $(".undo-task-btn").click(undoTaskBtnClick);
    $(".delete-task-btn").click(deleteTaskBtnClick);
    $(".overflow-icon").click(overflowIconClick);
    $(".task-content").click(taskContentClick);

    $( "#sortable" ).sortable({
        handle: ".sortable-handle",
        axis: "y",
        start: function(event, ui) {
            ui.item.data("previndex", ui.item.index());
        },
        update: function(event, ui) {
            diff = ui.item.index() - ui.item.data("previndex");
            ui.item.removeData("previndex");
            orderTask(ui.item.attr("id"), diff);
        }
    }).disableSelection();

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

    /* Click functions */

    function completeTaskBtnClick(event) {
        taskId = $(this).parent().parent().parent().attr("id");
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
    }

    function undoTaskBtnClick(event) {
        taskId = $(this).parent().parent().parent().attr("id");
        jsonData = JSON.stringify({ task_id: taskId }, null, '\t');
        $.ajax({
            type: "POST",
            url: "/tasks/undo",
            data: jsonData,
            contentType: "application/json;charset=UTF-8",
            success: function(redirect_url) {
                window.location.href = redirect_url;
            }
        });
    }

    function deleteTaskBtnClick(event) {
        taskId = $(this).parent().parent().parent().attr("id");
        deleteTask(taskId);
    }

    function overflowIconClick(event) {
        $(document).on("mouseup.hideOverflowMenu", function(event) {
            if (!$(event.target).is(".overflow-list *, .overflow-list")) {
                $(".task-selected").removeClass("task-selected");
                $(".overflow-list").css("display", "none");
                $(document).off(".hideOverflowMenu");
            }
        });

        overflowList = $(".overflow-list");
        overflowIcon = $(this);
        task = overflowIcon.parent().parent().parent();

        $(".task-selected").removeClass("task-selected");
        leftOffset = overflowIcon.offset().left - overflowList.width() + overflowIcon.width();
        topOffset = overflowIcon.offset().top + overflowIcon.height() + 10;

        overflowList.css("left", leftOffset);
        overflowList.css("top", topOffset);
        overflowList.css("display", "block");
        task.addClass("task-selected");

        $(".overflow-item").off("click");
        $(".overflow-item").click(overflowItemClick);
    };

    function overflowItemClick(event) {
        taskId = task.attr("id");
        listId = $(this).attr("id");
        if (listId.startsWith("move"))
            moveTask(taskId, listId);
        else if (listId.startsWith("order-up"))
            orderTask(taskId, -1);
        else if (listId.startsWith("order-down"))
            orderTask(taskId, 1);
        else if (listId.startsWith("delete"))
            deleteTask(taskId);
    }

    function taskContentClick(event) {
        $(".task-edit").prev().css("display", "");
        $(".task-edit").remove();

        elem = $(this).parent();
        elem.css("display", "none");

        createEditTaskHTML(this);

        $("#task-edit-submit").click(taskEditSubmitClick);
        $("#task-edit-cancel").click(taskEditCancelClick);
        $(".tag-list").click(function(event) { event.stopPropagation(); });
        $("#label-icon").click(labelIconClick);
    }

    function taskEditSubmitClick(event) {
        editElem = $(this).parent().parent().parent().parent().parent().parent();
        dataElem = editElem.find("#edit-task-description");
        updatedElem = editElem.prev();
        updatedElem.css("display", "");

        jsonData = JSON.stringify({ task_id: updatedElem.parent().attr("id"), desc: dataElem.text() }, null, '\t');
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
    }

    function taskEditCancelClick(event) {
        editElem = $(this).parent().parent().parent().parent().parent().parent();
        editElem.prev().css("display", "");
        editElem.remove();
    }

    function labelIconClick(event) {
        $(document).on("mouseup.hideTagMenu", function(event) {
            if (!$(event.target).is(".tag-list *, .tag-list")) {
                $(".task-selected").removeClass("task-selected");
                $(".tag-list").css("display", "none");
                $(document).off(".hideTagMenu");
            }
        });

        tagList = $(".tag-list");
        taskId = tagList.parent().parent().parent().attr("id");
        jsonData = JSON.stringify({ task_id: taskId  }, null, '\t');
        $.ajax({
            type: "POST",
            url: "/tasks/query_tags_for_task",
            data: jsonData,
            contentType: "application/json;charset=UTF-8",
            success: function(tags) {
                tagList = $(".tag-list");
                tagList.children().each(function() { $(this).removeClass("active"); });

                for (let tag of tags)
                    $("#tag-" + tag.id).addClass("active");

                $(".tag-list-item").off("click");
                $(".tag-list-item").click(tagListItemClick);

                labelIcon = $("#label-icon");
                leftOffset = labelIcon.offset().left - tagList.width() + labelIcon.width();
                topOffset = labelIcon.offset().top + labelIcon.height() + 20;

                tagList.css("left", leftOffset);
                tagList.css("top", topOffset);
                tagList.css("display", "block");
            }
        });
    }

    function tagListItemClick(event) {
        taskId = $(this).parent().parent().parent().parent().attr("id");
        tagId = $(this).attr("id");
        jsonTagData = JSON.stringify({ task_id: taskId, tag_id: tagId });
        $.ajax({
            type: "POST",
            url: "/tasks/update-tags",
            data: jsonTagData,
            contentType: "application/json;charset=UTF-8",
            success: function(msg) {
                if (msg === "error") {
                    console.log(msg);
                } else if (msg === "removed") {
                    $("#badge-" + tagId).remove();
                    $(event.target).removeClass("active");
                } else {
                    htmlString = "<span id='badge-" + tagId +
                        "' class='badge badge-pill badge-primary'>" + msg +
                        "</span>";
                    $("#" + taskId).find(".task-content").append($(htmlString));
                    $(event.target).addClass("active");
                }
            }
        });
    }

    function createEditTaskHTML(thisObj) {
        htmlElem = "\
        <div class='task-edit'> \
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
                        <td class='td_submit' align='left'> \
                            <a href='#' id='task-edit-submit'>Save</a> \
                            <a href='#' id='task-edit-cancel' class='cancel'>Cancel</a> \
                        </td> \
                        <td class='td_extra' align='right'> \
                            <span id='label-icon' class='icon icon-btn accent-color extra-item material-icons'>label_outline</span> \
                        </td> \
                    </tr> \
                </table> \
                <div class='icon-list tag-list'></div> \
            </form> \
        </div> \
        ";

        elem.after(htmlElem);
        inputField = $("#edit-task-description");
        inputField.html($(thisObj).parent().find(".task-description").text());
        inputField.focus();
        setEndOfContenteditable(inputField.get(0));

        $.ajax({
            type: "POST",
            url: "/tags/query",
            contentType: "application/json;charset=UTF-8",
            success: function(tags) {
                if ($.isArray(tags)) {
                    for (let tag of tags) {
                        htmlString = [
                        "<div id=\"tag-" + tag.id + "\" class=\"tag-list-item\">",
                        tag.name,
                        "<span class=\"material-icons\">done</span>",
                        "</div>"
                        ].join("");
                        $(".tag-list").append($(htmlString));
                    }

                    addBtnString = "\
                    <a class='theme-btn icon-btn add-tag-btn' href='/tags/edit'> \
                        <span class='icon material-icons'>add</span> \
                        <span>Add tag</span> \
                    </a> \
                    ";
                    $(".tag-list").append($(addBtnString));
                } else {
                    window.location.href = redirect_url;
                }
            }
        });
    }

    function deleteTask(taskId) {
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
    }

    function moveTask(taskId, listId) {
        jsonData = JSON.stringify({ task_id: taskId, list_id: listId }, null, '\t');
        $.ajax({
            type: "POST",
            url: "/tasks/move",
            data: jsonData,
            contentType: "application/json;charset=UTF-8",
            success: function(redirect_url) {
                window.location.href = redirect_url;
            }
        });
    }

    function orderTask(taskId, offset) {
        jsonTagData = JSON.stringify({ task_id: taskId, offset: offset });
        $.ajax({
            type: "POST",
            url: "/tasks/order_task",
            data: jsonTagData,
            contentType: "application/json;charset=UTF-8",
            success: function() {
                location.reload();
            }
        });
    }
});
