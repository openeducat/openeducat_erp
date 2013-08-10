openerp.openeducat_erp = function(instance) {
    var QWeb = instance.web.qweb;
    var _t = instance.web._t;

instance.web.WebClient.include({
    set_title: function(title) {
        title = _.str.clean(title);
        var sep = _.isEmpty(title) ? '' : ' - ';
        document.title = title + sep + 'OpenEduCat';
    },
    
});
};