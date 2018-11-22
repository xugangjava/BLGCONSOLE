function alert(msg) { Ext.Msg.alert('提示', msg); }

function warning(msg) { Ext.Msg.alert('警告', msg); }

function error(msg) { Ext.Msg.alert('错误', msg); }

function confirm(msg, fun) {
    Ext.Msg.confirm('警告', msg, function(e) {
        if (e == 'yes') {
            fun(e);
        }
    });
}

function yesno(value) { return value ? '是' : '否' }

function mask(msg) { Ext.getBody().mask(msg); }

function unmask() { Ext.getBody().unmask(); }

function isArrary(obj) { return Object.prototype.toString.call(obj) === '[object Array]'; }
Array.prototype.Clone = function() { return [].concat(this); }


Ext.Ajax.on('requestcomplete', function (conn, response, options) {
    //Ext重新封装了response对象     
    try{
        var js=JSON.parse(response.responseText);
        if(js&&js.SESSSION_TIME_OUT&&js.SESSSION_TIME_OUT===1){
            alert('您的登录已超时，请刷新页面后登陆');
        }
    }catch (e){
        console.log(e)
    }
}, this);     

//crsf验证
Ext.Ajax.on('beforerequest', function(conn, options) {
    if (!(/^http:.*/.test(options.url) || /^https:.*/.test(options.url))) {
        if (Ext.util.Cookies.get('csrftoken') == null) {
            Ext.util.Cookies.set('csrftoken', 'csrftoken')
        }
        if (typeof(options.headers) == "undefined") {
            options.headers = { 'X-CSRFToken': Ext.util.Cookies.get('csrftoken') };
        } else {
            options.headers['X-CSRFToken'] = Ext.util.Cookies.get('csrftoken');
        }
    }
}, this);


Ext.Ajax.on('requestexception', function(conn, options) {
    if (Main.Debug) {
        var win = new Ext.Window({
            title: '调试信息',
            closable: true,
            closeAction: 'close',
            width: 600,
            minWidth: 400,
            height: 400,
            maximizable: true,
            layout: 'fit',
            border: false,
            modal: true,
            items: [{
                xtype: 'panel',
                autoScroll: true,
                html: options.responseText
            }]
        });
        win.show();
    }
}, this);





function Debug(url, html) {

}

function downloadURL(url) {
    var hiddenIFrameID = 'hiddenDownloader',
        iframe = document.getElementById(hiddenIFrameID);
    if (iframe === null) {
        iframe = document.createElement('iframe');
        iframe.id = hiddenIFrameID;
        iframe.style.display = 'none';
        document.body.appendChild(iframe);
    }
    iframe.src = url;
}

function deleteObjects(ids, url, func) {
    Ext.Ajax.request({
        url: url,
        method: "post",
        params: { ids: ids.join() },
        success: function(form) {
            var json = Ext.decode(form.responseText);
            if (!json) {
                alert('找不到对象!');
                return;
            }
            func(json);
        }
    });
}

function getObjectById(id, url, func) {
    Ext.Ajax.request({
        url: url,
        method: "post",
        params: { pk: id },
        success: function(form) {
            var json = form.responseJSON;
            if (!json) {
                alert('找不到对象!');
                return;
            }
            func(json);
        }
    });
}


