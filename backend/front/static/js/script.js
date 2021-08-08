function get_cookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
  }
  
function set_cookie ( name, value, exp_y, exp_m, exp_d, path, domain, secure )
{
  var cookie_string = name + "=" + escape ( value );
 
  if ( exp_y )
  {
    var expires = new Date ( exp_y, exp_m, exp_d );
    cookie_string += "; expires=" + expires.toGMTString();
  }
 
  if ( path )
        cookie_string += "; path=" + escape ( path );
 
  if ( domain )
        cookie_string += "; domain=" + escape ( domain );
  
  if ( secure )
        cookie_string += "; secure";
  
  document.cookie = cookie_string;
}


  function CreateRequest()
  {
    var Request = false;
    
    if (window.XMLHttpRequest)
    {
        //Gecko-совместимые браузеры, Safari, Konqueror
        Request = new XMLHttpRequest();
        
    }
    else if (window.ActiveXObject)
    {
        //Internet explorer
        try
        {
            Request = new ActiveXObject("Microsoft.XMLHTTP");
        }    
        catch (CatchException)
        {
            Request = new ActiveXObject("Msxml2.XMLHTTP");
        }
    }
  
    if (!Request)
    {
        alert("Невозможно создать XMLHttpRequest");
    }
    
    return Request;
  } 
  
  function SendRequest(r_method, r_path, r_args, r_handler)
  {
    //Создаём запрос
    var Request = CreateRequest();
    
    //Проверяем существование запроса еще раз
    if (!Request)
    {
        
      return;

    }
    
    //Назначаем пользовательский обработчик
    Request.onreadystatechange = function()
    {
      
        //Если обмен данными завершен
        if (Request.readyState == 4)
        {
            //Передаем управление обработчику пользователя
            r_handler(Request);
        }
    }
    
    //Проверяем, если требуется сделать GET-запрос
    if (r_method.toLowerCase() == "get" && r_args.length > 0)
    r_path += "?" + r_args;
    
    //Инициализируем соединение
    Request.open(r_method, r_path, true);
    
    if (r_method.toLowerCase() == "post")
    {
        //Если это POST-запрос
        
        csrftoken = get_cookie('csrftoken');
        
        //Устанавливаем заголовок
        Request.setRequestHeader("X-CSRFToken", csrftoken );
        Request.setRequestHeader("Content-Type","application/x-www-form-urlencoded; charset=utf-8");
        //Посылаем запрос
        Request.send(r_args);
    }
    else
    {
        //Если это GET-запрос
        
        //Посылаем нуль-запрос
        Request.send(null);
    }
  }

  function get_param(name){
    if(name=(new RegExp('[?&]'+encodeURIComponent(name)+'=([^&]*)')).exec(location.search))
       return decodeURIComponent(name[1]);
 }


 $(document).ready(function() {
  
    $('#submit').click(function () {

      let url = $("#searchinput").val();
      console.log(url)
      let params = "url=" +url;   
      if (url){
          SendRequest("post", "/", params, (response )=>{
            console.log(response)

  
          })
        }
      else
      {
          alert("Введите ссылку")}
    }) 



  
  

  
  });