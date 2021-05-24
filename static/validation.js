Focus = ()=>
    {
        document.getElementById('username').focus();
        return true;
    }
UnameCheck = ()=>{
     var uname = document.getElementById('username').value;
    let strongUname = new RegExp('(?=.{5,})')

     if(!(strongUname.test(uname))) 
        document.getElementById('msg').innerText = '*Minimum 5 characters required';
    else
        document.getElementById('msg').innerText = '';

}
PasswordChecker = () => {

    let password = document.getElementById('password').value;
    let strongPassword = new RegExp('((?=.*[a-z])|(?=.*[A-Z]))(?=.*[0-9])(?=.{6,})')
    
    if (!(strongPassword.test(password)))
        {
            console.log("yes");
            document.getElementById('password-check').innerText = `*1. Min 6 characters required 
                 2. Must have [a-z] or [A -Z]
                 3. Must have an integer`;
            document. getElementById("submit"). disabled = true;
        }
    else
    {
        document.getElementById('password-check').innerText = '';
        document. getElementById("submit"). disabled = false;
    }
        
}


