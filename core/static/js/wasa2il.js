var issue_timer;
var issue_object;
var issue_id;
var election_timer;
var election_object;
var election_id;
var election_ui_update_is_safe = function() { return true; }
var discussion_timer;
var discussion_object;
var discussion_id;
var show_closed_elections;


function user_logged_out() {
    var user_id = $('input[name=user_id]').val();
    if (user_id && user_id != 'None') location.reload(true);
}


function document_propose(doc, val) {
    data = {};
    if (issue_id != undefined) {
        data["issue"] = issue_id;
    }
    $.getJSON("/api/document/propose/" + doc + "/" + val + "/", data, function(data) {
        if (data.ok) {
            $('#document_import').modal('hide');
            if (data.html_user_documents != undefined) {
                $("#document_user_proposals_table").html(data.html_user_documents);
            }
            if (data.html_all_documents != undefined) {
                $("#document_all_proposals_table").html(data.html_all_documents);
            }
        }
    });
}


function document_import(doc) {
    data = {};
    if (issue_id != undefined) {
        data["issue"] = issue_id;
    }
    data["document"] = doc;

    $.getJSON("/api/issue/import/", data, function(data) {
        if (data.ok) {
            if (data.html_user_documents != undefined) {
                $("#document_user_proposals_table").html(data.html_user_documents);
            }
            if (data.html_all_documents != undefined) {
                $("#document_all_proposals_table").html(data.html_all_documents);
            }
        }
    });
}

function topic_star(topic) {
    $.getJSON("/api/topic/star/", {"topic": topic}, function(data) {
        if (data.ok) {
            $("#topics_list tbody").html(data.html);
        }
    });
}


function topics_showstarred_toggle(polity) {
    $.getJSON("/api/topic/showstarred/", {"polity": polity}, function(data) {
        if (data.ok) {
            $("#topics_list tbody").html(data.html);
            if (data.showstarred) {
                $("#topics_showstarred_toggle span").removeClass("icon-grey");
            } else {
                $("#topics_showstarred_toggle span").addClass("icon-grey");
            }
        }
    });
}


function elections_showclosed_toggle(polity_id) {
    show_closed_elections = (show_closed_elections ? 0 : 1);
    $.getJSON("/api/election/showclosed/", {"polity_id": polity_id, "showclosed": show_closed_elections}, function(data) {
        if (data.ok) {
            $("#elections_list tbody").html(data.html);
            if (data.showclosed) {
                $("#elections_showclosed_toggle span").removeClass("icon-grey");
            } else {
                $("#elections_showclosed_toggle span").addClass("icon-grey");
            }
        }
    });
}


function issue_timer_start() {
    issue_timer = window.setInterval(function() { issue_poll(issue_id); }, 5000);
}

function issue_timer_stop() {
    window.clearInterval(issue_timer);
}


function issue_vote(val) {
    issue_timer_stop();
    $.getJSON("/api/issue/vote/", {"issue": issue_id, "vote": val}, function(data) {
        if (data.ok) {
            issue_object = data.issue;
            issue_render();
        } else {
            $("#vote_error").show();
        }
        issue_timer_start();
    });
}


function issue_poll(issue) {
    $.getJSON("/api/issue/poll/", {"issue": issue}, function(data) {
        if (data.ok) {
            issue_object = data.issue;
            issue_render();
        } else {
            // Silent error reporting?
        }
    });
}

function issue_render(issue) {
    //remove selection and deactivate all active buttons
    $("#vote_yes").parent().children().removeClass('btn-success');
    $("#vote_yes").parent().children().removeClass('active');

    if (issue_object.vote == 1) {
        $("#vote_yes").addClass('btn-success');
        $("#vote_yes").addClass('active');
    } else if (issue_object.vote == -1) {
        $("#vote_no").addClass('btn-success');
        $("#vote_no").addClass('active');
    } else {
        $("#vote_abstain").addClass('btn-success');
        $("#vote_abstain").addClass('active');
    }
    $("#issue_votes_count").text(issue_object.votes.count);
    if (issue_object.comments.length > 0) {
        $("#issue-comments-header").show();
    }
    else {
        $("#issue-comments-header").hide();
    }
}

function render_comment(comment) {
    div = "<div class=\"comment\" id=\"comment_" + comment.id + "\">";
    div +=  "<div class=\"profilepic\">";
    div +=    "<a href=\"/accounts/profile/" + comment.created_by + "/\"><img src=\"" + comment.created_by_thumb + "\" /></a>";
    div +=  "</div>";
    div +=  "<div class=\"content\">";
    div +=    "<div class=\"created_by\"><a href=\"/accounts/profile/" + comment.created_by + "/\">" + comment.created_by + "</a> ";
    if (comment.issue_id) {
        div += comment.in + " <a href=\"/issue/" + comment.issue_id + "/\">" + comment.issue_name + "</a>";
    }
    div += "</div>";
    div +=    "<div class=\"text\">" + comment.comment.replace(/\n/g, '<br />') + "</div>";
    div +=    "<div class=\"created\">" + comment.created_since + "</div>";
    div +=  "</div>";
    div += "</div>";
    return div
}

function render_comments(comments, $id) {
    $($id).empty();
    for (i in comments) {
        comment = comments[i];
        $($id).append(render_comment(comment));
    }
}

