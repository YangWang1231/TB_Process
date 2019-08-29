
$(document).ready(function () {
    var options = {
        // target: '#output2',   // target element(s) to be updated with server response
        beforeSubmit:   showRequest,  // pre-submit callback
        success:            showResponse,  // post-submit callback

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

//make a global var which can be accessed by all function in this scope
var projectname = ""

//function for time inerval
function cyc_retrive_projects_status() {
    var request_data = {
        "projectname": projectname
    }
    var timerID = setInterval( function () {
        $.get("/project_status",
                request_data,
                function (response, status, xhr) {
                    //if (response == "Processing")
                    //    alert("project is processing.");
                    //else
                    if (response.status == "Finished") {
                        clearInterval(timerID)
                        alert("project is finished. you can find it in the personal page")
                        $.get("/uploads", { "metrics_filename": response.filename } )
                    }
                },
                "json"
        );
    }
    , 500 );
}

// pre-submit callback
function showRequest(formData, jqForm, options) {
    projectname = $("#form2_project_name").val()
    return true;
}

        // post-submit callback
function showResponse(responseText, statusText) {
    if (responseText == "1") {
        alert("提交成功！");
        $('#submitover').text("提交成功，分析完毕会自动启动下载")
        cyc_retrive_projects_status()
    }
    else if (responseText == "0") {
        alert("文件名后缀不是'.zip'或'.rar‘")
    }
    return true
}