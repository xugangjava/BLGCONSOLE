Ext.onReady(function () {
    var main_left_tree = Ext.getCmp('main_left_tree'),
        exchange_grid = Ext.id(),
        exchange_approve_grid = Ext.id()
    ;
    main_left_tree.getRootNode().appendChild({
        text: '积分兑换',
        iconCls: 'Bulletright',
        expanded: true,
        children: [{
            text: '兑换审核',
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
                nopadding: true,
                items: [
                    {
                        xtype: 'basegrid',
                        action: '/blg/exchange_approve_list/',
                        FW: 600,
                        FH: 425,
                        flex: 4,
                        id: exchange_approve_grid,
                        tbar: [{
                            iconCls: 'Databaseedit',
                            text: '审核兑换请求',
                            handler: function () {
                                var me = Ext.getCmp(exchange_approve_grid);
                                var json = me.getFirstSel();
                                if (!json) return;
                                var store = me.getStore();
                                var win = new XG.Control.SimpelPoupForm({
                                    layout: 'form',
                                    title: '审核兑换请求',
                                    width: 400,
                                    height: 360,
                                    fieldWidth: 250,
                                    url: '/blg/do_exchange_approve/',
                                    items: [
                                        {fieldLabel: 'ID', name: 'ID', readOnly: true},
                                        {fieldLabel: '兑换物品', name: 'NAME', readOnly: true},
                                        {fieldLabel: '联系人', name: 'LXR', readOnly: true},
                                        {fieldLabel: '地址', name: 'ADDR', readOnly: true},
                                        {fieldLabel: '手机号', name: 'PHONE', readOnly: true},
                                        {
                                            xtype: 'radiogroup', name: 'IS_PASS_GROUP', fieldLabel: '是否通过审核',
                                            columnWidth: 0.7, items: [
                                            {boxLabel: '审核通过', name: 'IS_PASS', inputValue: '1', id: 'IS_PASS'},
                                            {boxLabel: '审核驳回', name: 'IS_PASS', inputValue: '0'}
                                        ]
                                        },
                                        {fieldLabel: '审核备注', name: 'APPROVE_REMARK', xtype: "textarea"}
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
                            text: '用户详细信息',
                            iconCls: 'User',
                            handler: function () {
                                var grid = Ext.getCmp(exchange_approve_grid);
                                var json = grid.getFirstSel();
                                UINFO(json.usrid);
                            }
                        }],
                        columes: [
                            {header: 'ID', dataIndex: 'ID', width: 120},
                            {header: '兑换物品', dataIndex: 'NAME', width: 120},
                            {header: '联系人', dataIndex: 'LXR', width: 200},
                            {header: '地址', dataIndex: 'ADDR', width: 200},
                            {header: '手机号', dataIndex: 'PHONE', width: 120},
                            {header: '兑换方式', dataIndex: 'EX_WAY', width: 120},
                            {header: '消耗积分', dataIndex: 'POINT', width: 120},

                            {header: '玩家ID', dataIndex: 'usrid', width: 100},
                            {header: '玩家昵称', dataIndex: 'nickname', width: 100},
                            {header: '玩家电话', dataIndex: 'phone', width: 100},
                            {header: '玩家积分', dataIndex: 'lotto', width: 100},
                            {header: '玩家充值金额', dataIndex: 'moneyconsume', width: 100},

                            {header: '审核提交时间', dataIndex: 'CREATE_TIME', width: 100}

                        ]
                    }
                ]

            }
        }, {
            text: '兑换日志',
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
                nopadding: true,
                items: [
                    {
                        xtype: 'basegrid',
                        action: '/blg/exchange_approve_log_list/',
                        FW: 600,
                        FH: 425,
                        flex: 4,
                        id: exchange_grid,
                        columes: [
                            {header: 'ID', dataIndex: 'ID', width: 80},
                            {header: '名称', dataIndex: 'NAME', width: 80},
                            {
                                header: '获取类型',
                                dataIndex: 'RTYPE',
                                width: 100,
                                renderer: function (value) {
                                    if (value === 1) return "获取筹码";
                                    else if (value === 2) return "获取实物";
                                    else if (value === 3) return "获取积分";
                                    return "未知类型"
                                }
                            },
                            {header: '获取途径', dataIndex: 'EXTYPE', width: 80},
                            {header: '玩家ID', dataIndex: 'usrid', width: 80},
                            {header: '玩家昵称', dataIndex: 'nickname', width: 80},
                            {header: '玩家电话', dataIndex: 'phone', width: 80},
                            {header: '审核状态', dataIndex: 'STATUS', width: 80},
                            {header: '审核时间', dataIndex: 'APPROVE_TIME', width: 120},
                            {header: '审核备注', dataIndex: 'APPROVE_REMARK', width: 120},
                            {header: '联系人', dataIndex: 'LXR', width: 120},
                            {header: '地址', dataIndex: 'ADDR', width: 120},
                            {header: '手机号', dataIndex: 'PHONE', width: 120},
                            {header: '消耗积分', dataIndex: 'POINT', width: 80},
                            {header: '兑换时间', dataIndex: 'EXTIME', width: 120},
                            {header: '兑换类型', dataIndex: 'EX_WAY', width: 80},
                        ]
                    }
                ]

            }
        }, {
            text: '兑换配置',
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
                nopadding: true,
                items: [
                    {
                        xtype: 'basegrid',
                        action: '/blg/exchange_config_list/',
                        FW: 600,
                        FH: 425,
                        flex: 4,
                        id: exchange_grid,
                        tbar: [{
                            iconCls: 'Databaseadd',
                            text: '添加配置',
                            handler: function () {
                                var me = Ext.getCmp(exchange_grid);
                                var store = me.getStore();
                                var win = new XG.Control.SimpelPoupForm({
                                    layout: 'form',
                                    title: '修改',
                                    width: 400,
                                    height: 400,
                                    fieldWidth: 250,
                                    url: '/blg/exchange_config_list_add/',
                                    items: [
                                        {fieldLabel: '名称', name: 'NAME'},
                                        {fieldLabel: '兑换需要积分', name: 'POINT'},
                                        {fieldLabel: '兑换获得积分', name: 'GET_POINT'},
                                        {fieldLabel: '当前库存', name: 'STOCK'},
                                        {fieldLabel: '获得筹码', name: 'CHIPS'},
                                        {
                                            fieldLabel: '是否广播', name: 'IS_PUSH', xtype: 'localcombo',
                                            data: [
                                                [0, '否'],
                                                [1, '是']
                                            ]
                                        },
                                        {
                                            fieldLabel: '兑换类型', name: 'RTYPE', xtype: 'localcombo',
                                            data: [
                                                [1, '获取筹码'],
                                                [2, '获取实物'],
                                                [3, '获取积分']
                                            ]
                                        },
                                        {fieldLabel: '转盘抽取概率', name: 'GET_RATE'},
                                        {
                                            fieldLabel: '转盘抽取概率', name: 'LUCK_TYPE',
                                            xtype: 'localcombo',
                                            data: [
                                                [1, '积分兑换'],
                                                [2, '积分抽奖'],
                                                [3, '积分兑换&积分抽奖']
                                            ]
                                        }
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
                            text: '修改',
                            handler: function () {
                                var me = Ext.getCmp(exchange_grid);
                                var json = me.getFirstSel();
                                if (!json) return;
                                var store = me.getStore();
                                var win = new XG.Control.SimpelPoupForm({
                                    layout: 'form',
                                    title: '修改',
                                    width: 400,
                                    height: 400,
                                    fieldWidth: 250,
                                    url: '/blg/exchange_config_list_edit/',
                                    items: [
                                        {fieldLabel: 'ID', name: 'ID', readOnly: true},
                                        {fieldLabel: '名称', name: 'NAME'},
                                        {fieldLabel: '兑换需要积分', name: 'POINT'},
                                        {fieldLabel: '兑换获得积分', name: 'GET_POINT'},
                                        {fieldLabel: '当前库存', name: 'STOCK'},
                                        {fieldLabel: '获得筹码', name: 'CHIPS'},
                                        {
                                            fieldLabel: '是否广播', name: 'IS_PUSH', xtype: 'localcombo',
                                            data: [
                                                [0, '否'],
                                                [1, '是']
                                            ]
                                        },
                                        {
                                            fieldLabel: '兑换类型', name: 'RTYPE', xtype: 'localcombo',
                                            data: [
                                                [1, '获取筹码_1'],
                                                [2, '获取实物_2'],
                                                [3, '获取积分_3']
                                            ]
                                        },
                                        {fieldLabel: '转盘抽取概率', name: 'GET_RATE'},
                                        {
                                            fieldLabel: '转盘抽取概率', name: 'LUCK_TYPE',
                                            xtype: 'localcombo',
                                            data: [
                                                [1, '积分兑换'],
                                                [2, '积分抽奖'],
                                                [3, '积分兑换&积分抽奖']
                                            ]
                                        }
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
                            iconCls: 'Databaseedit',
                            text: '删除配置',
                            handler: function () {
                                var me = Ext.getCmp(exchange_grid);
                                var json = me.getFirstSel();
                                if (!json) return;
                                me.deleteRow("/blg/exchange_config_list_del/");
                                me.getStore().reload();
                            }
                        }],
                        columes: [
                            {header: 'ID', dataIndex: 'ID', width: 120},
                            {header: '名称', dataIndex: 'NAME', width: 120},
                            {header: '兑换需要积分', dataIndex: 'POINT', width: 100},
                            {header: '兑换获得积分', dataIndex: 'GET_POINT', width: 100},
                            {header: '当前库存', dataIndex: 'STOCK', width: 120},
                            {header: '获得筹码', dataIndex: 'CHIPS', width: 100},
                            {header: '转盘抽取概率', dataIndex: 'GET_RATE', width: 100},
                            {
                                header: '是否广播', dataIndex: 'IS_PUSH', width: 100,
                                renderer: function (value) {
                                    if (value === 1) return "是";
                                    else return "否";
                                }
                            },
                            {
                                header: '获取类型',
                                dataIndex: 'RTYPE',
                                width: 100,
                                renderer: function (value) {
                                    if (value === 1) return "获取筹码";
                                    else if (value === 2) return "获取实物";
                                    else if (value === 3) return "获取积分";
                                    return "未知类型"
                                }
                            },
                            {
                                header: '获取途径',
                                dataIndex: 'LUCK_TYPE',
                                width: 100,
                                renderer: function (value) {
                                    if (value === 1) return "积分兑换";
                                    else if (value === 2) return "积分抽奖";
                                    else if (value === 3) return "积分兑换&积分抽奖";
                                    return "未知类型"
                                }
                            }
                        ]
                    }
                ]

            }
        }]
    });
    main_left_tree.doLayout();

});