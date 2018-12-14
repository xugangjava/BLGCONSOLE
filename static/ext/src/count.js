Ext.onReady(function () {


    var pay_store = new Ext.data.JsonStore({
        fields: ['TOTAL_PAY', 'LOG_TIME'],
        root: 'items',
        autoLoad: true,
        url: '/blg/game_count_list/?chart=1'
    });

    var app_analysis_store = new Ext.data.JsonStore({
        fields: ['LOG_TIME', 'LOGIN_COUNT', 'REG_COUNT', 'ACTVIE_COUNT',
            'TOTAL_PAY', 'PAY_COUNT', 'D2_LEAVE_RATE', 'PAY_RATE',
            'D2_LEAVE_RATE_V', 'PAY_RATE_V',
            'ARPU', 'ARPPU'],
        root: 'items',
        autoLoad: true,
        url: '/blg/game_count_list/?chart=1'
    });

    var app_analysis_channel_store= new Ext.data.JsonStore({
        fields: ['LOG_TIME', 'LOGIN_COUNT', 'REG_COUNT', 'ACTVIE_COUNT',
            'TOTAL_PAY', 'PAY_COUNT', 'D2_LEAVE_RATE', 'PAY_RATE',
            'D2_LEAVE_RATE_V', 'PAY_RATE_V','CHANNEL',
            'ARPU', 'ARPPU'],
        root: 'items',
        autoLoad: true,
        url: '/blg/game_count_channel_list/?chart=1'
    });

    var game_chips_count = new Ext.data.JsonStore({
        fields: ['LOG_TIME', 'CHIPS', 'ID'],
        root: 'items',
        autoLoad: true,
        url: '/blg/game_chips_count_list/?chart=1'
    });



    var game_chips_send_count = new Ext.data.JsonStore({
        fields: ['TIM', 'COUNTS', 'ID'],
        root: 'items',
        autoLoad: true,
        url: '/blg/gm_send_chips_count/?chart=1'
    });


    var gm_win_rate = new Ext.data.JsonStore({
        fields: ['TM', 'RATE', 'ID'],
        root: 'items',
        autoLoad: true,
        url: '/blg/game_win_chart/?chart=1'
    });

    var pay_log_grid = Ext.id(),
        active_log_search_form = Ext.id(),
        robot_play_grid = Ext.id(),
        recharge_log_search_form = Ext.id(),
        active_log_grid = Ext.id(),
        app_analysis_search_form = Ext.id(),
        app_cut_grid = Ext.id();

    var main_left_tree = Ext.getCmp('main_left_tree');
    main_left_tree.getRootNode().appendChild({
        text: '游戏统计',
        iconCls: 'Bulletright',
        expanded: true,
        children: [{
            text: '游戏统计',
            leaf: true,
            iconCls: 'Bulletright',
            view: {
                xtype: 'panel',
                layout: {
                    type: 'vbox',
                    padding: '1',
                    align: 'stretch'
                },
                border: false,
                flex: 4,
                nopadding: false,
                items: [{
                    xtype: 'form',
                    flex: 2,
                    id: app_analysis_search_form,
                    padding: 10,
                    items: [
                        {fieldLabel: '开始时间', xtype: 'datefield', name: 'start_time', format: 'Y-m-d'},
                        {fieldLabel: '结束时间', xtype: 'datefield', name: 'end_time', format: 'Y-m-d'}
                    ],
                    buttons: [{
                        iconCls: 'Databasedelete',
                        text: '清空条件',
                        handler: function () {
                            var form = Ext.getCmp(app_analysis_search_form);
                            form.getForm().reset();
                        }
                    }, {
                        iconCls: 'Databaseedit',
                        text: '查询',
                        handler: function () {
                            var form = Ext.getCmp(app_analysis_search_form);
                            var json = form.getForm().getValues();
                            var grid = Ext.getCmp(active_log_grid);
                            app_analysis_store.load({
                                params: json
                            });
                            grid.search(json);
                        }
                    }]
                }, {
                    xtype: 'linechart',
                    store: app_analysis_store,
                    url: '/static/ext/resources/charts.swf',
                    xField: 'LOG_TIME',
                    flex: 3,
                    series: [
                        {type: 'line', displayName: '留存率', yField: 'D2_LEAVE_RATE_V', style: {color: 716699}},
                        {type: 'line', displayName: '付费率', yField: 'PAY_RATE_V', style: {color: 0x2BD591}}
                    ],
                    extraStyle: {
                        legend: {
                            display: 'bottom',
                            padding: 5,
                            font: {
                                family: 'Tahoma',
                                size: 13
                            }
                        }
                    },
                    listeners: {
                        itemclick: function (o) {
                            var rec = store.getAt(o.index);
                            Ext.example.msg('详细信息', '{0}.', rec.get('name'));
                        }
                    }
                },
                    {
                        xtype: 'basegrid',
                        action: '/blg/game_count_list/',
                        flex: 4,
                        id: active_log_grid,
                        nopadding: false,
                        columes: [
                            {header: '日期', dataIndex: 'LOG_TIME', width: 200},
                            {header: '登录用户', dataIndex: 'LOGIN_COUNT', width: 200},
                            {header: '注册用户', dataIndex: 'REG_COUNT', width: 200},
                            {header: '有效活跃', dataIndex: 'ACTVIE_COUNT', width: 200},
                            {header: '付费人数', dataIndex: 'PAY_COUNT', width: 200},
                            {header: '总付费', dataIndex: 'TOTAL_PAY', width: 200},
                            {header: '两日留存', dataIndex: 'D2_LEAVE_RATE', width: 200},
                            {header: '付费率', dataIndex: 'PAY_RATE', width: 200},
                            {header: 'Arpu', dataIndex: 'ARPU', width: 200},
                            {header: 'Arppu', dataIndex: 'ARPPU', width: 200},
                            {header: '免费筹码领取', dataIndex: 'FREE_GET', width: 200}
                        ]
                    }
                ]
            }
        },{
            text: '游戏统计_渠道',
            leaf: true,
            iconCls: 'Bulletright',
            view: {
                xtype: 'panel',
                layout: {
                    type: 'vbox',
                    padding: '1',
                    align: 'stretch'
                },
                border: false,
                flex: 4,
                nopadding: false,
                items: [{
                    xtype: 'form',
                    flex: 2,
                    id: 'app_analysis_channel_search_form',
                    padding: 10,
                    items: [
                        {fieldLabel: '开始时间', xtype: 'datefield', name: 'start_time', format: 'Y-m-d'},
                        {fieldLabel: '结束时间', xtype: 'datefield', name: 'end_time', format: 'Y-m-d'},
                        {fieldLabel: '渠道',xtype: 'remotecombo', name: 'channel_id', url: '/blg/combo_channel/'}
                    ],
                    buttons: [{
                        iconCls: 'Databasedelete',
                        text: '清空条件',
                        handler: function () {
                            var form = Ext.getCmp('app_analysis_channel_search_form');
                            form.getForm().reset();
                        }
                    }, {
                        iconCls: 'Databaseedit',
                        text: '查询',
                        handler: function () {
                            var form = Ext.getCmp('app_analysis_channel_search_form');
                            var json = form.getForm().getValues();
                            var grid = Ext.getCmp('active_channel_log_grid');
                            app_analysis_channel_store.load({
                                params: json
                            });
                            grid.search(json);
                        }
                    }]
                }, {
                    xtype: 'linechart',
                    store: app_analysis_channel_store,
                    url: '/static/ext/resources/charts.swf',
                    xField: 'LOG_TIME',
                    flex: 3,
                    series: [
                        {type: 'line', displayName: '留存率', yField: 'D2_LEAVE_RATE_V', style: {color: 716699}},
                        {type: 'line', displayName: '付费率', yField: 'PAY_RATE_V', style: {color: 0x2BD591}}
                    ],
                    extraStyle: {
                        legend: {
                            display: 'bottom',
                            padding: 5,
                            font: {
                                family: 'Tahoma',
                                size: 13
                            }
                        }
                    },
                    listeners: {
                        itemclick: function (o) {
                            var rec = store.getAt(o.index);
                            Ext.example.msg('详细信息', '{0}.', rec.get('name'));
                        }
                    }
                }, {
                        xtype: 'basegrid',
                        action: '/blg/game_count_channel_list/',
                        flex: 4,
                        id: 'active_channel_log_grid',
                        nopadding: false,
                        columes: [
                            {header: '渠道', dataIndex: 'CHANNEL', width: 200},
                            {header: '日期', dataIndex: 'LOG_TIME', width: 200},
                            {header: '登录用户', dataIndex: 'LOGIN_COUNT', width: 200},
                            {header: '注册用户', dataIndex: 'REG_COUNT', width: 200},
                            {header: '有效活跃', dataIndex: 'ACTVIE_COUNT', width: 200},
                            {header: '付费人数', dataIndex: 'PAY_COUNT', width: 200},
                            {header: '总付费', dataIndex: 'TOTAL_PAY', width: 200},
                            {header: '两日留存', dataIndex: 'D2_LEAVE_RATE', width: 200},
                            {header: '付费率', dataIndex: 'PAY_RATE', width: 200},
                            {header: 'Arpu', dataIndex: 'ARPU', width: 200},
                            {header: 'Arppu', dataIndex: 'ARPPU', width: 200},
                        ]
                    }
                ]
            }
        }, {
            text: '充值统计',
            leaf: true,
            iconCls: 'Bulletright',
            view: {
                xtype: 'panel',
                layout: {
                    type: 'vbox',
                    padding: '1',
                    align: 'stretch'
                },
                border: false,
                flex: 8,
                tbar: [{
                    text: '刷新',
                    iconCls: 'Databaserefresh',
                    handler: function () {
                        pay_store.reload();
                    }
                }],
                items: [{
                    xtype: 'form',
                    flex: 3,
                    padding: 10,
                    id: recharge_log_search_form,
                    items: [
                        {fieldLabel: '开始时间', xtype: 'datefield', name: 'start_time', format: 'Y-m-d'},
                        {fieldLabel: '结束时间', xtype: 'datefield', name: 'end_time', format: 'Y-m-d'}
                    ],
                    buttons: [{
                        iconCls: 'Databaseedit',
                        text: '查询',
                        handler: function () {
                            var form = Ext.getCmp(recharge_log_search_form);
                            var json = form.getForm().getValues();
                            var grid = Ext.getCmp(pay_log_grid);
                            pay_store.load({
                                params: json
                            });
                            grid.search(json);
                        }
                    }]
                }, {
                    xtype: 'linechart',
                    store: app_analysis_store,
                    url: '/static/ext/resources/charts.swf',
                    xField: 'LOG_TIME',
                    flex: 3,
                    series: [
                        {type: 'line', displayName: 'Arpu', yField: 'ARPU', style: {color: 0xF79709}},
                        {type: 'line', displayName: 'Arppu', yField: 'ARPPU', style: {color: 0x66FC00}}
                    ],
                    extraStyle: {
                        legend: {
                            display: 'bottom',
                            padding: 5,
                            font: {
                                family: 'Tahoma',
                                size: 13
                            }
                        }
                    },
                    listeners: {
                        itemclick: function (o) {
                            var rec = store.getAt(o.index);
                            Ext.example.msg('详细信息', '{0}.', rec.get('name'));
                        }
                    }
                }, {
                    xtype: 'basegrid',
                    action: '/blg/game_count_list/',
                    flex: 4,
                    id: pay_log_grid,
                    nopadding: false,
                    columes: [
                        {header: '日期', dataIndex: 'LOG_TIME', width: 200},
                        {header: '付费人数', dataIndex: 'PAY_COUNT', width: 200},
                        {header: '总付费', dataIndex: 'TOTAL_PAY', width: 200},
                        {header: '登录用户', dataIndex: 'LOGIN_COUNT', width: 200},
                        {header: '注册用户', dataIndex: 'REG_COUNT', width: 200},
                        {header: '有效活跃', dataIndex: 'ACTVIE_COUNT', width: 200},
                        {header: '两日留存', dataIndex: 'D2_LEAVE_RATE', width: 200},
                        {header: '付费率', dataIndex: 'PAY_RATE', width: 200},
                        {header: 'Arpu', dataIndex: 'ARPU', width: 200},
                        {header: 'Arppu', dataIndex: 'ARPPU', width: 200}
                    ]
                }
                ]
            }
        }, {
            text: '游戏输赢',
            leaf: true,
            iconCls: 'Bulletright',
            view: {
                xtype: 'basegrid',
                action: '/blg/game_win_count_list/',
                flex: 4,
                id: active_log_grid,
                nopadding: false,
                columes: [
                    {header: 'ID', dataIndex: 'ID', width: 120},
                    {header: '名称', dataIndex: 'CNAME', width: 120},
                    {header: '下注筹码', dataIndex: 'CHIP_IN', width: 120},
                    {header: '赢取筹码', dataIndex: 'CHIP_WIN', width: 120},
                    {header: '积分产出', dataIndex: 'TOTAL_LOTTE', width: 120},
                    {
                        header: '赢取期望',
                        dataIndex: 'CHIP_WIN',
                        width: 120,
                        renderer: function (value, cellmeta, record, rowIndex, columnIndex, store) {
                            var data = record.data, CHIP_WIN = data['CHIP_WIN'], CHIP_IN = data['CHIP_IN'];
                            if (!CHIP_IN) {
                                return 0;
                            }
                            var r = CHIP_WIN * 1.0 / CHIP_IN;
                            return r.toFixed(2);
                        }
                    },
                    {header: '最后记录时间', dataIndex: 'LOG_TIME', width: 120},
                    {header: '总记录次数', dataIndex: 'TOTAL_LOG_TIMES', width: 120},
                    {header: '在线人数', dataIndex: 'ONLINE_COUNT', width: 120}
                ]
            }
        }, {
            text: '游戏输赢概率',
            leaf: true,
            iconCls: 'Bulletright',
            view: {
                xtype: 'linechart',
                store: gm_win_rate,
                url: '/static/ext/resources/charts.swf',
                xField: 'TM',
                series: [
                    {type: 'line', displayName: 'RATE', yField: 'RATE', style: {color: 0xF79709}}
                ],
                extraStyle: {
                    legend: {
                        display: 'bottom',
                        padding: 5,
                        font: {
                            family: 'Tahoma',
                            size: 13
                        }
                    }
                },
                listeners: {
                    itemclick: function (o) {
                        var rec = store.getAt(o.index);
                        Ext.example.msg('详细信息', '{0}.', rec.get('name'));
                    }
                }
            }
        }, {
            text: '筹码发放统计',
            leaf: true,
            iconCls: 'Bulletright',
            view: {
                xtype: 'panel',
                layout: {
                    type: 'vbox',
                    padding: '1',
                    align: 'stretch'
                },
                border: false,
                flex: 8,
                tbar: [{
                    text: '刷新',
                    iconCls: 'Databaserefresh',
                    handler: function () {
                        game_chips_send_count.reload();
                        var grid = Ext.getCmp('chips_send_grid');
                        grid.reload();
                    }
                }],
                items: [{
                    xtype: 'form',
                    flex: 3,
                    padding: 10,
                    id: 'chips_send_grid_form',
                    items: [
                        {fieldLabel: '开始时间', xtype: 'datefield', name: 'start_time', format: 'Y-m-d'},
                        {fieldLabel: '结束时间', xtype: 'datefield', name: 'end_time', format: 'Y-m-d'},
                    ],
                    buttons: [{
                        iconCls: 'Databaseedit',
                        text: '查询',
                        handler: function () {
                            var form = Ext.getCmp('chips_send_grid_form');
                            var json = form.getForm().getValues();
                            var grid = Ext.getCmp('chips_send_grid');
                            game_chips_send_count.load({
                                params: json
                            });
                            grid.search(json);
                        }
                    }]
                }, {
                    xtype: 'linechart',
                    store: game_chips_send_count,
                    url: '/static/ext/resources/charts.swf',
                    xField: 'TIM',
                    flex: 3,
                    series: [
                        {type: 'line', displayName: '筹码总发放', yField: 'COUNTS', style: {color: 0xF79709}}
                    ],
                    extraStyle: {
                        legend: {
                            display: 'bottom',
                            padding: 5,
                            font: {
                                family: 'Tahoma',
                                size: 13
                            }
                        }
                    },
                    listeners: {
                        itemclick: function (o) {
                            var rec = store.getAt(o.index);
                            Ext.example.msg('详细信息', '{0}.', rec.get('name'));
                        }
                    }
                }, {
                    xtype: 'basegrid',
                    action: '/blg/gm_send_chips_count/',
                    flex: 4,
                    id: 'chips_send_grid',
                    pagesize: 12,
                    nopadding: false,
                    columes: [
                        {header: '日期', dataIndex: 'TIM', width: 200},
                        {header: '筹码', dataIndex: 'COUNTS', width: 200},
                        {header: '原因', dataIndex: 'REASON', width: 200},
                        {header: '统计人数', dataIndex: 'USR_COUNT', width: 200},
                        {
                            header: '平均',
                            dataIndex: 'USR_COUNT',
                            width: 120,
                            renderer: function (value, cellmeta, record, rowIndex, columnIndex, store) {
                                var data = record.data, USR_COUNT = data['USR_COUNT'], COUNTS = data['COUNTS'];
                                if (!USR_COUNT) {
                                    return 0;
                                }
                                var r = COUNTS * 1.0 / USR_COUNT;
                                return r.toFixed(2);
                            }
                        }
                    ]
                }]
            }
        }, {
            text: '玩家筹码统计',
            leaf: true,
            iconCls: 'Bulletright',
            view: {
                xtype: 'panel',
                layout: {
                    type: 'vbox',
                    padding: '1',
                    align: 'stretch'
                },
                border: false,
                flex: 8,
                tbar: [{
                    text: '刷新',
                    iconCls: 'Databaserefresh',
                    handler: function () {
                        game_chips_count.reload();
                    }
                }],
                items: [{
                    xtype: 'form',
                    flex: 3,
                    padding: 10,
                    id: "game_chips_count_from",
                    items: [
                        {fieldLabel: '开始时间', xtype: 'datefield', name: 'start_time', format: 'Y-m-d'},
                        {fieldLabel: '结束时间', xtype: 'datefield', name: 'end_time', format: 'Y-m-d'}
                    ],
                    buttons: [{
                        iconCls: 'Databaseedit',
                        text: '查询',
                        handler: function () {
                            var form = Ext.getCmp("game_chips_count_from");
                            var json = form.getForm().getValues();
                            var grid = Ext.getCmp("game_chips_count_grid");
                            game_chips_count.load({
                                params: json
                            });
                            grid.search(json);
                        }
                    }]
                }, {
                    xtype: 'linechart',
                    store: game_chips_count,
                    url: '/static/ext/resources/charts.swf',
                    xField: 'LOG_TIME',
                    flex: 3,
                    series: [
                        {type: 'line', displayName: 'CHIPS', yField: 'CHIPS', style: {color: 0xF79709}}
                    ],
                    extraStyle: {
                        legend: {
                            display: 'bottom',
                            padding: 5,
                            font: {
                                family: 'Tahoma',
                                size: 13
                            }
                        }
                    },
                    listeners: {
                        itemclick: function (o) {
                            var rec = store.getAt(o.index);
                            Ext.example.msg('详细信息', '{0}.', rec.get('name'));
                        }
                    }
                }, {
                    xtype: 'basegrid',
                    action: '/blg/game_chips_count_list/',
                    flex: 4,
                    id: "game_chips_count_grid",
                    nopadding: false,
                    columes: [
                        {header: 'ID', dataIndex: 'ID', width: 200},
                        {header: '玩家筹码总和', dataIndex: 'CHIPS', width: 200},
                        {header: '日期', dataIndex: 'LOG_TIME', width: 200},
                        {header: 'COUNTUSER', dataIndex: 'COUNTUSER', width: 200}
                    ]
                }]
            }
        }, {
            text: '玩家游戏统计',
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
                    id: 'game_play_info_serach_from',
                    defaultType: 'textfield',
                    items: [
                        {fieldLabel: '用户ID', name: 'UserID', xtype: 'numberfield'},
                        {fieldLabel: '用户名', name: 'UserName'},
                        {fieldLabel: '昵称', name: 'NickName'},
                        {fieldLabel: '渠道', xtype: 'remotecombo', name: 'Channel', url: '/blg/combo_channel/'}
                    ],
                    buttons: [{
                        text: '重置查询条件',
                        handler: function () {
                            var form = Ext.getCmp('game_play_info_serach_from').getForm();
                            form.reset();
                        }
                    },
                        {
                            text: '查询',
                            handler: function () {
                                var form = Ext.getCmp('game_play_info_serach_from');
                                var obj = form.getForm().getValues();
                                var grid = Ext.getCmp('game_play_info');
                                grid.search(obj);
                            }
                        }
                    ]
                }, {
                    xtype: 'basegrid',
                    action: '/blg/game_play_info/',
                    FW: 600,
                    FH: 425,
                    flex: 4,
                    id: 'game_play_info',
                    tbar: [],
                    columes: [
                        {header: '用户ID', dataIndex: 'pk', width: 120},
                        {header: '用户名', dataIndex: 'phone', width: 120},
                        {header: '昵称', dataIndex: 'nickname', width: 120},
                        {header: '金钱', dataIndex: 'chips', width: 120},
                        {header: '积分', dataIndex: 'lotto', width: 100},
                        {header: '充值金额', dataIndex: 'moneyconsume', width: 100},
                        {header: '上次登录时间', dataIndex: 'lastLogintm'},
                        {header: '连续登陆天数', dataIndex: 'ContinueLogin'},
                        {header: 'LEVEL', dataIndex: 'level'},
                        {header: 'EXP', dataIndex: 'exp'},
                        {header: '运气值', dataIndex: 'luck'},
                        {header: '注册IP', dataIndex: 'regip'},
                        {header: '注册时间', dataIndex: 'regtime'},
                        {header: '注册渠道', dataIndex: 'versionid'},
                        {header: '注册设备', dataIndex: 'regdevice'},

                        {header: '百家乐一把最大赢取筹码（净利）', dataIndex: 'BiggestWinInBac'},
                        {header: '百家乐总的下注次数', dataIndex: 'BetTimesInBac'},
                        {header: '百家乐总的咪牌次数', dataIndex: 'PeekTimesInBac'},
                        {header: '百家乐押中对子的次数', dataIndex: 'WinPairsTimesInBac'},
                        {header: 'SLOTS总的spin次数（包含奖励的免费次数）', dataIndex: 'SpinTimesInSlot'},
                        {header: 'SLOTS里bigwin的次数', dataIndex: 'BigWinTimesInSlot'},
                        {header: 'SLOTS里megawin的次数', dataIndex: 'MegaWinTimesInSlot'},

                        {header: '水果机次数', dataIndex: 'SlotoFruit'},
                        {header: '野蛮人次数', dataIndex: 'SlotoYsr'},
                        {header: '金瓶梅次数', dataIndex: 'SlotoJpm'},
                        {header: '猜大小次数', dataIndex: 'SlotoFruitGuess'},
                        {header: '最大积分', dataIndex: 'MaxLotto'},

                        {header: 'videopoker的游戏总次数', dataIndex: 'PlayTimesInVP'},
                        {header: 'videopoker获得四条及以上的次数', dataIndex: 'FourAboveTimesInVP'},
                        {header: 'videopoker猜大小七连中的次数', dataIndex: 'SevenTimesWinInVP'},
                        {header: 'videopoker猜大小次数', dataIndex: 'VPGuess'},
                        {header: '21点play次数', dataIndex: 'bljcount'},
                        {header: 'blackjack次数', dataIndex: 'blackjackcount'},
                        {header: '21点次数', dataIndex: '21count'},
                        {header: '每日赢取最大筹码数(净利)', dataIndex: 'BiggestWinInDay'},
                        {header: '曾经拥有的最大筹码数', dataIndex: 'TheBestRicher'},
                        {header: '今日赢取总筹码', dataIndex: 'winInToday'},

                    ]
                }]

            }


        }


        ]
    });
    main_left_tree.doLayout();

});