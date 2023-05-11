/* jQuery Serialize All - https://github.com/mikeirvingweb/jquery-serialize-all */
(function ($) {

    $.fn.serializeAll = function () {
        var serialized = this.serialize(), serializedSplit = serialized.split("&"), empty = "";

        this.each(function () {

            jQuery(this).find(
                "input[name][type=checkbox]:not(:checked)"
            ).each(function () {
                empty += (empty !== "" ? "&" : "") + this.name + "=";
            });

            jQuery(this).find(
                "input[name][type=radio]:not(:checked)"
            ).each(function () {
                var includeField = true, checkName = this.name;

                jQuery(serializedSplit).each(function () {
                    if (this.split("=")[0] == checkName)
                        includeField = false;
                });

                var emptySplit = empty.split("&");

                jQuery(emptySplit).each(function () {
                    if (this.split("=")[0] == checkName)
                        includeField = false;
                });

                if (includeField) // exclude duplicates
                    empty += (empty !== "" ? "&" : "") + this.name + "=";
            });

            jQuery(this).find(
                "select[name][multiple]"
            ).each(function () {
                if (jQuery(this).find("option:selected").length === 0) {
                    empty += (empty !== "" ? "&" : "") + this.name + "=";
                }
            });

        });

        return serialized + ((serialized !== "" && empty !== "") ? "&" : "") + empty;
    };

}(jQuery));