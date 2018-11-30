Ext.onReady(function () {
    var main_left_tree = Ext.getCmp('main_left_tree'),
        user_grid = Ext.id(),
        email_grid = Ext.id(),
        user_avastar_grid = Ext.id(),
        user_suggest_grid = Ext.id(),
        user_search_form = Ext.id(),
        searc_user_play_log_form = Ext.id(),
        searc_user_money_diamold_log_form = Ext.id(),
        user_money_log_list_grid = Ext.id();
    main_left_tree.getRootNode().appendChild({
        text: '用户管理',
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
                    id: user_search_form,
                    defaultType: 'textfield',
                    items: [
                        {fieldLabel: '用户ID', name: 'UserID', xtype: 'numberfield'},
                        {fieldLabel: '用户名', name: 'UserName'},
                        {fieldLabel: '昵称', name: 'NickName'}
                    ],
                    buttons: [{
                        text: '重置查询条件',
                        handler: function () {
                            var form = Ext.getCmp(user_search_form).getForm();
                            form.reset();
                        }
                    },
                        {
                            text: '查询',
                            handler: function () {
                                var form = Ext.getCmp(user_search_form);
                                var obj = form.getForm().getValues();
                                var grid = Ext.getCmp(user_grid);
                                grid.search(obj);
                            }
                        }
                    ]
                },
                {
                        xtype: 'basegrid',
                        action: '/blg/user_list/',
                        FW: 600,
                        FH: 425,
                        flex: 4,
                        id: user_grid,
                        tbar: [{
                            iconCls: 'Databaseedit',
                            text: '修改',
                            handler: function () {
                                var me = Ext.getCmp(user_grid);
                                var json = me.getFirstSel();
                                if (!json) return;
                                var pk = json.pk;
                                var store = me.getStore();
                                var win = new XG.Control.SimpelPoupForm({
                                    layout: 'form',
                                    title: '修改',
                                    width: 400,
                                    height: 400,
                                    fieldWidth: 250,
                                    url: '/blg/do_edit_user_info/',
                                    items: [
                                        {fieldLabel: '用户ID', name: 'pk', readOnly: true},
                                        {fieldLabel: '用户名', name: 'phone', readOnly: true, allowBlank: true},
                                        {fieldLabel: '昵称', name: 'nickname'},
                                        {fieldLabel: '金钱', name: 'chips'},
                                        {fieldLabel: '积分', name: 'lotto'},
                                        {fieldLabel: '运气值', name: 'luck'},
                                        {fieldLabel: '等级', name: 'level'},
                                        {fieldLabel: '经验', name: 'exp'},
                                        {fieldLabel: '渠道', name: 'versionid'},
                                        {fieldLabel: '充值金额', name: 'moneyconsume'},
                                        {fieldLabel: 'DISABLE', name: 'disable'},
                                        {fieldLabel: 'TEST', name: 'test'}
                                    ],
                                    success: function () {
                                        alert('修改成功!');
                                        store.reload();
                                    }
                                });
                                win.fill(json);
                                win.show();
                            }
                        }, {
                            iconCls: 'Databasedelete',
                            text: '删除测试账号',
                            handler: function () {
                                var me = Ext.getCmp(user_grid);
                                var json = me.getFirstSel();
                                if (!json) return;
                                var pk = json.pk;
                                var store = me.getStore();
                                var win = new XG.Control.SimpelPoupForm({
                                    layout: 'form',
                                    title: '删除测试账号',
                                    width: 400,
                                    height: 400,
                                    fieldWidth: 250,
                                    url: '/blg/do_del_user_info/',
                                    items: [
                                        {fieldLabel: '用户ID', name: 'pk', readOnly: true},
                                        {fieldLabel: '用户名', name: 'phone', readOnly: true, allowBlank: true},
                                        {fieldLabel: '昵称', name: 'nickname', readOnly: true},
                                        {fieldLabel: '金钱', name: 'chips', readOnly: true},
                                        {fieldLabel: '积分', name: 'lotto', readOnly: true},
                                        {fieldLabel: '运气值', name: 'luck', readOnly: true},
                                        {fieldLabel: '等级', name: 'level', readOnly: true},
                                        {fieldLabel: '经验', name: 'exp', readOnly: true},
                                        {fieldLabel: '渠道', name: 'versionid', readOnly: true},
                                        {fieldLabel: '禁用', name: 'disable', readOnly: true}
                                    ],
                                    success: function () {
                                        alert('删除测试账号成功!');
                                        store.reload();
                                    }
                                });
                                win.fill(json);
                                win.show();
                            }
                        }, {
                            iconCls: 'Emailattach',
                            text: '发送邮件',
                            handler: function () {
                                var me = Ext.getCmp(user_grid);
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
                                    url: '/blg/do_send_user_email/',
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
                            iconCls: 'Emailmagnify',
                            text: '邮件历史记录',
                            handler: function () {
                                var me = Ext.getCmp(user_grid);
                                var json = me.getFirstSel();
                                if (!json) return;
                                var pk = json.pk;
                                var store = me.getStore();
                                var win = new Ext.Window({
                                    layout: 'fit',
                                    title: '邮件历史记录',
                                    width: 800,
                                    height: 500,
                                    items: [{
                                        xtype: 'basegrid',
                                        action: '/ffqp/console/users/?m=email_list&uid=' + pk,
                                        id: email_grid,
                                        not_main_grid: true,
                                        tbar: [{
                                            iconCls: 'Databaseedit',
                                            text: '删除',
                                            handler: function () {
                                                var grid = Ext.getCmp(email_grid);
                                                var ids = grid.getSel();
                                                if (!ids) return;
                                                POST('/ffqp/console/users/?m=email_delete', {
                                                    ids: ids
                                                }, function () {
                                                    // var pk = json.pk;
                                                    alert('删除成功');
                                                    grid.reload();
                                                });
                                            }
                                        }],
                                        columes: [
                                            {header: 'ID', dataIndex: 'id', width: 80},
                                            {header: '邮件标题', dataIndex: 'title', width: 120},
                                            {header: '邮件内容', dataIndex: 'conent', width: 120},
                                            {header: '发送时间', dataIndex: 'send_time', width: 120},
                                            {header: '是否阅读', dataIndex: 'is_read', width: 80, renderer: yesno},
                                            {header: '是否领取', dataIndex: 'is_get', width: 80, renderer: yesno}
                                        ]
                                    }]
                                });
                                win.show();
                            }
                        }, {
                            text: '用户详细信息',
                            iconCls: 'User',
                            handler: function () {
                                var grid = Ext.getCmp(user_grid);
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
                            {header: '筹码余额LOW', dataIndex: 'chipslow', width: 100},
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
                            {header: '测试账号', dataIndex: 'test',renderer:yesno}
                        ]
                    }
                ]
            }
        }, {
            text: '头像审核',
            leaf: true,
            iconCls: 'Bulletright',
            view: {
                xtype: 'basegrid',
                action: '/blg/users_avastar_approve_list/',
                FW: 600,
                FH: 425,
                id: user_avastar_grid,
                tbar: [{
                    iconCls: 'Databaseedit',
                    text: '批量审核',
                    handler: function () {
                        var me = Ext.getCmp(user_avastar_grid);
                        var ids = me.getSel();
                        if (!ids || !ids.length) return;
                        // var pk = json.pk;
                        var store = me.getStore();
                        var win = Ext.Msg.show({
                            title: "批量审核头像",
                            msg: "批量审核用户头像",
                            fn: function (btn) {
                                var is_pass = -1;
                                if ('yes' == btn) {
                                    is_pass = 1;
                                } else if ('no' == btn) {
                                    is_pass = 0;
                                }
                                if (is_pass >= 0) {
                                    Ext.Ajax.request({
                                        url: '/blg/do_users_avastar_approve/',
                                        method: "post",
                                        params: {
                                            ids: ids.join(),
                                            is_pass: is_pass
                                        },
                                        success: function (form) {
                                            var json = Ext.decode(form.responseText);
                                            ;
                                            alert("审核成功!");
                                            store.reload();
                                        }
                                    });
                                }
                            },
                            buttons: {yes: '审核通过', no: '审核不通过', cancel: '取消'},
                            icon: Ext.MessageBox.QUESTION
                        });
                    }
                }],
                columes: [
                    {header: 'ID', dataIndex: 'pk', width: 80},
                    {header: '玩家ID', dataIndex: 'UID', width: 120},
                    {
                        header: '图片',
                        dataIndex: 'IMAGE_URL',
                        width: 220,
                        renderer: function (val) {
                            return '<img width="100" height="100" src="' + val + '?r=' + Math.random() + '">';
                        }
                    },
                    {header: '上传时间', dataIndex: 'UPLOAD_TIME', width: 120}
                ]
            }
        }, {
            text: '用户反馈',
            leaf: true,
            iconCls: 'Bulletright',
            view: {
                xtype: 'basegrid',
                action: '/blg/user_suggest_list/',
                id: user_suggest_grid,
                tbar: [{
                    iconCls: 'Databaseedit',
                    text: '回复',
                    handler: function () {
                        var me = Ext.getCmp(user_suggest_grid);
                        var json = me.getFirstSel();
                        if (!json) return;
                        var win = new XG.Control.SimpelPoupForm({
                            layout: 'form',
                            title: '回复用户消息',
                            width: 400,
                            height: 450,
                            fieldWidth: 250,
                            url: '/blg/do_reply_user_suggest/',
                            items: [
                                {xtype: 'hidden', name: 'id', readOnly: true},
                                {fieldLabel: '用户ID', name: 'userid', readOnly: true},
                                {fieldLabel: '回复内容', name: 'question', xtype: 'textarea', height: 200}
                            ],
                            success: function () {
                                alert('回复成功!');
                                me.reload();
                                win.close();
                            }
                        });
                        win.fill(json);
                        win.show();
                    }
                }, {
                    iconCls: 'User',
                    text: '玩家信息',
                    handler: function () {
                        var me = Ext.getCmp(user_suggest_grid);
                        var json = me.getFirstSel();
                        if (!json) return;
                        UINFO(json.userid);
                    }
                }],
                columes: [
                    {header: 'ID', dataIndex: 'id', width: 80},
                    {header: '用户ID', dataIndex: 'userid', width: 120},
                    {header: '问题内容', dataIndex: 'question', width: 200},
                    {header: '回复内容', dataIndex: 'reply', width: 200},
                    {header: '发送时间', dataIndex: 'questime', width: 100},
                    {header: '状态', dataIndex: 'type', width: 100},
                ]
            }
        }, {
            text: '用户金币日志',
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
                    id: "user_money_log_search_form",
                    defaultType: 'textfield',
                    items: [
                        {fieldLabel: '用户ID', name: 'UID', xtype: 'numberfield'},
                          {fieldLabel: 'REASON', name: 'REASON'}
                    ],
                    buttons: [{
                        text: '重置查询条件',
                        handler: function () {
                            var form = Ext.getCmp("user_money_log_search_form").getForm();
                            form.reset();
                        }
                    },
                        {
                            text: '查询',
                            handler: function () {
                                var form = Ext.getCmp("user_money_log_search_form");
                                var obj = form.getForm().getValues();
                                var grid = Ext.getCmp("user_money_log_list_grid");
                                grid.search(obj);
                            }
                        }
                    ]
                },
                    {
                        xtype: 'basegrid',
                        action: '/blg/user_money_log_list/',
                        FW: 600,
                        FH: 425,
                        flex: 4,
                        id: "user_money_log_list_grid",
                        tbar: [],
                        columes: [
                            {header: 'ID', dataIndex: 'pk', width: 120},
                            {header: '用户ID', dataIndex: 'UID', width: 120},
                            {header: '用户名', dataIndex: 'phone', width: 120},
                            {header: '昵称', dataIndex: 'nickname', width: 120},
                            {header: '变更前筹码', dataIndex: 'BEFORE_CHIPS', width: 120},
                            {header: '变更后筹码', dataIndex: 'AFTER_CHIPS', width: 100},
                            {header: '变更金额', dataIndex: 'CHANGE', width: 100},
                            {header: '变更原因', dataIndex: 'REASON'},
                            {header: '变更时间', dataIndex: 'LOG_TIME'},
                            {header: '详情', dataIndex: 'REMARK'}
                        ]
                    }
                ]
            }
        },{
            text: '用户积分日志',
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
                    id: "user_lotto_log_search_form",
                    defaultType: 'textfield',
                    items: [
                        {fieldLabel: '用户ID', name: 'UID', xtype: 'numberfield'},
                          {fieldLabel: 'REASON', name: 'REASON'}
                    ],
                    buttons: [{
                        text: '重置查询条件',
                        handler: function () {
                            var form = Ext.getCmp("user_lotto_log_search_form").getForm();
                            form.reset();
                        }
                    },
                        {
                            text: '查询',
                            handler: function () {
                                var form = Ext.getCmp("user_lotto_log_search_form");
                                var obj = form.getForm().getValues();
                                var grid = Ext.getCmp("user_lotto_log_list_grid");
                                grid.search(obj);
                            }
                        }
                    ]
                }, {
                        xtype: 'basegrid',
                        action: '/blg/user_lotto_log_list/',
                        FW: 600,
                        FH: 425,
                        flex: 4,
                        id: "user_lotto_log_list_grid",
                        tbar: [],
                        columes: [
                            {header: 'ID', dataIndex: 'pk', width: 120},
                            {header: '用户ID', dataIndex: 'UID', width: 120},
                            {header: '用户名', dataIndex: 'phone', width: 120},
                            {header: '昵称', dataIndex: 'nickname', width: 120},
                            {header: '变更前积分', dataIndex: 'BEFORE_LOTTO', width: 120},
                            {header: '变更后积分', dataIndex: 'AFTER_LOTTO', width: 100},
                            {header: '变更积分', dataIndex: 'CHANGE', width: 100},
                            {header: '变更原因', dataIndex: 'REASON'},
                            {header: '变更时间', dataIndex: 'LOG_TIME'}
                        ]
                }]
            }
        },{
            text: '用户排行榜日志',
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
                        xtype: 'basegrid',
                        action: '/blg/user_ranking_log_list/',
                        FW: 600,
                        FH: 425,
                        flex: 4,
                        id: user_grid,
                        tbar: [{
                            text: '用户详细信息',
                            iconCls: 'User',
                            handler: function () {
                                var grid = Ext.getCmp(user_grid);
                                var json = grid.getFirstSel();
                                UINFO(json.usrid);
                            }
                        }],
                        columes: [
                            {header: '时间', dataIndex: 'DT', width: 120},
                            {header: '排名', dataIndex: 'RANK', width: 120},
                            {header: '赢取', dataIndex: 'WIN', width: 120},
                            {header: '用户ID', dataIndex: 'usrid', width: 120},
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
                            {header: '注册设备', dataIndex: 'regdevice'}
                        ]
                    }
                ]
            }
        }]
    });
    main_left_tree.doLayout();

});