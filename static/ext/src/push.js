// Ext.onReady(function () {
//     var main_left_tree = Ext.getCmp('main_left_tree');
//     var push_grid = Ext.id();
//     main_left_tree.getRootNode().appendChild({
//         text: '推送消息',
//         iconCls: 'Bulletright',
//         expanded: true,
//         children: [{
//             text: '消息列表',
//             leaf: true,
//             iconCls: 'Bulletright',
//             view: {
//                 xtype: 'panel',
//                 layout: 'fit',
//                 border: false,
//                 flex: 4,
//                 nopadding: false,
//                 tbar: [{
//                     iconCls: 'Databaseadd',
//                     text: '群发消息',
//                     handler: function () {
//                         var me = Ext.getCmp(push_grid);
//                         var store = me.getStore();
//                         var win = new XG.Control.SimpelPoupForm({
//                             layout: 'form',
//                             title: '添加',
//                             width: 400,
//                             height: 270,
//                             fieldWidth: 250,
//                             url: '/ffqp/console/push_message/?m=push_all',
//                             items: [
//                                 { fieldLabel: 'UID', name: 'uid', value: 0, xtype: 'hidden' },
//                                 { fieldLabel: '消息标题', name: 'title' },
//                                 { fieldLabel: '消息内容', name: 'content', xtype: 'textarea' },
//                                 {
//                                     fieldLabel: '平台', name: 'platform', xtype: 'localcombo',
//                                     data: [
//                                         { name: '全平台', pk: 'ALL' },
//                                         { name: 'IOS', pk: 'IOS' },
//                                         { name: 'ANDROID', pk: 'ANDROID' },
//                                     ]
//                                 }
//                             ],
//                             success: function (data) {
//                                 var json = Ext.decode(data);
//                                 alert('添加成功!')
//                                 store.reload();
//                             }
//                         });
//                         win.show();
//                     }
//                 }],
//                 items: [
//                     {
//                         xtype: 'basegrid',
//                         action: '/ffqp/console/push_message/',
//                         id: push_grid,
//                         FW: 600,
//                         FH: 425,
//                         columes: [
//                             { header: 'UID', dataIndex: 'uid', width: 120, renderer: function (v) { return v == 0 ? "群发" : v } },
//                             { header: '消息标题', dataIndex: 'title', width: 200 },
//                             { header: '消息内容', dataIndex: 'content', width: 200 },
//                             { header: '发送时间', dataIndex: 'send_time', width: 120 },
//                             { header: '平台', dataIndex: 'platform', width: 120 }
//                         ]
//                     }
//                 ]
//             }
//         }]
//     });
//     main_left_tree.doLayout();

// });