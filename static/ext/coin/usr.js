Ext.onReady(function () {
    var main_left_tree = Ext.getCmp('main_left_tree');
    function verify_status(value) {
        return value ? '启用' : '禁用'
    }
    main_left_tree.getRootNode().appendChild({
        text: '',
        iconCls: 'Bulletright',
        expanded: true,
        children: [{
            text: '用户列表',
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
                            text: '添加筹码-邮件发送',
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
                                        {fieldLabel: '邮件标题', name: 'email_title', value: '系统邮件'},
                                        {fieldLabel: '附件金钱', name: 'email_money', value: 0},
                                        {fieldLabel: '邮件内容', name: 'email_content', xtype: 'textarea'}
                                    ],
                                    success: function () {
                                        alert('邮件发送成功!');
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
        }]
    });
    main_left_tree.doLayout();

});