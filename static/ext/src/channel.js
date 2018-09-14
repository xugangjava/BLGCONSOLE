Ext.onReady(function () {

    var main_left_tree = Ext.getCmp('main_left_tree');
    var game_grid = Ext.id(),
        version_grid = Ext.id(),
        broatcast_grid = Ext.id(),
        channel_grid = Ext.id();

    main_left_tree.getRootNode().appendChild({
        text: '系统管理',
        iconCls: 'Bulletright',
        expanded: true,
        children: [{
            text: '渠道列表',
            leaf: true,
            iconCls: 'Bulletright',
            view: {
                xtype: 'basegrid',
                title: '渠道列表',
                action: '/blg/channel_list/',
                id: channel_grid,
                flex: 2,
                tbar: [{
                    iconCls: 'Databaseedit',
                    text: '修改信息',
                    handler: function () {
                        var me = Ext.getCmp(channel_grid);
                        var json = me.getFirstSel();
                        if (!json) return;
                        var store = me.getStore();
                        var win = new XG.Control.SimpelPoupForm({
                            layout: 'form',
                            title: '修改版本',
                            width: 400,
                            height: 380,
                            fieldWidth: 250,
                            url: '/blg/do_edit_channel/',
                            items: [
                                {xtype: 'hidden', name: 'pk', readOnly: true},
                                {fieldLabel: '渠道名称', name: 'NAME', readOnly: true},
                                {fieldLabel: '渠道编号', name: 'NO', readOnly: true},
                                {fieldLabel: '备注', name: 'remark'},
                                {
                                    fieldLabel: '游戏平台',
                                    name: 'platform',
                                    xtype: 'localcombo',
                                    data: [
                                        ['IOS', 'IOS'],
                                        ['ANDROID', 'ANDROID']
                                    ]
                                },
                                {fieldLabel: 'IOS APPID 评论跳转', name: 'app_id'},
                                {fieldLabel: '推送KEY', name: 'push_key'},
                                {fieldLabel: '推送SECRET', name: 'push_mestersecret'},
                                {fieldLabel: '推送SECRET', name: 'push_mestersecret'}
                            ],
                            success: function () {
                                alert('修改成功!');
                                store.reload();
                                win.close();
                            }
                        });
                        win.fill(json);
                        win.show();
                    }
                }],
                nopadding: true,
                columes: [
                    {header: 'ID', dataIndex: 'pk', width: 70},
                    {header: '渠道名称', dataIndex: 'NAME', width: 120},
                    {header: '渠道编号', dataIndex: 'NO', width: 120},
                    {header: '备注', dataIndex: 'remark', width: 120},
                    {header: '游戏平台', dataIndex: 'platform', width: 120},
                    {header: 'IOS APPID 评论跳转', dataIndex: 'app_id', width: 120},
                    {header: '推送KEY', dataIndex: 'push_key', width: 120},
                    {header: '推送SECRET', dataIndex: 'push_mestersecret', width: 80}
                ]
            }
        }, {
            text: '版本列表',
            leaf: true,
            iconCls: 'Bulletright',
            view: {
                xtype: 'basegrid',
                title: '版本',
                action: '/blg/version_list/',
                id: version_grid,
                flex: 2,
                tbar: [{
                    iconCls: 'Databaseadd',
                    text: '添加版本',
                    handler: function () {
                        var me = Ext.getCmp(version_grid);
                        var store = me.getStore();
                        var win = new XG.Control.SimpelPoupForm({
                            layout: 'form',
                            title: '添加版本',
                            width: 400,
                            height: 380,
                            fieldWidth: 250,
                            url: '/blg/do_add_version/',
                            items: [{
                                fieldLabel: '渠道',
                                xtype: 'remotecombo',
                                name: 'channel_id',
                                url: '/blg/combo_channel/'
                            },
                                {fieldLabel: '版本号', name: 'name'},
                                {
                                    fieldLabel: '是否审核',
                                    name: 'is_approve',
                                    xtype: 'localcombo',
                                    data: [
                                        [1, '是'],
                                        [0, '否']
                                    ]
                                },
                                {fieldLabel: '语言编号', name: 'lan_id', value: '41'}
                            ],
                            success: function () {
                                alert('添加成功!');
                                store.reload();
                            }
                        });
                        win.show();
                    }
                }, {
                    iconCls: 'Databaseedit',
                    text: '修改版本',
                    handler: function () {
                        var me = Ext.getCmp(version_grid);
                        var json = me.getFirstSel();
                        if (!json) return;
                        var store = me.getStore();
                        var win = new XG.Control.SimpelPoupForm({
                            layout: 'form',
                            title: '修改版本',
                            width: 400,
                            height: 380,
                            fieldWidth: 250,
                            url: '/blg/do_edit_version/',
                            items: [
                                {xtype: 'hidden', name: 'pk'},
                                {
                                    fieldLabel: '渠道',
                                    xtype: 'remotecombo',
                                    name: 'CID',
                                    url: '/blg/combo_channel/'
                                },
                                {fieldLabel: '版本号', name: 'VNAME'},
                                {
                                    fieldLabel: '是否审核',
                                    name: 'IS_APPROVE',
                                    xtype: 'localcombo',
                                    data: [
                                        [true, '是'],
                                        [false, '否']
                                    ]
                                },
                                {fieldLabel: '语言编号', name: 'LAN_ID', value: '41'},
                                {fieldLabel: '升级包名', name: 'UPDATE_LINK',allowBlank:true}
                            ],
                            success: function () {
                                alert('修改成功!');
                                store.reload();
                                win.close();
                            }
                        });
                        win.fill(json);
                        win.show();
                    }
                }, {
                    iconCls: 'Databasedelete',
                    text: '删除版本',
                    handler: function () {
                        var me = Ext.getCmp(version_grid);
                        var json = me.getFirstSel();
                        me.deleteRow('/blg/do_del_version/');
                    }
                }],
                nopadding: true,
                columes: [
                    {header: 'ID', dataIndex: 'pk', width: 70},
                    {header: '渠道名称', dataIndex: 'NAME', width: 120},
                    {header: '渠道编号', dataIndex: 'NO', width: 120},
                    {header: '版本名称', dataIndex: 'VNAME', width: 120},
                    {header: '更新包名', dataIndex: 'UPDATE_LINK', width: 120},
                    {header: '版本人数', dataIndex: 'USR_COUNT', width: 120},
                    {header: '升级人数', dataIndex: 'UPDATE_COUNT', width: 120},
                    {header: '是否审核', dataIndex: 'IS_APPROVE', width: 80, renderer: yesno},
                    {header: '备注信息', dataIndex: 'remark', width: 120},
                    {header: '渠道ID', dataIndex: 'CID', width: 120},
                    {header: '语言ID', dataIndex: 'LAN_ID', width: 120}
                ]
            }
        }, {
            text: '跑马灯消息',
            leaf: true,
            iconCls: 'Bulletright',
            view: {
                xtype: 'basegrid',
                title: '跑马灯消息',
                action: '/blg/race_lamp_list/',
                id: broatcast_grid,
                flex: 2,
                tbar: [{
                    iconCls: 'Databaseadd',
                    text: '添加跑马灯消息',
                    handler: function () {
                        var me = Ext.getCmp(broatcast_grid);
                        var store = me.getStore();
                        var win = new XG.Control.SimpelPoupForm({
                            layout: 'form',
                            title: '添加版本',
                            width: 400,
                            height: 380,
                            fieldWidth: 250,
                            url: '/blg/do_add_race_lamp/?m=add',
                            items: [
                                {fieldLabel: '发送次数', name: 'repeatcount'},
                                {fieldLabel: '时间间隔(秒)', name: 'repeatgap'},
                                {fieldLabel: '消息内容', name: 'content', xtype: 'textarea'},
                                {fieldLabel: '消息内容EN', name: 'en_content', xtype: 'textarea'}
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
                        var me = Ext.getCmp(broatcast_grid);
                        var json = me.getFirstSel();
                        me.deleteRow('/blg/do_del_race_lamp/?m=del');
                    }
                }, {
                    text: '刷新',
                    iconCls: 'Databaserefresh',
                    handler: function () {
                        var me = Ext.getCmp(broatcast_grid);
                        me.getStore().reload();
                    }
                }],
                nopadding: true,
                columes: [
                    {header: 'ID', dataIndex: 'pk', width: 70},
                    {header: '消息内容', dataIndex: 'content', width: 240},
                    {header: '发送次数', dataIndex: 'repeatcount', width: 120},
                    {header: '上次发送时间', dataIndex: 'noticetime', width: 120}
                ]
            }
        }]
    });
    main_left_tree.doLayout();

});