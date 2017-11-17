tinyMCE.init({
    mode:"textareas",
    plugins : "advlist,anchor,autolink,autoresize,autosave,bbcode,charmap,code,codesample,colorpicker,contextmenu,directionality,emoticons,fullpage,fullscreen,help,hr,image,imagetools,importcss,insertdatetime,legacyoutput,link,lists,media,nonbreaking,noneditable,pagebreak,paste,preview,print,save,searchreplace,spellchecker,tabfocus,table,template,textcolor,textpattern,toc,visualblocks,visualchars,wordcount",
    extended_valid_elements :  'script[type|src],iframe[src|width|height|scrolling|marginwidth|marginheight|frameborder],div[*],p[*],object[width|height|classid|codebase|embed|param],param[name|value],embed[param|src|type|width|height|flashvars|wmode]',
    // Theme options
    theme_advanced_buttons1 :  "bold,italic,underline,strikethrough,|,justifyleft,justifycenter,justifyright,justifyfull,|,bullist,numlist,sub,sup,|,forecolor,backcolor,formatselect,fontsizeselect",
    theme_advanced_buttons2 :  "preview,|,outdent,indent,|,undo,redo,|,link,unlink,anchor,image,tablecontrols,removeformat,code,emotions",
    theme_advanced_toolbar_location : "top",
    theme_advanced_toolbar_align : "left",
    theme_advanced_statusbar_location : "bottom",
forced_root_block : false,
    force_p_newlines : false,
    remove_linebreaks : false,
    force_br_newlines : true,
    remove_trailing_nbsp : false,
    verify_html : false,
});