function commentPoll(obj_key, obj_id) {
    var obj = {};
    obj[obj_key] = obj_id;
    var APIPath = "/api/" + obj_key + "/poll/";

    $.get(APIPath, obj).done(function(data) {
        if (data.ok) {
            keys = Object.keys(data);
            ok_pos = keys.indexOf("ok");
            if (ok_pos != -1) {
                keys.splice(keys.indexOf("ok"), 1);
            }
            key = keys[0];
            object = data[key];
            render_comments(object.comments, "#" + key + "_comments");
        } else {
            // Silent error reporting?
        }
    }).fail(function(xhr, textStatus, errorThrown) {
        alert("Error: " + errorThrown);
    });
}


function commentSend(obj_key, obj_id, comment) {
    comment_text = comment.val();
    if (comment_text == "") {
        comment.focus();
        return;
    }
    var APIPath = "/api/" + obj_key + "/comment/send/";
    var postData = {};
    postData["comment"] = comment_text;
    postData[obj_key] = obj_id;
    postData['csrfmiddlewaretoken'] = $('.comment_form'
        ).find('input[name="csrfmiddlewaretoken"]').val();
    $.post(APIPath, postData, null, 'json').done(function(data) {
        if (data.ok) {
            comment.val("");
            keys = Object.keys(data);
            ok_pos = keys.indexOf("ok");
            if (ok_pos != -1) {
                keys.splice(keys.indexOf("ok"), 1);
            }
            key = keys[0];
            object = data[key];
            render_comments(object.comments, "#" + key + "_comments");
            comment.focus();
        } else {
            alert('Error: Data malformed');
        }
    }).fail(function(xhr, textStatus, errorThrown) {
        alert("Error: " + errorThrown);
    });
}


function commentTimerStart(key, obj_id) {
    discussion_timer = window.setInterval(function() {
        commentPoll(key, obj_id);
    }, 5000);
}

function commentTimerStop() {
    window.clearInterval(discussion_timer);
}

function election_timer_start() {
    // This is basically just checking for new candidates or keeping
    // different tabs/windows in sync and as such, doesn't really need to
    // happen too frequently.  Doing this too fast just increases load.
    election_timer = window.setInterval(function() {
        election_poll(election_id);
    }, 20000);
}

function election_timer_stop() {
    window.clearInterval(election_timer);
}

function election_timer_restart() {
    election_timer_stop();
    election_timer_start();
}


function election_candidacy_announce() {
    $('#election_button_announce').hide();
    $('#election_announce_working').show();
    return election_candidacy(1);
}

function election_candidacy_withdraw() {
    var confirm_msg = $('#election_button_withdraw').data("confirm");
    if (!confirm_msg || confirm(confirm_msg)) {
        $('#election_button_withdraw').hide();
        $('#election_announce_working').show();
        return election_candidacy(0);
    }
}


function election_candidacy(val) {
    election_timer_stop();
    $.post("/api/election/candidacy/", {
        "csrfmiddlewaretoken": $('input[name=csrfmiddlewaretoken]').val(),
        "election": election_id,
        "val": val
    }, function(data) {
        if (data.ok) {
            election_object = data.election;
        } else {
            // FIXME: Error handling?
        }
        election_render();
        election_timer_start();
    }, "json").always(function() {
        $('#election_announce_working').hide();
    });
}


function election_poll(election) {
    $.getJSON("/api/election/poll/", {"election": election}, function(data) {
        if (data.logged_out) user_logged_out();
        if (data.ok) {
            election_object = data.election;
            $('#submit-working, #submit-is-magic, #submit-error').hide();
        } else {
            // FIXME: Error handling?
        }
        election_render();
    });
}


function election_render(election) {
    if (election_object.is_voting) {
        $(".voting").show();
    }

    // FIXME: The second term here makes much of the code below obsolete.
    //        This is deliberate; we would like to allow users to withdraw
    // their candidacy at any time, but we need a few more things before
    // that is safe and reasonable:
    //     1. E-mail notifications to people who have voted for the candidate
    //     2. A grace period so people can update their votes
    //     3. Double-checking the ballot counting logic to ensure this does
    //        not break anything at that end, as it will create a gap in
    //        the user's ballot sequence.
    if (election_ui_update_is_safe()) {
        if (election_object.is_closed || election_object.is_voting) {
            $("#election_button_withdraw").hide();
            $("#election_button_announce").hide();
        }
        else if (election_object.user_is_candidate) {
            $("#election_button_withdraw").show();
            $("#election_button_announce").hide();
        }
        else {
            $("#election_button_withdraw").hide();
            if (election_object.is_voting) {
                $("#election_button_announce").hide();
            } else if (election_object.is_waiting) {
                $("#election_button_announce").hide();
            } else {
                $("#election_button_announce").show();
            }
        }

        $("#election_votes_count").text(election_object.votes.count);
        $("#election_candidates_count").text(election_object.candidates.count);
        $("#candidates").html(election_object.candidates.html);
        $("#vote").html(election_object.vote.html);
    }
}


$(document).ready(function() {
    // NOTE: The first text input field is the search field at the top of the page.
    // I was here. This gets the order incorrectly or something.
    var $inputs = $('input[type="text"],input[type="password"],textarea');
    if ($inputs.length > 1) {
        $inputs[1].focus();
    }
});

// function start_introjs(){
//     introJs().start();
// }

$(function() {

    $("i[rel='tooltip'],a[rel='tooltip']").tooltip({'placement': 'top'});

});

