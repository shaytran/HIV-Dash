window.dash_clientside = Object.assign({}, window.dash_clientside, {
    clientside: {
        toggle_modal_data_source: function(n_clicks, is_open) {
            return !is_open;
        }
    }
});