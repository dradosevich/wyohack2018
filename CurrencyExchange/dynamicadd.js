//Danny Radosevich
//Dynamically add the images


var itemID = 0; //helps keep track of elements
var elems = new Array();


function addToGrid(data)
{
  //alert("adding");
  //create the ID for the element to be accessed
      var id = "data"+ itemID;
      itemID++;
      //add id to an array to keep track
      elems.push(id);
      caption = data;
      //set up the figure for dispaly
      var newFig = document.createElement("img");
      var divFig = document.createElement("div");
      var text = document.createTextNode(caption);
      var br = document.createElement("br");


      if(elemType=='tag')
      {
        newFig.src = './res/folder.png';
      }
      else if (elemType=='file')
      {
        newFig.src = './res/icon.png';
      }

      //Setting up the figure
      //newFig.src = 'https://cdn.bulbagarden.net/upload/7/73/004Charmander.png';
      //newFig.src = './res/icon.png';
      newFig.height = '90%';
      newFig.width = '90%';

      // creating the text below the figure

      //adding the picture to the display area
      divFig.appendChild(newFig);
      divFig.appendChild(br);
      divFig.appendChild(text);
      divFig.setAttribute("class","image");
      divFig.style.padding = "5px 5px 5px 5px";
      divFig.style.width = "90%";
      divFig.id=id;
      //text.setAttribute("align","bottom");
      document.getElementById('grid').appendChild(divFig);
}
function clearGrid() //empties the grid and the elements in the array
{
  for(var i=0; i <elems.length; i++)
  {
    var toRemove = document.getElementById(elems[i]);
    toRemove.parentNode.removeChild(toRemove);
  }
  elems = [];
}
