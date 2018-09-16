Ext.onReady(function () {
    var main_left_tree = Ext.getCmp('main_left_tree'),
        pay_order_grid = Ext.id(),
        pay_order_search_grid = Ext.id();
	function verify_status(value) {
        return value ? '支付成功' : '等待支付'
    }
    var nopay=true;
    main_left_tree.getRootNode().appendChild({
        text: '订单管理',
        iconCls: 'Bulletright',
        expanded: true,
        children: [{
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
                    id: pay_order_search_grid,
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
                            var form = Ext.getCmp(pay_order_search_grid);
                            var grid = Ext.getCmp(pay_order_grid);
                            var json = form.getForm().getValues();
                            grid.search(json);
                        }
                    }]
                }, {
                    xtype: 'basegrid',
                    action: '/blg/pay_order_list/',
                    flex: 4,
                    id: pay_order_grid,
                    tbar: [{
                        text: '用户详细信息',
                        iconCls: 'User',
                        handler: function () {
                            var grid = Ext.getCmp(pay_order_grid);
                            var json = grid.getFirstSel();
                            if (!json) return;
                            UINFO(json.usrId);
                        }
                    },{
                        text: '切换显示未支付',
                        iconCls: 'Databaserefresh',
                        handler: function () {
                            var form = Ext.getCmp(pay_order_search_grid);
                            var grid = Ext.getCmp(pay_order_grid);
                            var json = form.getForm().getValues();
                            json.nopay=!nopay;
                            grid.search(json);
                        }
                    }],
                    columes: [
                        { header: '玩家ID', dataIndex: 'usrId', width: 120 },

                        { header: '支付金额', dataIndex: 'realdollar', width: 120 },
                        { header: '购买筹码', dataIndex: 'chips', width: 120 },
                        { header: '玩家用户名', dataIndex: 'phone', width: 120 },
                        { header: '玩家昵称', dataIndex: 'nickname', width: 120 },
                        { header: '支付方式', dataIndex: 'pay_way', width: 120 },

                        { header: '订单状态', dataIndex: 'verify', width: 100 , renderer: verify_status},
                        { header: '订单编号', dataIndex: 'orderid', width: 100 },
                        { header: '订单交易号', dataIndex: 'trade_no', width: 100 },
                        { header: '玩家渠道', dataIndex: 'paychannelname', width: 120 },
                        { header: '游戏名称', dataIndex: 'versionname', width: 120 },
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