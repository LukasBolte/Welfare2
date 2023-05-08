var tdList={};
var selectedCutoff;
var cutoffHistory=[];

var leftDiv;
var rightDiv;


var drawChoices = function(base){
    var table=document.createElement("table");
    table.className="table table-hover";
    base.appendChild(table);
    //add header
    thead=document.createElement("thead");
    table.appendChild(thead);
    var trHead=document.createElement("tr");
    thead.appendChild(trHead);
    //now column headers
    var thHead=document.createElement("th");
    thHead.className="text-center";
    thHead.setAttribute("scope","col");
    trHead.appendChild(thHead);
    var text=document.createTextNode(leftHeader);
    thHead.appendChild(text);
    var thHead=document.createElement("th");
    thHead.setAttribute("scope","col");
    thHead.style.width="35%";
    trHead.appendChild(thHead);
    var thHead=document.createElement("th");
    thHead.setAttribute("scope","col");
    thHead.style.width="20%";
    trHead.appendChild(thHead);
    var text=document.createTextNode(rightHeader);
    thHead.appendChild(text);
    thHead.className="text-center";
    thHead.style.width="35%";
    //create body
    var tbody=document.createElement("tbody");
    tbody.addEventListener("mouseleave", unhighlight.bind(this));
    table.appendChild(tbody);
    var counter=0;
    for(let i=0;i<leftBonus.length;i++){
        tr=document.createElement("tr");
        tdList[i]=[];
        tbody.appendChild(tr);
        //left choice
        td=document.createElement("td");
        td.className="text-center";
        var text=document.createTextNode("...$"+leftBonus[i]);
        td.appendChild(text);
        td.setAttribute("cutoff","left:"+i);
        tr.appendChild(td);
        tdList[i].push(td);
        td.addEventListener("click", selectCutoff.bind(this));
        td.addEventListener("mouseenter", highlightSelection.bind(this));
        //middle OR
        td=document.createElement("td");
        td.className="text-center";
        text=document.createTextNode("OR");
        td.setAttribute("cutoff","middle:"+i);
        td.appendChild(text);
        tr.appendChild(td);
        td.addEventListener("mouseenter", highlightSelection.bind(this));
        //right choice
        td=document.createElement("td");
        td.className="text-center";
        text=document.createTextNode("...$"+rightBonus[i]);
        td.appendChild(text);
        td.setAttribute("cutoff","right:"+i);
        tr.appendChild(td);        
        tdList[i].push(td);
        td.addEventListener("click", selectCutoff.bind(this));
        td.addEventListener("mouseenter", highlightSelection.bind(this));
        counter++;
    }
    countTDtotal=counter;
    maxY=td.offsetTop;
}

var formatExplainer = function(rows,leftright){
    if (rows==1){
        return "If this row is selected for payment you are choosing the "+leftright+" option."
    }
    else{  
        return "If one of these "+rows+" rows is selected for payment you are choosing the "+leftright+" option."
    }
}

var highlight = function(cutoff,color){
    var choiceFrags=cutoff.split(':');
    var cutoffNum=parseFloat(choiceFrags[1]);
    for(var c in tdList){
        var cf=parseFloat(c);
        $(tdList[c][0]).removeClass("orange");
        $(tdList[c][0]).removeClass("darkorange");
        $(tdList[c][1]).removeClass("orange");
        $(tdList[c][1]).removeClass("darkorange");
        if (cf<cutoffNum){
            $(tdList[c][0]).addClass(color);
        }
        if (cf>cutoffNum){
            $(tdList[c][1]).addClass(color);
        }
        if (cf==cutoffNum){
            switch(choiceFrags[0]){
                case "left":
                    $(tdList[c][0]).addClass(color);
                    break;
                case "middle":
                    break;
                case "right":
                    $(tdList[c][1]).addClass(color);
                    break;
            }
        }
    }    
}

var unhighlight = function(){
    if (this.selectedCutoff){
        return;
    }
    for(var c in tdList){
        $(tdList[c][0]).removeClass("orange");
        $(tdList[c][1]).removeClass("orange");
        $(tdList[c][0]).removeClass("darkorange");
        $(tdList[c][1]).removeClass("darkorange");
    }
}

var showNext=function(){
    var nextButton=document.getElementById("id_next_button");
    if (nextButton){
        nextButton.style.display="";
    }
}

var selectCutoff = function(e){
    if (selectedCutoff){
        cutoffHistory.push(selectedCutoff);
    }
    var cutoff=e.target.getAttribute("cutoff");
    selectedCutoff=cutoff;
    highlight(cutoff,"darkorange");
    //save data in hidden field
    document.getElementById(varname).value=JSON.stringify({"history":cutoffHistory,"cutoff":selectedCutoff});     
    console.log(document.getElementById(varname).value);  
    //make the oTree next button appear if present
    setTimeout(showNext,2000);
}

var highlightSelection = function(e){
    e.target.style.cursor = "pointer";
    if (selectedCutoff){
        return;
    }
    var cutoff=e.target.getAttribute("cutoff");
    highlight(cutoff,"orange");
}


var drawWTP=function(){
    var hiddenDiv = document.getElementById("hidden_fields_wtp_elicitation");
    var hiddenField=document.createElement("input");
    hiddenDiv.appendChild(hiddenField);
    hiddenField.setAttribute("type","hidden");
    hiddenField.setAttribute("name",varname);
    hiddenField.setAttribute("id",varname); 
    //draw game  
    var container=document.createElement("div");
    container.className="container";
    document.getElementById("wtp_elicitation").appendChild(container);
    var row=document.createElement("div");
    row.className="row";
    container.appendChild(row);
    leftDiv=document.createElement("div");
    leftDiv.className="col-2";
    leftDiv.innerHTML="&nbsp;";
    row.appendChild(leftDiv);
    var midDiv=document.createElement("div");
    midDiv.className="col-8";
    row.appendChild(midDiv);
    rightDiv=document.createElement("div");
    rightDiv.className="col-2";
    rightDiv.innerHTML="&nbsp;";
    row.appendChild(rightDiv);
    drawChoices(midDiv);
}

drawWTP();