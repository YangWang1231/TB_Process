
$(document).ready(function () {
    //watch link click event
    $(".column4").click(function () {
        var column2 = $(this).siblings(".column2");
        prj_name = column2.text();
        alert("selected project name: " + prj_name);

        //$.get("/project_status",
        //    request_data,
        //    function (response, status, xhr) {
        //        //if (response == "Processing")
        //        //    alert("project is processing.");
        //        //else
        //        if (response.status == "Finished") {
        //            clearInterval(timerID)
        //            alert("project is finished. you can find it in the personal page")
        //            $.get("/uploads", { "metrics_filename": response.filename })
        //        }
        //    },
        //    "json"
        //);
    }
    );
    var options = {
        // target: '#output2',   // target element(s) to be updated with server response
        beforeSubmit: showRequest,  // pre-submit callback
        success: showResponse,  // post-submit callback

        // other available options:
        //url:       url         // override for form's 'action' attribute
        //type:      type        // 'get' or 'post', override for form's 'method' attribute
        //dataType:  null        // 'xml', 'script', or 'json' (expected server response type)
        clearForm: true        // clear all form fields after successful submit
        //resetForm: true        // reset the form after successful submit

        // $.ajax options can be used here too, for example:
        //timeout:   3000
    };

    $('#form1').ajaxForm(options);
    $('#form2').ajaxForm(options);
});
