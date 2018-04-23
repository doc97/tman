$(function() {
    allTags = []

    $.ajax({
        type: "POST",
        url: "/tasks/query_all_tags",
        contentType: "application/json;charset=UTF-8",
        success: function(tags) {
            Array.prototype.push.apply(allTags, tags)
        }
    });

    $(".complete-btn").click(function(event) {
        taskId = $(event.target).parent().parent().parent().attr("id");
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

    $(".undo-btn").click(function(event) {
        taskId = $(event.target).parent().parent().parent().attr("id");
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
    });

    $(".delete-btn").click(function(event) {
        taskId = $(event.target).parent().parent().parent().attr("id");
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

    $(".overflow-icon").click(function(event) {
        overflowList = $(".overflow-list");
        overflowIcon = $(event.target);

        if (overflowIcon.hasClass("active")) {
            overflowIcon.removeClass("active");
            overflowList.css("display", "none");
        } else {
            $(".overflow-icon").removeClass("active");
            leftOffset = overflowIcon.offset().left - overflowList.width() + overflowIcon.width();
            topOffset = overflowIcon.offset().top + overflowIcon.height() + 20;

            overflowList.css("left", leftOffset);
            overflowList.css("top", topOffset);
            overflowList.css("display", "block");
            overflowIcon.addClass("active");
        }
        event.stopPropagation();
    });

    $(".overflow-list").click(function(event) {
        event.stopPropagation();
    });

    $(document).click(function() {
        $(".overflow-icon").removeClass("active");
        $(".overflow-list").css("display", "none");
    });

    $(".overflow-item").click(function(event) {
        taskId = $(".overflow-icon.active").parent().parent().parent().attr("id");
        listId = $(event.target).attr("id");
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
    });

    $(".task-content").click(function(event) {
        $(".task-edit").prev().css("display", "");
        $(".task-edit").remove();

        $(".task-edit").remove();
        elem = $(event.target).parent().parent();
        elem.css("display", "none");

        htmlElem = "\
        <div class='task-edit task'> \
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
                            <i id='label-icon' class='icon-btn extra-item material-icons'>label_outline</i> \
                        </td> \
                    </tr> \
                </table> \
                <div class='icon-list tag-list'></div> \
            </form> \
        </div> \
        ";

        elem.after(htmlElem);
        inputField = $("#edit-task-description");
        inputField.html($(event.target).text());
        inputField.focus();
        setEndOfContenteditable(inputField.get(0));

        for (let tag of allTags) {
            htmlString = "<a id=tag-" + tag.id + " class='tag-item' href='#' draggable=false>" + tag.name + "</a>";
            $(".tag-list").append($(htmlString));
        }

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

        $("#label-icon").click(function(event) {
            tagList = $(".tag-list");
            if (tagList.css("display") === "none") {
                editElem = tagList.parent().parent().prev();
                jsonData = JSON.stringify({ task_id: editElem.attr("id")  }, null, '\t');
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


                        $(".tag-item").click(function(event) {
                            taskId = $(event.target).parent().parent().parent().prev().attr("id");
                            tagId = $(event.target).attr("id");
                            jsonTagData = JSON.stringify({ task_id: taskId, tag_id: tagId });
                            $.ajax({
                                type: "POST",
                                url: "/tasks/update-tags",
                                data: jsonTagData,
                                contentType: "application/json;charset=UTF-8",
                                success: function(msg) {
                                    if (msg === "added") {
                                        htmlString = "<span id='badge-" + tagId +
                                            "' class='badge badge-pill badge-primary'>" + $(event.target).text() +
                                            "</span>";
                                        $("#" + taskId).find(".task-content").append($(htmlString));
                                        $(event.target).addClass("active");
                                    } else if (msg === "removed") {
                                        $("#badge-" + tagId).remove();
                                        $(event.target).removeClass("active");
                                    } else {
                                        console.log(msg);
                                    }
                                }
                            });
                        });

                        labelIcon = $("#label-icon");
                        leftOffset = labelIcon.offset().left - tagList.width() + labelIcon.width();
                        topOffset = labelIcon.offset().top + labelIcon.height() + 20;

                        tagList.css("left", leftOffset);
                        tagList.css("top", topOffset);
                        tagList.css("display", "block");
                    }
                });
            } else {
                tagList.css("display", "none");
            }
        });
    });

    $( "#sortable" ).sortable({
        handle: ".sortable-handle",
        axis: "y",
        update: function(event, ui) {
            console.log(ui.item.index());
        }
    });
    $( "#sortable" ).disableSelection();

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
