
const Focus = ()=>
{
    document.getElementById('title').focus();
    if(window.location.href.includes('update'))
      {
        var SearchBAr = document.getElementById("search");
        var SearchButton = document.getElementById("search-button");
        SearchBAr.remove();
        SearchButton.remove();

      }
    return true;
}

const search = (e)=>{
    const s = document.getElementById('search').value.trim();
    console.log(s);
    fun(e,s);
}

const fun = (e,s)=> {
    e.preventDefault();
    console.log(s);
    $(window).scrollTop($(`td:contains(${s}):last`).offset().top);
    document.getElementsByName('search')[0].placeholder= "Search your Todo";
}

// const fun = (e)=> {
//   if (e !== "") {
//     let text = document.getElementsById("search-input").innerText;
//     console.log(text);
//   	let re = new RegExp(e,"gi"); // search for all instances
//       console.log(re);
// 		let newText = text.replace(re, `<td><mark>${e}</mark></td>`);
// 		document.getElementById("search-input").innerHTML = newText;
//   }
// }