Ext.ns("XG.Control.AbstractGrid");
XG.Control.AbstractGrid = Ext.extend(Ext.grid.GridPanel, {
    constructor: function(config) {
        var itemsPerPage =config.pagesize?config.pagesize: 20;
        var stroe_fields = ['pk'];
        var columes = config.columes;
        var tbar = [];
        var baseParams = config.baseParams;
        var op = config.op;
        var fields = config.fields;
        var action = config.action;
        var data_columes = [];
        if (config.tbar) {
            for (var i = config.tbar.length - 1; i >= 0; i--) {
                tbar.push(config.tbar[i]);
            };
        }
        this.id = config.id ? config.id : Ext.id();

        if (!config.hasOwnProperty('nocheck')) {
            var sm = new Ext.grid.CheckboxSelectionModel({
                singleSelect: config.singleSelect ? true : false,
                sortable: false
            });
            this.selModel = sm;
            data_columes.push(sm);
        }
        var autoExpandColumn = null;
        for (var i = 0; i < columes.length; i++) {
            stroe_fields.push(columes[i].dataIndex);
            if (columes[i].expend) {
                autoExpandColumn = columes[i].id = Ext.id();
            }
            if (columes[i].hasOwnProperty('header')) {
                var b = columes[i];
                b.sortable = true;
                data_columes.push(b);
            }
        }

        var values = ['pk'];
        for (var i = stroe_fields.length - 1; i >= 0; i--) {
            values.push(stroe_fields[i])
        };

        var store = new Ext.data.JsonStore({
            totalProperty: 'total',
            idProperty: 'pk',
            fields: stroe_fields,
            pageSize: itemsPerPage,
            root: 'items',
            url: config.not_main_grid ? action : action + '?m=list'
        });

        if (baseParams) {
            store.baseParams = baseParams;
        }
        config.store = store;
        this.stateful = true;
        this.multiSelect = true;
        this.cm = new Ext.grid.ColumnModel(data_columes);
        this.region = 'center';
        this.autoExpandColumn = autoExpandColumn;
        config.viewConfig = {
            //  forceFit:true,
            stripeRows: true,
            enableTextSelection: true
        };
        var me = this;
        if (!config.nopadding) {
            config.bbar = new Ext.PagingToolbar({
                pageSize: itemsPerPage,
                store: store,
                displayInfo: true
            });
        } else {
            tbar.push({
                text: '刷新',
                iconCls: 'Databaserefresh',
                handler: function() {
                    me.getStore().reload();
                }
            });
        }

        this.tbar = tbar;
        this.getSel = function() {
            var record = me.getSelectionModel().getSelections();
            var ids = [];
            if (!record || 0 == record.length) {
                alert('没有选中数据!');
                return ids;
            }

            Ext.each(record, function(item) {
                ids.push(item.data.pk ? item.data.pk : item.data.id);
            });
            return ids;
        }

        this.getFirstSel = function() {
            var record = me.getSelectionModel().getSelections();
            if (record.length != 1) {
                alert('请单选数据!');
                return null;
            }
            return record[0].data;
        }


        this.deleteRow = function(url) {
            var ids = me.getSel();
            if (!ids || ids.length == 0) return;
            var params = ids.length == 1 ? { pk: ids[0] } : { ids: ids.join() };
            confirm('确认删除选中的信息吗？<br/>相关联的数据也会被删除，请谨慎操作！', function(e) {
                Ext.Ajax.request({
                    url: url,
                    method: "post",
                    params: params,
                    success: function(form) {
                        var action = form.responseJSON;
                        if (action && action.message != "OK") {
                            alert(action.message);
                        } else {
                            me.getStore().load();
                            alert('删除成功!');
                        }
                    },
                    failure: function(form) {
                        var action = form.responseJSON;
                        if (action && 'result' in action) {
                            if ('msg' in action.result) {
                                error(action.result.msg);
                            }
                        } else {
                            error('发生异常!');
                        }
                    }
                });
            });
        }
        this.search = function(data) {
            me.getStore().baseParams = data;
            me.getStore().load({
                params: {
                    start: 0,
                    limit: itemsPerPage
                }
            });
        }
        this.reload = function() {
            me.getStore().reload();
        }
        XG.Control.AbstractGrid.superclass.constructor.call(this, config);

        this.getStore().load({
            params: {
                start: 0,
                limit: itemsPerPage
            }
        });
    }

});
Ext.reg('basegrid', XG.Control.AbstractGrid);



