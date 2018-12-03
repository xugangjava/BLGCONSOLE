Ext.onReady(function () {
    var main_left_tree = Ext.getCmp('main_left_tree');

    function verify_status(value) {
        return value ? '支付成功' : '支付失败';
    }

    function pwd() {
        return "*********";
    }

    var nopay=true;
    main_left_tree.getRootNode().appendChild({
        text: '币商管理平台',
        iconCls: 'Bulletright',
        id:"root2",
        expanded: true,
        children: [{
            text: '玩家列表',
            leaf: true,
            iconCls: 'Bulletright',
            view: {
                xtype: 'panel',
                layout: {
                    type: 'vbox',
                    padding: '1',
                    align: 'stretch',
                    html: ''
                },
                border: false,
                flex: 6,
                nopadding: false,
                items: [{
                    xtype: 'form',
                    nopadding: true,
                    flex: 1,
                    padding: 10,
                    id: 'user_search_form',
                    defaultType: 'textfield',
                    items: [
                        {fieldLabel: '用户ID', name: 'UserID', xtype: 'numberfield'},
                        {fieldLabel: '用户名', name: 'UserName'},
                        {fieldLabel: '昵称', name: 'NickName'},
                    ],
                    buttons: [
                        {
                            text: '添加筹码',
                            handler: function () {
                                RefreshTimeOut();
                                var me = Ext.getCmp('user_grid');
                                var json = me.getFirstSel();
                                if (!json) return;
                                var pk = json.pk;
                                var store = me.getStore();
                                var win = new XG.Control.SimpelPoupForm({
                                    layout: 'form',
                                    title: '添加筹码',
                                    width: 400,
                                    height: 380,
                                    fieldWidth: 250,
                                    url: '/coin/player_list/?add_chips=1',
                                    items: [
                                        {fieldLabel: '用户ID', name: 'pk', readOnly: true},
                                        {fieldLabel: '昵称', name: 'nickname', readOnly: true},
                                        {
                                            fieldLabel: 'NT',
                                            xtype: 'remotecombo',
                                            name: 'payid',
                                            url: '/coin/player_list/?combo=1'
                                        },
                                        {fieldLabel: 'CHIPS', name: 'CHIPS'},
                                        {fieldLabel: '备注', name: 'REMARK', xtype: "textarea", maxLength: 30}
                                    ],
                                    success: function () {
                                        alert('筹码发放成功!');
                                        store.reload();
                                    }
                                });
                                win.fill(json);
                                win.show();
                            }
                        },
                        {
                            text: '用户详细信息',
                            handler: function () {
                                var grid = Ext.getCmp('user_grid');
                                var json = grid.getFirstSel();
                                UINFO(json.pk);
                            }
                        },
                        {
                            text: '重置查询条件',
                            handler: function () {
                                var form = Ext.getCmp('user_search_form').getForm();
                                form.reset();
                            }
                        },
                        {
                            text: '查询',
                            handler: function () {
                                RefreshTimeOut();
                                var form = Ext.getCmp('user_search_form');
                                var obj = form.getForm().getValues();
                                var grid = Ext.getCmp('user_grid');
                                grid.search(obj);
                            }
                        }
                    ]
                }, {
                        xtype: 'basegrid',
                        action: '/coin/player_list/',
                        FW: 600,
                        FH: 425,
                        flex: 4,
                        id: 'user_grid',
                        notbar:true,
                        columes: [
                            {header: '用户ID', dataIndex: 'pk', width: 120},
                            {header: '用户名', dataIndex: 'phone', width: 120},
                            {header: '昵称', dataIndex: 'nickname', width: 120},
                            {header: '金钱', dataIndex: 'chips', width: 120},
                            {header: '积分', dataIndex: 'lotto', width: 100},
                            {header: '充值金额', dataIndex: 'moneyconsume', width: 100},
                            {header: '当前版本', dataIndex: 'version', width: 100}
                        ]
                    }
                ]
            }
        }, {
            text: '筹码变动日志',
            leaf: true,
            iconCls: 'Bulletright',
            view: {
                xtype: 'panel',
                layout: {
                    type: 'vbox',
                    padding: '1',
                    align: 'stretch',
                    html: ''
                },
                items: [{
                    xtype: 'form',
                    flex: 2,
                    padding: 10,
                    id: 'blg_coin_usr_chips_change_log',
                    items: [
                        {fieldLabel: '玩家ID', xtype: 'textfield', name: 'uid'},
                        {fieldLabel: '用户名', xtype: 'textfield', name: 'name'},
                        {fieldLabel: '昵称', xtype: 'textfield', name: 'nick'},
                        {fieldLabel: '开始时间', xtype: 'datefield', name: 'start_time', format: 'Y-m-d'},
                        {fieldLabel: '结束时间', xtype: 'datefield', name: 'end_time', format: 'Y-m-d'}
                    ],
                    buttons: [{
                        iconCls: 'Databaseedit',
                        text: '查询',
                        handler: function () {
                            var form = Ext.getCmp('blg_coin_usr_chips_change_log');
                            var grid = Ext.getCmp('blg_coin_usr_chips_change_log_grid');
                            var json = form.getForm().getValues();
                            grid.search(json);
                        }
                    }]
                }, {
                    xtype: 'basegrid',
                    action: '/coin/chips_change_log/',
                    flex: 4,
                    id: 'blg_coin_usr_chips_change_log_grid',
                    tbar: [{
                        text: '用户详细信息',
                        iconCls: 'User',
                        handler: function () {
                            var grid = Ext.getCmp('blg_coin_usr_chips_change_log_grid');
                            var json = grid.getFirstSel();
                            if (!json || !json.usrId) return;
                            UINFO(json.usrId);
                        }
                    }],
                    columes: [
                        {header: '币商ID', dataIndex: 'CID', width: 120},
                        {header: '币商用户名', dataIndex: 'CUSRNAME', width: 120},
                        {header: '币商昵称', dataIndex: 'CNICKNAME', width: 120},
                        {header: '变更前额度', dataIndex: 'BEFORE_CHIPS', width: 120},
                        {header: '变更后额度', dataIndex: 'AFTER_CHIPS', width: 120},
                        {header: '变更额度', dataIndex: 'CHANGE_CHIPS', width: 120},
                        {header: '变更原因', dataIndex: 'REASON', width: 120},
                        {header: '变更时间', dataIndex: 'DT', width: 120},
                        {header: '玩家ID', dataIndex: 'usrid', width: 120},
                        {header: '当前筹码', dataIndex: 'chips', width: 120},
                        {header: '玩家用户名', dataIndex: 'phone', width: 120},
                        {header: '玩家昵称', dataIndex: 'nickname', width: 120},
                        {header: '充值金额', dataIndex: 'moneyconsume', width: 120}
                    ]
                }]
            }
        }, {
            text: '订单查询',
            leaf: true,
            iconCls: 'Bulletright',
            view: {
                xtype: 'panel',
                layout: {
                    type: 'vbox',
                    padding: '1',
                    align: 'stretch',
                    html: ''
                },
                items: [{
                    xtype: 'form',
                    flex: 4,
                    padding: 10,
                    id: 'coin_pay_order_search_from',
                    items: [
                        { fieldLabel: '玩家ID', xtype: 'textfield', name: 'uid' },
                        { fieldLabel: '用户名', xtype: 'textfield', name: 'name' },
                        { fieldLabel: '昵称', xtype: 'textfield', name: 'nick' },
                        { fieldLabel: '开始时间', xtype: 'datefield', name: 'start_time',format: 'Y-m-d'  },
                        { fieldLabel: '结束时间', xtype: 'datefield', name: 'end_time' ,format: 'Y-m-d' }
                    ],
                    buttons: [{
                        iconCls: 'Databaseedit',
                        text: '查询',
                        handler: function () {
                            var form = Ext.getCmp('coin_pay_order_search_from');
                            var grid = Ext.getCmp('coin_pay_order_grid');
                            var json = form.getForm().getValues();
                            grid.search(json);
                        }
                    }]
                }, {
                    xtype: 'basegrid',
                    action: '/coin/pay_order_list/',
                    flex: 4,
                    id: 'coin_pay_order_grid',
                    tbar: [{
                        text: '用户详细信息',
                        iconCls: 'User',
                        handler: function () {
                            var grid = Ext.getCmp('coin_pay_order_grid');
                            var json = grid.getFirstSel();
                            if (!json) return;
                            UINFO(json.usrId);
                        }
                    },{
                        text: '切换显示未支付',
                        iconCls: 'Databaserefresh',
                        handler: function () {
                            var form = Ext.getCmp('coin_pay_order_search_from');
                            var grid = Ext.getCmp('coin_pay_order_grid');
                            var json = form.getForm().getValues();
                            nopay=json.nopay=!nopay;
                            grid.search(json);
                        }
                    }],
                    columes: [
                        { header: '玩家ID', dataIndex: 'usrId', width: 120 },
                        { header: '支付金额', dataIndex: 'realdollar', width: 120 },
                        { header: '购买筹码', dataIndex: 'chips', width: 120 },
                        { header: '玩家用户名', dataIndex: 'phone', width: 120 },
                        { header: '玩家昵称', dataIndex: 'nickname', width: 120 },
                        { header: '支付方式', dataIndex: 'paychannelname', width: 120 },
                        { header: '订单状态', dataIndex: 'verify', width: 100 , renderer: verify_status},
                        { header: '订单编号', dataIndex: 'orderid', width: 100 },
                        { header: '订单交易号', dataIndex: 'payNum', width: 100 },
                        { header: '游戏名称', dataIndex: 'versionname', width: 120 },
                        { header: '游戏版本', dataIndex: 'versionid', width: 120 },
                        { header: '创建时间', dataIndex: 'tim', width: 120 },
                        { header: '玩家等级', dataIndex: 'level', width: 120 },
                        { header: '玩家总充值', dataIndex: 'moneyconsume', width: 120 }
                    ]
                }]
            }
        },{
            text: '跑马灯消息',
            leaf: true,
            iconCls: 'Bulletright',
            view: {
                xtype: 'basegrid',
                title: '跑马灯消息',
                action: '/coin/race_lamp_list/',
                id: 'broatcast_grid',
                flex: 2,
                tbar: [{
                    iconCls: 'Databaseadd',
                    text: '添加跑马灯消息',
                    handler: function () {
                        var me = Ext.getCmp('broatcast_grid');
                        var store = me.getStore();
                        var win = new XG.Control.SimpelPoupForm({
                            layout: 'form',
                            title: '添加版本',
                            width: 400,
                            height: 380,
                            fieldWidth: 250,
                            url: '/coin/race_lamp_list/?add=1',
                            items: [
                                {fieldLabel: '发送次数', name: 'repeatcount'},
                                {fieldLabel: '时间间隔(秒)', name: 'repeatgap'},
                                {fieldLabel: '发送渠道', name: 'channel',allowBlank:true},
                                {fieldLabel: '消息内容', name: 'content', xtype: 'textarea',allowBlank:true},
                                {fieldLabel: '消息内容EN', name: 'en_content', xtype: 'textarea',allowBlank:true}
                            ],
                            success: function () {
                                alert('添加成功!');
                                store.reload();
                            }
                        });
                        win.show();
                    }
                }, {
                    iconCls: 'Databasedelete',
                    text: '删除跑马灯消息',
                    handler: function () {
                        var me = Ext.getCmp('broatcast_grid');
                        var json = me.getFirstSel();
                        me.deleteRow('/coin/race_lamp_list/?del=1');
                    }
                }, {
                    text: '刷新',
                    iconCls: 'Databaserefresh',
                    handler: function () {
                        var me = Ext.getCmp('broatcast_grid');
                        me.getStore().reload();
                    }
                }],
                nopadding: true,
                columes: [
                    {header: 'ID', dataIndex: 'pk', width: 70},
                    {header: '消息内容', dataIndex: 'content', width: 240},
                    {header: '发送次数', dataIndex: 'repeatcount', width: 120},
                    {header: '上次发送时间', dataIndex: 'noticetime', width: 120},
                    {header: '发送渠道', dataIndex: 'channel', width: 120}
                ]
            }
        }, {
            text: '密码修改',
            leaf: true,
            iconCls: 'Bulletright',
            view: {
                xtype: 'panel',
                width:600,
                layout: {
                    type: 'vbox',
                    padding: '1',
                    align: 'stretch',
                    html: ''
                },
                items: [{
                    xtype: 'form',
                    id:"editpwdform",
                    items: [
                        {fieldLabel: '当前密码', xtype: 'textfield', name: 'curpwd', inputType: 'password'},
                        {fieldLabel: '新密码', xtype: 'textfield', name: 'newpwd', inputType: 'password'},
                        {fieldLabel: '确认新密码', xtype: 'textfield', name: 'cnewpwd', inputType: 'password'}
                    ],
                    buttons: [{
                        iconCls: 'Databaseedit',
                        text: '修改密码',
                        handler: function () {
                            var form = Ext.getCmp('editpwdform');
                            var json = form.getForm().getValues();
                            if(!json.newpwd||!json.cnewpwd||!json.curpwd){
                                alert("密码不能为空");
                                return;
                            }
                            if(json.newpwd!=json.cnewpwd){
                                alert("新密码确认不一致");
                                return;
                            }
                            if(!json.newpwd||json.newpwd.length<6||
                                !json.cnewpwd||json.cnewpwd.length<6){
                                alert("密码长度必须6位或以上");
                                return;
                            }
                            POST( '/coin/edit_password/',json,function (json) {
                                if(json.success){
                                    alert("密码修改成功");
                                }else{
                                    alert(json.message);
                                }
                                form.reset();
                            });
                        }
                    }]
                }]
            }
        }
        ]
    });
    main_left_tree.doLayout();

});