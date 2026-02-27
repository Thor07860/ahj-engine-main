document.addEventListener("DOMContentLoaded", function () {
    if (typeof CKEDITOR === "undefined") {
        return;
    }

    var textareas = document.querySelectorAll("textarea");

    textareas.forEach(function (textarea) {
        if (!textarea.id) {
            textarea.id = "ck-editor-" + Math.random().toString(36).slice(2);
        }

        if (CKEDITOR.instances[textarea.id]) {
            return;
        }

        CKEDITOR.replace(textarea.id, {
            height: 350
        });
    });
});