Ext.ns("XG.Control.SimpelPoupForm");
XG.Control.SimpelPoupForm = Ext.extend(Ext.Window, {
    constructor: function(config) {
        this.submit_click = false;
        this.title = config.title;
        this.closable = true;
        this.closeAction = 'close';
        this.modal = true;
        this.constrain = true;
        //this.layout='fit';
        this.width = config.width;
        this.height = config.height;
        this.animateTarget = config.animateTarget;
        this.border = false;

        var win = this;
        this.sbId = Ext.id();
        var obj_fields = [];
        for (var i = 0; i < config.items.length; i++) {
            if (config.items[i].readOnly) {
                config.items[i].style = 'background:#E6E6E6';
            } else {
                obj_fields.push(config.items[i].name);
            }
        }
        var form = new Ext.FormPanel({
            bodyStyle: 'padding:5px 5px 0',
            region: 'center',
            fieldDefaults: {
                msgTarget: 'side'
            },
            autoScroll: true,
            collect_params: config.collect_params,
            labelWidth: config.labelWidth,
            defaultType: 'textfield',
            defaults: {
                allowBlank: false,
                width: config.fieldWidth
            },
            items: config.items,
            clear: function() {
                var form = win.items.itemAt(0).getForm();
                form.reset();
                var fields = form.items;
                for (var f in fields) {
                    if (fields[f].xtype == 'combobox') {
                        fields[f].setValue(fields[f].getStore().getAt(0));
                    }
                }
            },
            buttons: [{
                text: '保存',
                id: win.sbId,
                handler: function() {
                    var form = win.items.itemAt(0).getForm();
                    if (!form.isValid()) return;
                    if (config.vailidate) {
                        if (!config.vailidate(form)) {
                            return;
                        }
                    }
                    var baseParams = {
                        fields: obj_fields
                    };
                    if (form.collect_params) {
                        var baseParams = form.collect_params(form);
                        if (!baseParams) return;
                    }
                    if (this.submit_click) return;
                    this.submit_click = true;
                    // win.hide();
                    var me = this;
                    form.submit({
                        clientValidation: true,
                        url: config.url,
                        params: baseParams,
                        success: function(form, action) {
                            me.submit_click = false;
                            if (action && action.result.message != "OK") {
                                alert(action.result.message);
                            }
                            if (config.success) config.success();
                            win.close();
                        },
                        failure: function(form, action) {
                            me.submit_click = false;
                            if (config.failure) config.failure();
                            else if (action && action.hasOwnProperty('result') &&
                                action.result.hasOwnProperty('message') &&
                                action.result.message) {
                                error(action.result.message);
                                return;
                            } else {
                                error('发生异常！');
                            }
                            win.close();
                        }
                    });
                }
            }, {
                text: '取消',
                handler: function() {
                    var form = win.items.itemAt(0).getForm();
                    form.clear();
                    win.close();
                }
            }]
        });

        if (config.layout) {
            form.layout = config.layout;
            form.layoutConfig = config.layoutConfig;
        }
        config.layout = 'fit';
        config.items = [form];


        XG.Control.SimpelPoupForm.superclass.constructor.call(this, config);
    },
    setReadOnly: function(bReadOnly) {
        var items = this.getItems();
        for (var i = items.length - 1; i >= 0; i--) {
            if (items[i].setReadOnly) {
                items[i].setReadOnly(true);
            }
        };
        Ext.getCmp(this.sbId).hide();
    },
    getItems: function() {
        var form = this.items.itemAt(0).getForm();
        var items = [];
        form.items.each(function(field) {
            if (items.xtype == 'fieldset') {
                items.items.each(function(f) {
                    items.push[f];
                });
            } else if (items.xtype == 'onetomanyfields') {
                var temp = [];
                items.items.each(function(f) {
                    temp.push[f];
                });
            } else {
                items.push(field);
            }
        });
        return items;
    },
    fill: function(json) {
        var form = this.items.itemAt(0).getForm();
        var filed, value;
        var one2manys = this.find('xtype', 'onetomanyfields');
        for (var obj in json) {
            if (isArrary(json[obj])) {
                var jarray = json[obj];
                var gfield = null;
                if (!one2manys || one2manys.length == 0) continue;
                for (var i = one2manys.length - 1; i >= 0; i--) {
                    gfield = one2manys[i];
                    if (!gfield.gname != obj) continue;
                    break;
                };
                if (!gfield) continue;
                gfield.setValue(jarray);
            } else {
                fields = form.findField(obj);
                if (fields) {
                    value = json[obj];
                    if (true === value) {
                        value = 1;
                    } else if (false === value) {
                        value = 0;
                    }
                    fields.setValue(value);
                }
            }
        }
    }
});
Ext.reg('poupform', XG.Control.SimpelPoupForm);




Ext.ns("XG.Control.BaseAyncTreeLoader");
XG.Control.BaseAyncTreeLoader = Ext.extend(Ext.tree.TreeLoader, {
    constructor: function(config) {
        XG.Control.BaseAyncTreeLoader.superclass.constructor.call(this, config);
    },
    getParams: function(node) {
        var buf = [],
            bp = this.baseParams;
        if (this.directFn) {
            //buf.push(node.attributes.id);  
            buf.push(node.attributes.treeid);
            if (bp) {
                if (this.paramOrder) {
                    for (var i = 0, len = this.paramOrder.length; i < len; i++) {
                        buf.push(bp[this.paramOrder[i]]);
                    }
                } else if (this.paramsAsHash) {
                    buf.push(bp);
                }
            }
            return buf;
        } else {
            for (var key in bp) {
                if (!Ext.isFunction(bp[key])) {
                    buf.push(encodeURIComponent(key), "=", encodeURIComponent(bp[key]), "&");
                }
            }
            //buf.push("node=", encodeURIComponent(node.attributes.id));  
            buf.push("node=", encodeURIComponent(node.attributes.treeid));
            return buf.join("");
        }
    }
});


