

const nodes = document.querySelectorAll(".box")
const parent = document.querySelector(".hero")
let boxes = toArray(nodes)
let aux_list = []


function toArray(boxes){

    let array = []
    for(let i = 0;i<boxes.length;i++){
        array.push(boxes[i])
    }
    return array
}


function changeHandler(){
    parent.innerHTML = ""
    if(aux_list.length == 0){
        aux_list = [...boxes]
    }
    const box = `<div class="box">${aux_list.pop().innerHTML}</div>`
    parent.innerHTML = box
}



window.onload = () =>{

setInterval(changeHandler, 5000);

}



