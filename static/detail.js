function validate(){
//document.write(al.value);

if(name.value=="")
{

alert("please fillthe name");
}
else if(email.value=="")
{

    alert("fillthe email");
}
else {
    var e=email.value;
    if(e.includes("@"))
    {
    alert("successful submit");
    }
    else{
        alert("nota valid email");
    }
    
}}