Ext.ns("XG.Control.RemoteCombo");
XG.Control.RemoteCombo = Ext.extend(Ext.form.ComboBox, {
    constructor: function(config) {
        this.name = config.name;
        this.url = config.url;
        this.baseParams = config.baseParams;
        this.valueField = config.valueField;
        this.displayField = config.displayField;
        this.emptyData = config.emptyData;
        this.editable = config.editable;
        this.value = config.value;
        XG.Control.RemoteCombo.superclass.constructor.call(this, config);
    },
    getJson: function(v) {
        if (!this.items) return null;
        for (var i = this.items.length - 1; i >= 0; i--) {
            if (this.items[i][this.valueField] === v) {
                return this.items[i];
            }
        };
        return null;
    },
    initComponent: function() {
        var name = this.name,
            url = this.url;
        var valueField = this.valueField ? this.valueField : 'pk';
        var displayField = this.displayField ? this.displayField : 'name';
        var data = this.emptyData ? [
            [this.emptyData.pk, this.emptyData.name]
        ] : [];
        var items = null;
        var self = this;
        Ext.Ajax.request({
            url: url,
            async: false,
            success: function(response) {
                var json = Ext.decode(response.responseText);
                items = json.items;
                if (items && items.length > 0) {
                    for (var i = items.length - 1; i >= 0; i--) {
                        data.push([items[i][valueField], items[i][displayField]]);
                    };
                }
                store.loadData(data);
                if (!self.value && data.length > 0) {
                    self.value = data[0][0];
                }
                self.setValue(self.value);
            }
        });
        this.items = items;
        data.reverse();
        this.data = data;


        var store = new Ext.data.SimpleStore({
            fields: [valueField, displayField],
            data: []
        });
        Ext.apply(this, {
            hiddenName: name,
            store: store,
            valueField: valueField,
            triggerAction: 'all',
            displayField: displayField,
            mode: 'local',
            editable: this.editable ? true : false
        });

    }

});
Ext.reg('remotecombo', XG.Control.RemoteCombo);


Ext.ns("XG.Control.LocalCombo");
XG.Control.LocalCombo = Ext.extend(Ext.form.ComboBox, {
    constructor: function(config) {
        this.data = config.data;
        this.name = config.name;
        XG.Control.LocalCombo.superclass.constructor.call(this, config);
    },
    initComponent: function() {
        var defaultValue, store;
        if (isArrary(this.data)) {
            store = new Ext.data.SimpleStore({
                fields: ['value', 'text'],
                data: this.data
            });
            defaultValue = this.data[0][0];
        } else {
            store = this.data;
            if (store.getAt(0)) {
                defaultValue = store.getAt(0).data.value;
            }
        }
        Ext.apply(this, {
            hiddenName: this.name,
            name: this.name + '_s',
            store: store,
            valueField: 'value',
            triggerAction: 'all',
            displayField: 'text',
            mode: 'local',
            editable: false,
            value: defaultValue
        });
    },
    setValue: function(value) {

        XG.Control.LocalCombo.superclass.setValue.call(this, value);
    }
});
Ext.reg('localcombo', XG.Control.LocalCombo);



Ext.ns("XG.Control.LookUpEdit");
XG.Control.LookUpEdit = Ext.extend(Ext.Window, {

});
Ext.reg('lookup', XG.Control.LocalCombo);


Ext.ns("XG.Form.OneToManyFields");
XG.Form.OneToManyFields = Ext.extend(Ext.form.FieldSet, {
    constructor: function(config) {
        this.items = [{

            xtype: 'fieldset',
            layout: 'fit',
            items: [{
                xtype: 'basegrid',
                columes: config.columes,
                tbar: [{
                        text: '添加',
                        handler: function() {

                        }
                    },
                    {
                        text: '移除',
                        handler: function() {

                        }
                    }
                ]
            }]
        }];
        XG.Form.OneToManyFields.superclass.constructor.call(this, config);
    },
    fill: function(value) {

    }
});




function GET(url, json, success, fail) {

    Ext.Ajax.request({
        url: url,
        method: "get",
        params: {
            data: json
        },
        success: function(form) {
            var action = form.responseJSON;
            if (success) {
                success(action);
                return;
            }
            if (action && action.message != "OK") {
                alert(action.message);
            }
        },
        failure: function(form) {
            var action = form.responseJSON;
            if (fail) {
                fail(action);
                return;
            }
            if (action && 'result' in action) {
                if ('msg' in action.result) {
                    error(action.result.msg);
                }
            } else {
                error('发生异常!');
            }
        }
    });
}

function POST(url, json, success, fail) {

    Ext.Ajax.request({
        url: url,
        method: "post",
        params: json,
        success: function(form) {
            var action = form.responseJSON;
            if (success) {
                success(action);
                return;
            }
            if (action && action.message != "OK") {
                alert(action.message);
            }
        },
        failure: function(form) {
            var action = form.responseJSON;
            if (fail) {
                fail(action);
                return;
            }
            if (action && 'result' in action) {
                if ('msg' in action.result) {
                    error(action.result.msg);
                }
            } else {
                error('发生异常!');
            }
        }
    });
}