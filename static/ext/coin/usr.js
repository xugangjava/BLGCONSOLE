Ext.onReady(function () {
    var main_left_tree = Ext.getCmp('main_left_tree');

    function verify_status(value) {
        return value ? '支付成功' : '支付失败';
    }

    var nopay=true;
    main_left_tree.getRootNode().appendChild({
        text: '币商管理平台',
        iconCls: 'Bulletright',
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
                        {fieldLabel: '昵称', name: 'NickName'}
                    ],
                    buttons: [{
                        text: '重置查询条件',
                        handler: function () {
                            var form = Ext.getCmp('user_search_form').getForm();
                            form.reset();
                        }
                    },
                        {
                            text: '查询',
                            handler: function () {
                                var form = Ext.getCmp('user_search_form');
                                var obj = form.getForm().getValues();
                                var grid = Ext.getCmp('user_grid');
                                grid.search(obj);
                            }
                        }
                    ]
                },
                    {
                        xtype: 'basegrid',
                        action: '/coin/player_list/',
                        FW: 600,
                        FH: 425,
                        flex: 4,
                        id: 'user_grid',
                        tbar: [{
                            iconCls: 'Emailattach',
                            text: '添加筹码',
                            handler: function () {
                                var me = Ext.getCmp('user_grid');
                                var json = me.getFirstSel();
                                if (!json) return;
                                var pk = json.pk;
                                var store = me.getStore();
                                var win = new XG.Control.SimpelPoupForm({
                                    layout: 'form',
                                    title: '发送邮件',
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
                                        {fieldLabel: '备注', name: 'REMARK',xtype:"textarea",maxLength:30}
                                    ],
                                    success: function () {
                                        alert('筹码发放成功!');
                                        store.reload();
                                    }
                                });
                                win.fill(json);
                                win.show();
                            }
                        }, {
                            text: '用户详细信息',
                            iconCls: 'User',
                            handler: function () {
                                var grid = Ext.getCmp('user_grid');
                                var json = grid.getFirstSel();
                                UINFO(json.pk);
                            }
                        }],
                        columes: [
                            {header: '用户ID', dataIndex: 'pk', width: 120},
                            {header: '用户名', dataIndex: 'phone', width: 120},
                            {header: '昵称', dataIndex: 'nickname', width: 120},
                            {header: '金钱', dataIndex: 'chips', width: 120},
                            {header: '积分', dataIndex: 'lotto', width: 100},
                            {header: '充值金额', dataIndex: 'moneyconsume', width: 100},
                            {header: '筹码余额', dataIndex: 'chipslimit', width: 100},
                            {header: '当前版本', dataIndex: 'version', width: 100},
                            {header: '注册版本', dataIndex: 'regversion', width: 100},
                            {header: '是否禁用', dataIndex: 'disable', width: 100},
                            {header: '上次登录时间', dataIndex: 'lastLogintm'},
                            {header: 'LEVEL', dataIndex: 'level'},
                            {header: 'EXP', dataIndex: 'exp'},
                            {header: '运气值', dataIndex: 'luck'},
                            {header: '注册IP', dataIndex: 'regip'},
                            {header: '注册时间', dataIndex: 'regtime'},
                            {header: '注册渠道', dataIndex: 'versionid'},
                            {header: '注册设备', dataIndex: 'regdevice'},
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
                    action: '/blg/coin_usr_chips_change_log/',
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
                        {header: '当前额度', dataIndex: 'CCHIPS', width: 120},
                        {header: '玩家ID', dataIndex: 'usrId', width: 120},
                        {header: '购买筹码', dataIndex: 'chips', width: 120},
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
                    flex: 2,
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
        }]
    });
    main_left_tree.doLayout();

});