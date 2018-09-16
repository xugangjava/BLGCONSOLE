/**
 * Created by xugang on 14-9-29.
 */

Ext.apply(Ext.form.VTypes, {
    daterange : function(val, field) {
        var date = field.parseDate(val);
        if(!date){
            return false;
        }
        if (field.startDateField) {
            var start = Ext.getCmp(field.startDateField);
            if (!start.maxValue || (date.getTime() != start.maxValue.getTime())) {
                start.setMaxValue(date);
                start.validate();
            }
        }
        else if (field.endDateField) {
            var end = Ext.getCmp(field.endDateField);
            if (!end.minValue || (date.getTime() != end.minValue.getTime())) {
                end.setMinValue(date);
                end.validate();
            }
        }
        return true;
    },
    daterange_start:function(val,field){
        var items=field.ownerCt.items.items;
        var date = field.parseDate(val);
        if(!date){
            return false;
        }
        var myIdx=-1;
        for (var i = items.length - 1; i >= 0; i--) {
            if(items[i].id==field.id){
                myIdx=i;
                break;
            }
        };
        if(-1!=myIdx){
            var end=items[myIdx+1];
            if (!end.minValue || (date.getTime() != end.minValue.getTime())) {
                end.setMinValue(date);
                end.validate();
            }
        }
        return true;
    },
    daterange_startText:'开始时间必须小于结束时间',
    daterange_end:function(val,field){
        var items=field.ownerCt.items.items;
        var date = field.parseDate(val);
        if(!date){
            return false;
        }
        var myIdx=-1;
        for (var i = items.length - 1; i >= 0; i--) {
            if(items[i].id==field.id){
                myIdx=i;
                break;
            }
        };
        if(-1!=myIdx){
            var start=items[myIdx-1];
            if (!start.maxValue || (date.getTime() != start.maxValue.getTime())) {
                start.setMaxValue(date);
                start.validate();
            }
        }
        return true;
    },
    daterange_endText:'结束时间必须大于开始时间',
    password : function(val, field) {
        // if (field.initialPassField) {
        //     var pwd = Ext.getCmp(field.initialPassField);
        //     return (val == pwd.getValue());
        // }
        return true;
    },
    passwordText : '两次输入密码不一致',
    percent:function(value,field){
        try{
            var i=parseInt(value);
            return i>0&&i<100;
        }catch(err){
            return false;
        }
    },
    percentText:'必须为0-100的数字',
    username:function(val,field){
        if(field.lastname==val)return true;
        var result;   
        Ext.Ajax.request({  
            url:'/user/name/',
            async:false,
            params:{
                name:val
            },
            method:'post',  
            success:function(response,options){  
                var res = Ext.util.JSON.decode(response.responseText);  
                if(res.msg=='OK'){
                    result=true;
                    field.lastname=val;
                    field.clearInvalid();
                }else{
                    result=false;
                }
            }
        });
        return result;
    },
    usernameText:'用户名已经存在',
    positive:function(val,field){
        try  
        {  
            if(/^[1-9][\d]*$/.test(val))  
                return true;  
            return false;  
        }  
        catch(e)  
        {  
            return false;  
        }  
    },
    positiveText:'请输入正确的正整数！',
    natural:function(val,field){
        try  
        {  
            if(/^[\d]*$/.test(val))  
                return true;  
            return false;  
        }  
        catch(e)  
        {  
            return false;  
        }  
    },
    naturalText:'请输入自然数！',
    future_date:function(val,field){
        try  
        {   
            return field.getValue()>new Date()
        }  
        catch(e)  
        {  
            return false;  
        }  
    },
    future_dateText:'必须大于当前时间！',
    
    phone:function(val,field){
        if(!(/\d{3}-\d{8}|\d{4}-\d{7}/.test(val))){ 
            return false; 
        } 
        return true;
    },
    phoneText:'请填写正确的电话号码，例如(021-87888822)',

    mobile:function(val,field){
        if(!(/^1[3|4|5|8][0-9]\d{4,8}$/.test(val))){ 
            return false; 
        } 
        return true;
    },
    mobileText:'不是完整的11位手机号或者正确的手机号前七位',
    blank_no:function(val,field){
        var regex = /^\d{19}$/;
        if (regex.test(val)) {
            return true;
        }
        return false;
    },
    blank_noText:'不是正确的银行卡格式'
});

