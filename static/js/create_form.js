(function() {

        function form_is_valid() {

                var valid = true;

                // check form title
                if ($("#form-title").value == false) {
                        return false;
                }

                // check that form has at least one question
                if ($(document).find(".question").length == 0) {
                        return false;
                }
         

                // check each question 
                $("#questions .question input").each(function () {
                        // check if input value is falsey
                        if (this.value != 0 && this.value == false) {
                                valid = false;
                        }

                });

                // check if all multiple-choice and multiple select
                // have at least one option
                $("#questions .question .options").each(function() {
                        if ($(this).find(".option").length == 0) {
                                valid = false;
                        }
                });

                return valid;
        }

        function parse_form_object() {

                var name = $("#form-title").val();
                var graded = $("#is-graded").val();
                var questions = [];

                $("#questions .question").each(function () {

                        var question = {};
                        question.question_type = $(this).attr("name");
                        question.question_text = $(this).find(".question-text").val();
                        question.additional_info = {}; 

                        if ($(this).attr("name") == "MC" || $(this).attr("name") == "SM") {
                                question.additional_info.choices = [];
                                $(this).find(".option .form-control").each(function() {
                                        question.additional_info.choices.push(this.value);
                                });
                        }

                        if ($(this).attr("name") == "SS") {
                                question.additional_info.range_min = parseInt($(this).find(".slider-min").val());
                                question.additional_info.range_max = parseInt($(this).find(".slider-max").val());
                        }

                        questions.push(question);

                });

                return {name: name, graded: graded, questions: questions};

        }

        var num_questions = 0;
        function add_question(path, name) {

                if (num_questions == 0) {
                        $("#questions").empty();
                }
                $.get("question/" + path, function (t) {
                        $("#questions").append("<div class='question' name='" + name + "'>"  + t + "<hr></div>");
                        update_question_nums();
                });
                num_questions += 1;

        }

        // form controls
        function update_question_nums() {

                var num = 1;
                $(".question").each(function () {
                        $(this).attr("id", num);
                        num += 1;
                });

                num = 1;
                $(".question-num").each(function () {
                        $(this).html("#" + num);
                        num += 1;
                });

        }

        function init_sliders() {

                var num_sliders = 0;
                $(".question #slider-target").each(function () {

                        $(this).attr("id", num_sliders.toString());
                        if (! $(this).hasClass("edited")) {
                                $(this).slider({
                                        id: "slider-target",
                                        min: 0,
                                        max: 0,
                                        step: 1
                                });
                        }
                        num_sliders += 1;

                });
                
        }

        $("#add-short-answer").on("click", function() {
                add_question("short_answer", "SF");
        });
        
        $("#add-long-answer").on("click", function() {
                add_question("long_answer", "LF");
        });

        $("#add-multiple-choice").on("click", function() {
                add_question("multiple_choice", "MC");
        });

        $("#add-multiple-select").on("click", function() {
                add_question("multiple_select", "SM");
        });

        $("#add-slider").on("click", function() {
                add_question("slider", "SS");
        });

        $("#submit-form").on("click", function() {
                if (form_is_valid()) {
                        form_object = parse_form_object();
                        $.ajax({
                            type: 'POST',
                            url: "/create_form",
                            data: {form: JSON.stringify(form_object),
                                   csrfmiddlewaretoken: csrf_token},
                            success: function(result) {
                                window.location.href = "/dashboard";
                            },
                            error: function(xhr, status, error) {
                                $.get("question/invalid_form", function(t) {
                                        $("#questions").prepend(t);
                                });
                            },
                        });
                } else {
                        $.get("question/invalid_form", function(t) {
                                $("#questions").prepend(t);
                        });
                }
        });

        // controls for each question
        function swap(source, target) {
                var temp = $("#" + target).html();
                var source_values = [];
                var target_values = [];
                $("#" + source + " input").each(function() {
                        source_values.push(this.value);
                });
                $("#" + target + " input").each(function() {
                        target_values.push(this.value);
                });
                $("#" + target).html($("#" + source).html());
                $("#" + source).html(temp);
                $("#" + source + " input").each(function(index) {
                        $(this).val(target_values[index]);
                });
                $("#" + target + " input").each(function(index) {
                        $(this).val(source_values[index]);
                });
                update_question_nums();
        }

        $("#questions").on("click", ".move-up", function(e) {
                var source = parseInt($(this).closest(".question").attr("id"));
                var target = source - 1;
                if (target == 0) {
                        return;
                } else {
                        swap(source, target);
                }
        });

        $("#questions").on("click", ".move-down", function(e) {
                var source = parseInt($(this).closest(".question").attr("id"));
                var target = source + 1;
                if (target == num_questions + 1) {
                        return;
                } else {
                        swap(source, target);
                }
        });

        $("#questions").on("click", ".delete", function(e) {
                $(this).closest(".question").remove();
                update_question_nums();
        });

        $("#questions").on("click", ".add-option", function(e) {
                var t = `<div class="option">
                        <div class="input-group">
                        <span class="input-group-addon">
                        <input type="radio" disabled>
                        </span>
                        <input type="text" class="form-control" placeholder="Edit Option">
                        <span class="input-group-btn">
                        <button class="btn btn-danger delete-option" type="button">Delete</button>
                        </span>
                        </div>
                        <br>
                        </div>`
                $(this).closest(".options").prepend(t);
        });

        $("#questions").on("click", ".delete-option", function(e) {
                $(this).closest(".option").remove();
        });

        $("#questions").on("change", ".slider-min", function(e) {
                var new_min = this.value;
                var new_max = this.value;
                var question = $(this).closest(".question");
                var max_val = $(question).find(".slider-max").val();
                if (max_val) {
                        new_max = max_val;
                }
                var values = [];
                for (var i = new_min; i <= max_val; i++) {
                        values.push(i);
                }
                if (values.length == 0) {
                        values.push(this.value);
                }
                $(question).find("#slider-target").each(function() {
                        $(this).addClass("edited");
                        $(this).slider({
                                id: "slider-target",
                                ticks: values
                        });
                });
        });

        $("#questions").on("change", ".slider-max", function(e) {
                var new_min = this.value;
                var new_max = this.value;
                var question = $(this).closest(".question");
                var min_val = $(question).find(".slider-min").val();
                if (min_val) {
                        new_min = min_val;
                }
                var values = [];
                for (var i = new_min; i <= new_max; i++) {
                        values.push(i);
                }
                if (values.length == 0) {
                        values.push(this.value);
                }
                $(question).find("#slider-target").each(function() {
                        $(this).addClass("edited");
                        $(this).slider({
                                id: "slider-target",
                                ticks: values
                        });
                });
        });


})();
