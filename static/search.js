
const search = (e)=>{
    const s = document.getElementById('search').value;
    fun(e ,s);
}

const fun = (e,s)=> {
    e.preventDefault();
    console.log(s);
    $(window).scrollTop($(`td:contains(${s}):last`).offset().top);
    document.getElementsByName('search')[0].placeholder= "Search your Todo";
}
