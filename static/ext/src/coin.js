Ext.onReady(function () {
    var main_left_tree = Ext.getCmp('main_left_tree');
    function verify_status(value) {
        return value ? '启用' : '禁用'
    }

    function pwd() {
        return "*********";
    }

    main_left_tree.getRootNode().appendChild({
        text: '币商管理',
        iconCls: 'Bulletright',
        expanded: true,
        children: [
        {
            text: '币商列表',
            leaf: true,
            iconCls: 'Bulletright',
            view: {
                xtype: 'basegrid',
                action: '/blg/coin_usr_list/',
                flex: 4,
                id: 'coin_usr_grid',
                nopadding:true,
                tbar: [{
                    text: '添加币商',
                    iconCls: 'User',
                    handler: function () {
                        var me = Ext.getCmp('coin_usr_grid');
                        var store = me.getStore();
                        var win = new XG.Control.SimpelPoupForm({
                            layout: 'form',
                            title: '添加币商',
                            width: 400,
                            height: 380,
                            fieldWidth: 250,
                            url: '/blg/coin_usr_list/?add=1',
                            items: [
                                {fieldLabel: '用户名', name: 'USRNAME'},
                                {fieldLabel: '昵称', name: 'NICKNAME'},
                                {fieldLabel: '密码', name: 'PWD'},
                                {fieldLabel: '筹码额度', name: 'CHIPS'}
                            ],
                            success: function () {
                                alert('添加成功!');
                                store.reload();
                            }
                        });
                        win.show();
                    }
                },{
                    text: '修改币商',
                    iconCls: 'Databaseedit',
                    handler: function () {
                        var me = Ext.getCmp('coin_usr_grid');
                        var store = me.getStore();
                        var json = me.getFirstSel();
                        if (!json) return;

                        var win = new XG.Control.SimpelPoupForm({
                            layout: 'form',
                            title: '修改币商',
                            width: 400,
                            height: 380,
                            fieldWidth: 250,
                            url: '/blg/coin_usr_list/?edit=1',
                            items: [
                                {fieldLabel: 'ID', name: 'ID',readOnly:true},
                                {fieldLabel: '用户名', name: 'USRNAME',readOnly:true},
                                {fieldLabel: '昵称', name: 'NICKNAME'},
                                {fieldLabel: '密码', name: 'PWD'},
                                {fieldLabel: '筹码额度', name: 'CHIPS'},
                                {fieldLabel: 'ENABLE', name: 'ENABLE'},
                                {fieldLabel: '游戏内ID', name: 'GAME_UID'}
                            ],
                            success: function () {
                                alert('修改成功!');
                                store.reload();
                            }
                        });
                        win.fill(json);
                        win.show();
                    }
                },{
                    text: '刷新',
                    iconCls: 'Databaserefresh',
                    handler: function () {
                        var me = Ext.getCmp('coin_usr_grid');
                        var store = me.getStore();
                        store.reload();
                    }
                }],
                columes: [
                    { header: 'ID', dataIndex: 'ID', width: 120 },
                    { header: '用户名', dataIndex: 'USRNAME', width: 120 },
                    { header: '昵称', dataIndex: 'NICKNAME', width: 120 },
                    { header: '当前额度', dataIndex: 'CHIPS', width: 120 },
                    { header: 'ENABLE', dataIndex: 'ENABLE', width: 120 ,renderer: verify_status},
                    { header: 'PWD', dataIndex: 'PWD', width: 120 ,renderer: pwd},
                    { header: '游戏内ID', dataIndex: 'GAME_UID', width: 120},
                    { header: '上级币商ID', dataIndex: 'PARENT', width: 120},
                ]
            }
        },
        {
            text: '币商计费点',
            leaf: true,
            iconCls: 'Bulletright',
            view: {
                xtype: 'basegrid',
                action: '/blg/coin_usr_chips_config/',
                flex: 4,
                id: 'coin_usr_config_grid',
                nopadding:true,
                tbar: [{
                    text: '添加计费点',
                    iconCls: 'User',
                    handler: function () {
                        var me = Ext.getCmp('coin_usr_config_grid');
                        var store = me.getStore();
                        var win = new XG.Control.SimpelPoupForm({
                            layout: 'form',
                            title: '添加计费点',
                            width: 400,
                            height: 380,
                            fieldWidth: 250,
                            url: '/blg/coin_usr_chips_config/?add=1',
                            items: [
                                {fieldLabel: 'CHIPS', name: 'CHIPS'},
                                {fieldLabel: 'RMB', name: 'RMB'},
                                {fieldLabel: 'NT', name: 'NT'}
                            ],
                            success: function () {
                                alert('添加成功!');
                                store.reload();
                            }
                        });
                        win.show();
                    }
                },{
                    text: '修改计费点',
                    iconCls: 'Databaseedit',
                    handler: function () {
                        var me = Ext.getCmp('coin_usr_config_grid');
                        var store = me.getStore();
                        var json = me.getFirstSel();
                        if (!json) return;

                        var win = new XG.Control.SimpelPoupForm({
                            layout: 'form',
                            title: '修改计费点',
                            width: 400,
                            height: 380,
                            fieldWidth: 250,
                            url: '/blg/coin_usr_chips_config/?edit=1',
                            items: [
                                {fieldLabel: 'ID', name: 'ID',readOnly:true},
                                {fieldLabel: 'CHIPS', name: 'CHIPS'},
                                {fieldLabel: 'RMB', name: 'RMB'},
                                {fieldLabel: 'NT', name: 'NT'}
                            ],
                            success: function () {
                                alert('修改成功!');
                                store.reload();
                            }
                        });
                        win.fill(json);
                        win.show();
                    }
                },{
                    text: '删除计费点',
                    iconCls: 'Databasedelete',
                    handler: function () {
                        var me = Ext.getCmp('coin_usr_config_grid');
                        var store = me.getStore();
                        var json = me.getFirstSel();
                        if (!json) return;

                        var win = new XG.Control.SimpelPoupForm({
                            layout: 'form',
                            title: '删除计费点',
                            width: 400,
                            height: 380,
                            fieldWidth: 250,
                            url: '/blg/coin_usr_chips_config/?delete=1',
                            items: [
                                {fieldLabel: 'ID', name: 'ID',readOnly:true},
                                {fieldLabel: 'CHIPS', name: 'CHIPS',readOnly:true},
                                {fieldLabel: 'RMB', name: 'RMB',readOnly:true},
                                {fieldLabel: 'NT', name: 'NT',readOnly:true}
                            ],
                            success: function () {
                                alert('修改成功!');
                                store.reload();
                            }
                        });
                        win.fill(json);
                        win.show();
                    }
                },{
                    text: '刷新',
                    iconCls: 'Databaserefresh',
                    handler: function () {
                        var me = Ext.getCmp('coin_usr_config_grid');
                        var store = me.getStore();
                        store.reload();
                    }
                }],
                columes: [
                    { header: 'ID', dataIndex: 'ID', width: 120 },
                    { header: 'RMB', dataIndex: 'RMB', width: 120 },
                    { header: 'NT', dataIndex: 'NT', width: 120 },
                    { header: 'CHIPS', dataIndex: 'CHIPS', width: 120 }
                ]
            }
        },
        {
            text: '筹码变动日志',
            leaf: true,
            iconCls: 'Bulletright',
            view:{
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
                            if (!json||!json.usrId) return;
                            UINFO(json.usrId);
                        }
                    }],
                    columes: [
                        { header: '币商ID', dataIndex: 'CID', width: 120 },
                        { header: '币商用户名', dataIndex: 'CUSRNAME', width: 120 },
                        { header: '币商昵称', dataIndex: 'CNICKNAME', width: 120 },
                        { header: '变更前额度', dataIndex: 'BEFORE_CHIPS', width: 120 },
                        { header: '变更后额度', dataIndex: 'AFTER_CHIPS', width: 120 },
                        { header: '变更额度', dataIndex: 'CHANGE_CHIPS', width: 120 },
                        { header: '变更原因', dataIndex: 'REASON', width: 120 },
                        {header: '变更时间', dataIndex: 'DT', width: 120},
                        { header: '玩家ID', dataIndex: 'usrid', width: 120 },
                        { header: '当前筹码', dataIndex: 'chips', width: 120 },
                        { header: '玩家用户名', dataIndex: 'phone', width: 120 },
                        { header: '玩家昵称', dataIndex: 'nickname', width: 120 },
                        { header: '充值金额', dataIndex: 'moneyconsume', width: 120 }
                    ]
                }]
            }
        }]
    });
    main_left_tree.doLayout();

});