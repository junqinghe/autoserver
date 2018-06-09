
(function(jq) {
    String.prototype.format=function (args){
    return this.replace(/\{(\w+)\}/g,function (s,i) {
// {#            这里的's'是整个//替换的部分，包括中括号，'i'是剔除中括号后的内容}#}
        return args[i];
// {#            把值返回给//里面#}
    });
};

    var GLOBAL_DICT={};
    function initial(url) {
        $.ajax({
                url: url,
                type: 'GET',
                data: {},
                dataType: 'json',
                success: function (arg) {
                    $.each(arg.global_dict,function (k,v) {
                        GLOBAL_DICT[k]=v
                    });

                    InitTableHeader(arg.table_config);
                    IniTableBody(arg.table_config, arg.server_list)
                }
            }
        );
    }

    function InitTableHeader(tablelist) {
        var tr=document.createElement('tr');
        $.each(tablelist,function (k,v) {
            if (v.display){
                var th=document.createElement('th');
                th.innerHTML=v.title;
                $(tr).append(th)
            }
        });
        $('#table_head').append(tr)

}

    function IniTableBody(tablelist,serverlist) {
    $.each(serverlist,function (k,v) {
        var tr=document.createElement('tr');
        tr.setAttribute('nid',v.id);
        $.each(tablelist,function (kk,vv) {

            //是否显示
            if(vv.display){
                var td=document.createElement('td');
// {#                if(vv.q){#}
// {#                    td.innerHTML=v[vv.q];#}
// {#                }else{#}
                //在td标签中添加内容
                var newkwargs={};
                $.each(vv.text.kwargs,function (kkk,vvv) {
                    if(vvv.substring(0,2)=='@@'){
                        var global_dict_key=vvv.substring(2,vvv.length);
                        var nid=v[vv.q];
                        $.each(GLOBAL_DICT[global_dict_key],function (g,w){
                            if(w[0]==nid){
                                newkwargs[kkk]=w[1]
                            }
                        })
                    }
                    else if(vvv[0] == "@"){
                        var av=vvv.substring(1,vvv.length);
                        newkwargs[kkk]=v[av];
                    }

                });
                var newText=vv.text.tpl.format(newkwargs);
                td.innerHTML=newText;
// {#                }#}
                //在td标签中添加属性
                $.each(vv.attrs,function(atk,atv){
                    if(atv[0]=="@"){
                        td.setAttribute(atk,v[atv.substring(1,atv.length)])
                    }else{
                        td.setAttribute(atk,atv);
                    }
                });
            tr.append(td)
            }
        });
        $('#table_body').append(tr)
    })
}

    function IntoEdit($tr) {
        $tr.find('td[editable="true"]').each(function () {
        //    $(this) 每一个td
            var $edit_type=$(this).attr('edit_type');
            if( $edit_type=='select'){
                //生成下拉框:找到数据源
                var device_type_choice=GLOBAL_DICT[$(this).attr('global_key')];
                var selectTag=document.createElement('select');
                var orihgin_id=$(this).attr('origin');
                $.each(device_type_choice,function (dk,dv) {
                    //显示默认值
                    var option=document.createElement('option');
                    $(option).text(dv[1]);
                    $(option).val(dv[0]);
                    if(orihgin_id==dv[0]){
                        //默认选中的值
                        $(option).prop('selected',true)
                    }
                    $(selectTag).append(option)
                });
                $(this).html(selectTag)

            }else {
                var v1=$(this).text();
                var inp=document.createElement('input');
                $(inp).val(v1);
                $(this).html(inp)
            }
        })
    }

    function OutEdit($tr) {
         $tr.find('td[editable="true"]').each(function () {
        //    $(this) 每一个td
             var ths=$(this);
             var $edit_type=$(this).attr('edit_type');
             if($edit_type=='select'){
                 // $.each($(this).find('option'),function (h,hw) {
                 //     var zhi=$(hw).prop('select');
                 //     if($(zhi)){
                 //         var optval=$(hw).text();
                 //         ths.html(optval);
                 //         console.log(optval)
                 //     }else {
                 //         console.log('buxing')
                 //     }
                 // });    //竟然不行，MD
               var option=$(this).find('select')[0].selectedOptions;   //找到选中的option
               $(this).attr('new-origin',$(option).val());
               $(this).html($(option).text())
             }else {
                 var inpVal=$(this).find('input').val();
                 $(this).html(inpVal)
             }
         })
    }

    jq.extend({
        nb_list:function (url) {
            initial(url);

            //给checkbox绑定事件
            $('#table_body').on('click',':checkbox',function () {
                 if ($('#INoutEdit').hasClass('btn-warning')){
                    var $tr=$(this).parent().parent();
                    if($(this).prop('checked')){
                    IntoEdit($tr)
                    }else {
                    OutEdit($tr)
                    }
                 }else {
                     $(this).prop('checked',true)
                 }

    });

            //给按钮绑定事件
            $('#checkall').click(function () {
                if ($('#INoutEdit').hasClass('btn-warning')){
                    $('#table_body').find(':checkbox').each(function () {
                    if(!$(this).prop('checked')){
                        $(this).prop('checked',true);
                        var $tr=$(this).parent().parent();
                        IntoEdit($tr)
                }
            })
                }else {
                    $('#table_body').find(':checkbox').prop('checked',true)
                }
            });

            $('#checkareverse').click(function () {
                if ($('#INoutEdit').hasClass('btn-warning')){
                   $('#table_body').find(':checkbox').each(function () {
                    var $tr=$(this).parent().parent();
                    if(!$(this).prop('checked')){
                        $(this).prop('checked',true);
                        IntoEdit($tr)
                    }else {
                         $(this).prop('checked',false);
                         OutEdit($tr)
                     }
                 })
                }else {
                    $('#table_body').find(':checkbox').each(function () {
                    var $tr=$(this).parent().parent();
                    if(!$(this).prop('checked')){
                        $(this).prop('checked',true);
                    }else {
                         $(this).prop('checked',false);
                     }
                 })

                }

            });

            $('#checkcancle').click(function () {
               if ($('#INoutEdit').hasClass('btn-warning')){
                  $('#table_body').find(':checkbox').each(function () {
                    if($(this).prop('checked')){
                        $(this).prop('checked',false);
                        var $tr=$(this).parent().parent();
                        OutEdit($tr)
                    }
                })
                 }else {
                   $('#table_body').find(':checkbox').prop('checked',false);
               }
            });

            $('#INoutEdit').click(function () {
                if ($(this).hasClass('btn-warning')){
                    $(this).text('退出编辑');
                    $(this).removeClass('btn-warning');
                    $('#table_body').find(':checkbox').each(function () {
                    if($(this).prop('checked')){
                        $(this).prop('checked',false);
                        var $tr=$(this).parent().parent();
                        OutEdit($tr)
                    }
                })
                }else {
                    $(this).addClass('btn-warning');
                    $(this).text('进入编辑模式');
                    $('#table_body').find(':checkbox').each(function () {
                    if($(this).prop('checked')){
                        $(this).prop('checked',true);
                        var $tr=$(this).parent().parent();
                        IntoEdit($tr)
                }
            })
                }
            });
            $('#checkDelete').click(function () {
                // $('#table_body').find(':checkbox')
                var idlist =[];
                $('#table_body').find(':checked').each(function () {
                    idlist.push($(this).val())
                });
                $.ajax({
                    url:url,
                    type:'DELETE',
                    data:JSON.stringify(idlist),
                    success:function (arg) {
                        console.log(arg)
                    }
                })
            });

            $('#checkSave').click(function () {
                 if($('#INoutEdit').hasClass('btn-warning')){
                    $('#table_body').find(':checkbox').each(function () {
                    if($(this).prop('checked')){
                        var $tr=$(this).parent().parent();
                        OutEdit($tr);
                    }
                });
                 }
                    var all_list=[];
                     //获取用户修改过的数据
                     $('#table_body').children().each(function () {
                        row_dict={};
                         var $tr=$(this);
                         var nid=$(this).attr('nid');
                         flag=false;
                         $($tr).children().each(function () {
                             var name=$(this).attr('name');
                             if($(this).attr('editable')){
                             if($(this).attr('edit_type')=='select'){
                                var new_data=$(this).attr('new-origin');
                                var old_data=$(this).attr('origin');
                                if(new_data){
                                    if(new_data!=old_data){
                                    row_dict[name]=new_data;
                                    flag=true;
                               }
                             }
                            }else {
                                var new_dd=$(this).text();
                                var old_cc=$(this).attr('origin');
                                if(new_dd!=old_cc){
                                    row_dict[name]=new_data;
                                    // flag=true
                            }
                         }
                     }
                        });
                         if(flag){
                             row_dict['id']=nid;
                         }
                         console.log(row_dict,'1111');
                         all_list.push(row_dict)
                        }
                     );
                    // all_list.push(row_dict);
                     //ajax提交后台
                    $.ajax({
                    url:url,
                    type:'PUT',
                    data:JSON.stringify(all_list),
                    success:function (arg) {
                        console.log(arg)
                    }
                })

            })

        }
    })

})(jQuery);