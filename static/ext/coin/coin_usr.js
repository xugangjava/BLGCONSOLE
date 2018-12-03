Ext.onReady(function () {
    var main_left_tree = Ext.getCmp('main_left_tree');

    function verify_status(value) {
        return value ? '启用' : '禁用';
    }

    function pwd() {
        return "*********";
    }

    main_left_tree.getRootNode().firstChild.appendChild({
            text: '分销商管理',
            leaf: true,
            iconCls: 'Bulletright',
            view: {
                xtype: 'basegrid',
                action: '/coin/coin_usr_list/',
                flex: 4,
                id: 'coin_usr_grid',
                nopadding:true,
                tbar: [{
                    text: '添加分销商',
                    iconCls: 'User',
                    handler: function () {
                        var me = Ext.getCmp('coin_usr_grid');
                        var store = me.getStore();
                        var win = new XG.Control.SimpelPoupForm({
                            layout: 'form',
                            title: '添加分销商',
                            width: 400,
                            height: 380,
                            fieldWidth: 250,
                            url: '/coin/coin_usr_list/?add=1',
                            items: [
                                {fieldLabel: '用户名', name: 'USRNAME'},
                                {fieldLabel: '昵称', name: 'NICKNAME'},
                                {fieldLabel: '密码', name: 'PWD'}
                            ],
                            success: function () {
                                alert('添加成功!');
                                store.reload();
                            }
                        });
                        win.show();
                    }
                },{
                    text: '修改分销商',
                    iconCls: 'Databaseedit',
                    handler: function () {
                        var me = Ext.getCmp('coin_usr_grid');
                        var store = me.getStore();
                        var json = me.getFirstSel();
                        if (!json) return;

                        var win = new XG.Control.SimpelPoupForm({
                            layout: 'form',
                            title: '修改分销商',
                            width: 400,
                            height: 380,
                            fieldWidth: 250,
                            url: '/coin/coin_usr_list/?edit=1',
                            items: [
                                {fieldLabel: 'ID', name: 'ID',readOnly:true},
                                {fieldLabel: '用户名', name: 'USRNAME',readOnly:true},
                                {fieldLabel: '昵称', name: 'NICKNAME'},
                                {fieldLabel: '密码', name: 'PWD'},
                                {
                                    fieldLabel: '是否禁用', name: 'ENABLE',
                                    xtype: 'localcombo',
                                    data: [
                                        [1,'启用'],
                                        [0,'禁用']
                                    ]
                                },
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
                ]
            }
        });
    main_left_tree.doLayout();

});