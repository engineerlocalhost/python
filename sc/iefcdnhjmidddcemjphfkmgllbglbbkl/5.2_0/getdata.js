function timer(ms) {
    return new Promise((r) => setTimeout(r, ms));
  }
   
 
  async function pageScroll()
{
    
	window.scrollBy(0,900); 

}  
pageScroll();
// window.scrollBy(0,500); 