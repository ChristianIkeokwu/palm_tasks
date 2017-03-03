$( "#{{ notif._id}}" ).click(function() {
        $.ajax({
            dataType: "json",
            url: {{ url_for("notifications.read", _id=notif._id) }},
            type: 'get',
            success: function(data) {
                    console.log(data.message);
                }
            });
        });